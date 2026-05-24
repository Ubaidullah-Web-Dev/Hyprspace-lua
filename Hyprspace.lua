local M = {}

local HOME = os.getenv("HOME") or ""
local MATUGEN_PATH = HOME .. "/.config/matugen/generated/hyprland-colors.lua"
local plugin_path = os.getenv("HYPRSPACE_PLUGIN_PATH") or (HOME .. "/.config/hypr/edit_here/Hyprspace/Hyprspace.so")
local user_opts = {}

-- Define local color variables so that both unquoted identifiers and quoted strings resolve properly
local primary = "primary"
local secondary = "secondary"
local tertiary = "tertiary"
local error = "error"
local background = "background"
local surface = "surface"
local surface_variant = "surface_variant"
local outline = "outline"
local inverse_on_surface = "inverse_on_surface"
local on_surface = "on_surface"
local primary_container = "primary_container"
local secondary_container = "secondary_container"
local tertiary_container = "tertiary_container"
local outline_variant = "outline_variant"


local function file_exists(path)
    if type(path) ~= "string" or path == "" then
        return false
    end

    local file = io.open(path, "r")
    if not file then
        return false
    end

    file:close()
    return true
end

local function shell_quote(value)
    return "'" .. tostring(value):gsub("'", "'\\''") .. "'"
end

local function load_colors(path)
    local env = {}
    local chunk = loadfile(path, "t", env)
    if not chunk then
        return {}
    end

    local ok = pcall(chunk)
    if not ok then
        return {}
    end

    return env
end

local function rgba_to_aarrggbb(value, fallback)
    if type(fallback) ~= "number" then
        return nil
    end

    local hex = type(value) == "string" and value:match("^rgba%((%x%x%x%x%x%x%x%x)%)$")
    if not hex then
        return fallback
    end

    local parsed = tonumber("0x" .. hex:sub(7, 8) .. hex:sub(1, 2) .. hex:sub(3, 4) .. hex:sub(5, 6))
    if type(parsed) ~= "number" then
        return fallback
    end

    return parsed
end

local function with_alpha(value, alpha, fallback)
    if type(fallback) ~= "number" then
        return nil
    end

    local base = rgba_to_aarrggbb(value, fallback)
    if type(base) ~= "number" then
        base = fallback
    end

    return ((alpha & 0xff) << 24) | (base & 0x00ffffff)
end

local function plugin_loaded()
    return hl.plugin and hl.plugin.Hyprspace and type(hl.plugin.Hyprspace.overview) == "function"
end

local function ensure_plugin_loaded()
    if plugin_loaded() then
        return true
    end

    if not file_exists(plugin_path) then
        return false
    end

    hl.exec_cmd("hyprctl plugin load " .. shell_quote(plugin_path))
    return plugin_loaded()
end

-- =============================================================================
-- AST-MUTATOR-COMPATIBLE SCHEMAS CAPTURING WRAPPER
-- =============================================================================
local original_hl_config = hl.config
local registered_config = {}

hl.config = function(tbl)
    if type(tbl) == "table" and tbl.plugin and tbl.plugin.hyprspace then
        for k, v in pairs(tbl.plugin.hyprspace) do
            registered_config[k] = v
        end
    end
    -- Only invoke the original hl.config call inside the TUI sandbox (where os.getenv("HOME") is mocked to nil)
    -- to prevent Hyprland parser warnings outside the sandbox prior to option resolution.
    if os.getenv("HOME") == nil then
        original_hl_config(tbl)
    end
end

