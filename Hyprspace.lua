local M = {}

local HOME = os.getenv("HOME") or ""
local MATUGEN_PATH = HOME .. "/.config/matugen/generated/hyprland-colors.lua"
local plugin_path = os.getenv("HYPRSPACE_PLUGIN_PATH") or (HOME .. "/.config/hypr/edit_here/Hyprspace/Hyprspace.so")
local user_opts = {}

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

local function build_config()
    local colors = load_colors(MATUGEN_PATH)

    local config = {
        panel_color                   = with_alpha(colors.surface_container_high or colors.surface, 0x20, 0x20261d20),
        panel_border_color            = with_alpha(colors.primary or colors.outline, 0x38, 0x38ffb0cf),
        workspace_active_background   = with_alpha(colors.surface_container_highest or colors.surface_container_high, 0x40, 0x403c3235),
        workspace_inactive_background = with_alpha(colors.surface_container or colors.surface, 0x0c, 0x0c261d20),
        workspace_active_border       = with_alpha(colors.primary or colors.on_surface, 0xa0, 0xa0ffb0cf),
        workspace_inactive_border     = with_alpha(colors.outline_variant or colors.outline, 0x15, 0x15504348),

        panel_height                  = 220,
        panel_border_width            = 2,
        workspace_margin              = 10,
        reserved_area                 = 35,
        workspace_border_size         = 1,

        adaptive_height               = false,
        center_aligned                = true,
        on_bottom                     = false,
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

        disable_gestures              = false,
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
    }

    -- Merge user options
    for k, v in pairs(user_opts) do
        if k ~= "plugin_path" then
            config[k] = v
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