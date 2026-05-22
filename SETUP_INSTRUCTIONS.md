# Hyprspace Lua Integration & Setup Guide

This guide details how to clone, install, configure, and compile the **Hyprspace-lua** plugin for your custom Hyprland environment. It is tailored to match your specific Lua config files, including your keybinds, trackpad gestures, and premium super-blurry glassmorphic aesthetic.

---

## 🚀 Installation & Setup Steps

### 1. Clone the Repository
Clone the repository directly into your home directory:
```bash
git clone https://github.com/Ubaidullah-Web-Dev/Hyprspace-lua.git ~/Hyprspace-lua
```

### 2. Move to Configuration Directory
Move the cloned repository to your config location and establish the necessary symbolic link so the Lua configuration modules can resolve correctly:

```bash
# 1. Back up any existing Hyprspace config directory if present
if [ -d ~/.config/Hyprspace ]; then
    mv ~/.config/Hyprspace ~/.config/Hyprspace.bak_$(date +%s)
fi

# 2. Move the repository to ~/.config/Hyprspace
mv ~/Hyprspace-lua ~/.config/Hyprspace

# 3. Create a symlink in ~/.config/hypr so require("Hyprspace.Hyprspace") can find it
ln -sfn ~/.config/Hyprspace ~/.config/hypr/Hyprspace
```

### 3. Compile the Plugin
Build the C++ shared object (`Hyprspace.so`) using the provided Makefile:
```bash
cd ~/.config/Hyprspace
make all
```
> [!NOTE]
> This compiles the source files and generates `~/.config/Hyprspace/Hyprspace.so` which is the binary loaded into Hyprland.

---

## 🛠️ Configuration Settings (Lua-Based)

These configurations are designed specifically for your system layout. Ensure the following settings are present in your respective config files inside `~/.config/hypr/edit_here/source/`.

### A. Autostart & Loading
The plugin is automatically initialized on Hyprland startup via your plugins configuration. Add the following block to your `plugins.lua`:

**File Path:** `~/.config/hypr/edit_here/source/plugins.lua`
```lua
require("Hyprspace.Hyprspace").setup({
    -- Point to your newly compiled local binary
    plugin_path = HOME .. "/.config/Hyprspace/Hyprspace.so",
    panel_height = 175,
    reserved_area = 36,
    switch_on_drop = true,
    exit_on_switch = true,
    disable_gestures = true, -- Disables internal C++ gestures in favor of trackpad.lua
})
```

---

### B. Keyboard Keybinds
To toggle the workspace overview with a keyboard shortcut, bind the dispatch function in your keybinds config:

**File Path:** `~/.config/hypr/edit_here/source/keybinds.lua`
```lua
-- Bind Alt + Tab to toggle Hyprspace overview
hl.unbind("ALT + TAB")
hl.bind(
    "ALT + TAB",
    function()
        if hl.plugin and hl.plugin.Hyprspace and type(hl.plugin.Hyprspace.overview) == "function" then
            hl.plugin.Hyprspace.overview("toggle")
        end
    end,
    { description = "Toggle Hyprspace overview" }
)
```

---

### C. Trackpad Gestures
To toggle the overview with a **3-finger swipe up** gesture, configure it in your trackpad settings:

**File Path:** `~/.config/hypr/edit_here/source/trackpad.lua`
```lua
hl.gesture({
    fingers   = 3,
    direction = "up",
    action    = function()
        if hl.plugin and hl.plugin.Hyprspace and type(hl.plugin.Hyprspace.overview) == "function" then
            hl.plugin.Hyprspace.overview("toggle")
        else
            hl.exec_cmd("notify-send 'Hyprspace overview not loaded'")
        end
    end,
})
```

---

## ✨ Design Customizations (Super Blurry & Transparent)

The frosted-glass, transparent aesthetic has been tuned via two main files. If you need to tweak the level of blur or transparency, look at these parameters:

### 1. Panel & Workspace Transparency (Alpha Values)
Transparency is handled in the plugin config using the `with_alpha` helper. Hex values dictate opacity (`0x00` fully transparent, `0xff` fully opaque):

**File Path:** `~/.config/Hyprspace/Hyprspace.lua`
```lua
-- 0x20 and 0x38 indicate highly transparent alpha channel parameters
panel_color        = with_alpha(colors.surface_container_high or colors.surface, 0x20, 0x20261d20),
panel_border_color = with_alpha(colors.primary or colors.outline, 0x38, 0x38ffb0cf),
```

### 2. High-Strength Kawase Blur
The backdrop blur that shines through the transparent workspaces and overview panel is configured globally:

**File Path:** `~/.config/hypr/edit_here/source/appearance.lua`
```lua
decoration = {
    blur = {
        enabled = true,
        size = 12,      -- Large blur radius
        passes = 4,     -- High number of rendering passes for a smooth finish
        ignore_opacity = true,
        new_optimizations = true,
    }
}
```

---

## 🔄 Applying the Changes

After completing all instructions, reload your Hyprland configuration to load the plugin and apply the visual properties:
```bash
hyprctl reload
```

To verify that the plugin loaded correctly, run:
```bash
hyprctl plugins list
```
You should see `Hyprspace` listed in the loaded plugins. Press `Alt + Tab` or swipe up with three fingers to open the workspace overview!