-- The root-level AST configuration block. The TUI's token parser will modify this block directly.
hl.config {
    plugin = {
        hyprspace = {
            panel_color                   = surface,
            panel_border_color            = error,
            workspace_active_background   = primary,
            workspace_inactive_background = primary,
            workspace_active_border       = secondary,
            workspace_inactive_border     = on_surface,

            panel_height                  = 200,
            panel_border_width            = 3,
            workspace_margin              = 14,
            reserved_area                 = 0,
            workspace_border_size         = 4,

            adaptive_height               = false,
            center_aligned                = true,
            on_bottom                     = true,
            hide_background_layers        = false,
            hide_top_layers               = false,
            hide_overlay_layers           = false,
            draw_active_workspace         = true,
            hide_real_layers              = false,
            affect_strut                  = false,

            auto_drag                     = true,
            auto_scroll                   = true,
            exit_on_click                 = true,
            switch_on_drop                = false,
            exit_on_switch                = false,
            show_new_workspace            = true,
            show_empty_workspace          = true,
            show_special_workspace        = false,

            disable_gestures              = true,
            reverse_swipe                 = false,
            swipe_fingers                 = 3,
            swipe_distance                = 300,
            swipe_force_speed             = 30,
            swipe_cancel_ratio            = 0.5,
            swipe_threshold               = 10.0,
            swipe_closed_padding          = 10.0,
            workspace_scroll_speed        = 2.0,

            disable_blur                  = false,
            override_anim_speed           = 0.0,
            drag_alpha                    = 0.2,
            exit_key                      = "Escape",
            click_release_threshold_ms    = 200,

            override_gaps                 = false,
            gaps_in                       = 0,
            gaps_out                      = 0,
        }
    }
}

-- Restore the original hl.config function reference
hl.config = original_hl_config

-- Color metadata to resolve Matugen colors with custom transparency levels
local color_meta = {
    panel_color = {
        matugen_keys = { "surface_container_high", "surface" },
        default_alpha = 0x20,
        fallback = 0x20261d20
    },
    panel_border_color = {
        matugen_keys = { "primary", "outline" },
        default_alpha = 0x38,
        fallback = 0x38ffb0cf
    },
    workspace_active_background = {
        matugen_keys = { "surface_container_highest", "surface_container_high" },
        default_alpha = 0x40,
        fallback = 0x403c3235
    },
    workspace_inactive_background = {
        matugen_keys = { "surface_container", "surface" },
        default_alpha = 0x0c,
        fallback = 0x0c261d20
    },
    workspace_active_border = {
        matugen_keys = { "primary", "on_surface" },
        default_alpha = 0xa0,
        fallback = 0xa0ffb0cf
    },
    workspace_inactive_border = {
        matugen_keys = { "outline_variant", "outline" },
        default_alpha = 0x15,
        fallback = 0x15504348
    }
}

local function resolve_color(key, value, colors)
    local meta = color_meta[key]
    if not meta then
        return value
    end

    if type(value) ~= "string" then
        return value
    end

    -- Direct rgba specification (keeps user-customized transparency alpha)
    if value:match("^rgba%((%x%x%x%x%x%x%x%x)%)$") then
        return rgba_to_aarrggbb(value, meta.fallback)
    end

    -- Look up in loaded Matugen colors
    local color_val = colors[value]
    if not color_val then
        -- Fall back to default matugen keys matching this setting
        for _, mk in ipairs(meta.matugen_keys) do
            if colors[mk] then
                color_val = colors[mk]
                break
            end
        end
    end

    if color_val then
        return with_alpha(color_val, meta.default_alpha, meta.fallback)
    end

    return meta.fallback
end

local function build_config()
    local colors = load_colors(MATUGEN_PATH)
    local config = {}

    -- Apply registered defaults (possibly updated by TUI write operations)
    for k, v in pairs(registered_config) do
        if color_meta[k] then
            config[k] = resolve_color(k, v, colors)
        else
            config[k] = v
        end
    end

    -- Merge user overrides passed via M.setup(...)
    for k, v in pairs(user_opts) do
        if k ~= "plugin_path" then
            if color_meta[k] then
                config[k] = resolve_color(k, v, colors)
            else
                config[k] = v
            end
        end
    end

    return {
        plugin = {
            hyprspace = config,
        },
    }
end

local function apply_config()
    if not plugin_loaded() then
        return false
    end

    -- Hyprland 0.55+ native config path.
    hl.config(build_config())
    return true
end

function M.setup(opts)
    if type(opts) == "table" then
        if type(opts.plugin_path) == "string" then
            plugin_path = opts.plugin_path
        end
        user_opts = opts
    end

    hl.on("hyprland.start", function()
        ensure_plugin_loaded()
        apply_config()
    end)

    ensure_plugin_loaded()
    apply_config()
end

return M