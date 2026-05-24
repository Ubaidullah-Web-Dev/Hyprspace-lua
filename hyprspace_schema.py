#!/usr/bin/env python3
"""
===============================================================================
DUSKY TUI: HYPRSPACE CONFIGURATION SCHEMA
===============================================================================
Target: ~/.config/Hyprspace/Hyprspace.lua
Engine: lua
"""

from python.frontend.core_types import ConfigItem

# =============================================================================
# 1. CORE APPLICATION ROUTING (REQUIRED)
# =============================================================================
ENGINE_TYPE = "lua"
TARGET_FILE = "~/.config/Hyprspace/Hyprspace.lua"
APP_TITLE = "Hyprspace Overview Configuration"

# =============================================================================
# 2. UI & ENVIRONMENT BEHAVIOR
# =============================================================================
DEFAULT_MODE = "auto"

# STRICT REQUIREMENT: This exact path must always exist.
THEME_FILE = "~/.config/matugen/generated/dusky_tui.json"

# Enable dynamic user profiles on the designated Profiles tab
ENABLE_USER_PRESETS = True
USER_PRESETS_TAB = "Profiles"

# Global popup when launched
GLOBAL_POPUP = {
    "title": "Hyprspace Manager",
    "message": "Configure live workspace exposures, layout parameters, colors, and input gestures.",
    "level": "success",
    "require_confirm": False,
    "cancel_quits": False
}

# Informative messages drawn at the top of specific tabs
TAB_NOTICES = {
    0: {"level": "info", "message": "Quickly trigger compositor reloads or apply visual presets."},
    1: {"level": "success", "message": "Configure panel dimensions and visual theme colors."},
    3: {"level": "warning", "message": "Gesture thresholds and finger offsets depend on your input driver."}
}

# =============================================================================
# 3. TABS DEFINITION
# STRICT RULE: Keep tab names strictly ONE WORD.
# =============================================================================
TABS = [
    "Presets",
    "Panel",
    "Workspaces",
    "Gestures",
    "Performance",
    "Profiles"
]

# =============================================================================
# COLOR ALIASES
# =============================================================================
COLOR_ALIASES = [
    # Matugen dynamic variables
    "primary", "secondary", "tertiary", "error", "background", 
    "surface", "surface_variant", "outline", "inverse_on_surface", 
    "on_surface", "primary_container", "secondary_container", "tertiary_container",
    
    # Core system transparencies
    "rgba(1a1a1aee)", "rgba(ffffff11)", "rgba(00000000)",
    
    # Hardcoded base options
    "rgba(ff0000ff)", # Red
    "rgba(00ff00ff)", # Green
    "rgba(0000ffff)", # Blue
    "rgba(ffa500ff)", # Orange
    "rgba(ffff00ff)", # Yellow
    "rgba(800080ff)", # Purple
    "rgba(00ffffff)", # Cyan
    "rgba(ffd700ff)", # Golden
    "rgba(000000ff)", # Black
    "rgba(ffffffff)", # White
    "rgba(ffc0cbff)", # Pink
    "rgba(808080ff)"  # Gray
]

# =============================================================================
# 4. SCHEMA DEFINITION
# =============================================================================
SCHEMA = {
    # -------------------------------------------------------------------------
    # TAB 0: PRESETS & ACTIONS
    # -------------------------------------------------------------------------
    0: [
        ConfigItem(
            label="Reload Hyprland Config",
            key="action_reload_hyprland",
            scope="DEFAULT",
            type_="action",
            default="hyprctl reload",
            group="System",
            popup_message="Hyprland configuration reloaded successfully!",
            extended_help="**Reload Hyprland**\n\nExecutes the `hyprctl reload` shell command to instantly apply saved overview changes inside the Hyprland compositor."
        ),
        ConfigItem(
            label="Reset Overview Defaults",
            key="preset_factory_reset",
            scope="DEFAULT",
            type_="preset",
            default=None,
            group="System",
            confirm_message="Are you sure you want to revert all values back to defaults?",
            preset_payload={"__ALL_DEFAULTS__": True},
            extended_help="**Factory Reset**\n\nReverts all customized configurations inside the Hyprspace panel settings back to original defaults."
        ),
        ConfigItem(
            label="Compact Overview",
            key="pre_compact_clean",
            scope="DEFAULT",
            type_="preset",
            default=None,
            group="Presets",
            preset_payload={
                "plugin/hyprspace.panel_height": 160,
                "plugin/hyprspace.panel_border_width": 1,
                "plugin/hyprspace.workspace_margin": 6,
                "plugin/hyprspace.workspace_border_size": 2,
                "plugin/hyprspace.reserved_area": 20,
                "plugin/hyprspace.adaptive_height": True,
                "plugin/hyprspace.center_aligned": True,
                "plugin/hyprspace.drag_alpha": 0.1,
                "plugin/hyprspace.workspace_active_background": "rgba(ffffff11)",
                "plugin/hyprspace.panel_color": "surface",
            },
            extended_help="**Compact Overview Preset**\n\nResizes and packs cards tightly. Sets panel height to 160px with narrow workspace margins."
        ),
        ConfigItem(
            label="Bottom Dock Layout",
            key="pre_bottom_expo",
            scope="DEFAULT",
            type_="preset",
            default=None,
            group="Presets",
            preset_payload={
                "plugin/hyprspace.on_bottom": True,
                "plugin/hyprspace.panel_height": 260,
                "plugin/hyprspace.workspace_margin": 12,
                "plugin/hyprspace.workspace_border_size": 4,
                "plugin/hyprspace.workspace_active_border": "primary",
                "plugin/hyprspace.reserved_area": 40,
                "plugin/hyprspace.center_aligned": True,
            },
            extended_help="**Bottom Expo Preset**\n\nMoves exposure blocks to the bottom monitor edge, emulating a panel dock layout."
        ),
        ConfigItem(
            label="Touch Optimized Settings",
            key="pre_touch",
            scope="DEFAULT",
            type_="preset",
            default=None,
            group="Presets",
            preset_payload={
                "plugin/hyprspace.disable_gestures": False,
                "plugin/hyprspace.swipe_fingers": 3,
                "plugin/hyprspace.swipe_distance": 220,
                "plugin/hyprspace.swipe_force_speed": 40,
                "plugin/hyprspace.swipe_threshold": 5.0,
                "plugin/hyprspace.auto_drag": True,
                "plugin/hyprspace.workspace_scroll_speed": 3.0,
            },
            extended_help="**Touch Screen Preset**\n\nSets sensitive swipes, 3-finger recognition, and low distance thresholds."
        ),
        ConfigItem(
            label="Keyboard Productivity Mode",
            key="pre_kb_centric",
            scope="DEFAULT",
            type_="preset",
            default=None,
            group="Presets",
            preset_payload={
                "plugin/hyprspace.disable_gestures": True,
                "plugin/hyprspace.auto_scroll": False,
                "plugin/hyprspace.exit_on_switch": True,
                "plugin/hyprspace.exit_on_click": True,
                "plugin/hyprspace.disable_blur": True,
                "plugin/hyprspace.override_anim_speed": 4.0,
            },
            extended_help="**Keyboard Profile**\n\nDisables swipes, turns off blur, sets high animation speeds, and closes overview instantly on switches."
        ),
    ],

    # -------------------------------------------------------------------------
    # TAB 1: PANEL & THEMING
    # -------------------------------------------------------------------------
    1: [
        ConfigItem(
            label="Panel Height Size",
            key="panel_height",
            scope="plugin/hyprspace",
            type_="int",
            default=220,
            min_val=100,
            max_val=800,
            step=10,
            group="Dimensions",
            extended_help="**Panel Height**\n\nSets the base pixel height for the workspace exposure strip."
        ),
        ConfigItem(
            label="Panel Border Width",
            key="panel_border_width",
            scope="plugin/hyprspace",
            type_="int",
            default=2,
            min_val=0,
            max_val=10,
            step=1,
            group="Dimensions",
            extended_help="**Border Width**\n\nThickness of the outer panel contour border."
        ),
        ConfigItem(
            label="Adaptive Height Scale",
            key="adaptive_height",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Toggles",
            extended_help="**Adaptive Height**\n\nDynamically adjusts container heights based on aspect ratios."
        ),
        ConfigItem(
            label="Center Aligned Panel",
            key="center_aligned",
            scope="plugin/hyprspace",
            type_="bool",
            default=True,
            group="Toggles",
            extended_help="**Center Alignment**\n\nCenters the active exposure workspace strip."
        ),
        ConfigItem(
            label="Position Panel on Bottom",
            key="on_bottom",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Toggles",
            extended_help="**On Bottom**\n\nToggles positioning between the top or bottom of the screen."
        ),
        ConfigItem(
            label="Panel Color Fill",
            key="panel_color",
            scope="plugin/hyprspace",
            type_="color",
            default="surface_container_high",
            options=COLOR_ALIASES,
            group="Colors",
            extended_help="**Base Color**\n\nSolid color filling the overview background."
        ),
        ConfigItem(
            label="Panel Border Outline",
            key="panel_border_color",
            scope="plugin/hyprspace",
            type_="color",
            default="primary",
            options=COLOR_ALIASES,
            group="Colors",
            extended_help="**Border Color**\n\nColor highlight tracing the panel borders."
        ),
        ConfigItem(
            label="Active Workspace Card Fill",
            key="workspace_active_background",
            scope="plugin/hyprspace",
            type_="color",
            default="surface_container_highest",
            options=COLOR_ALIASES,
            group="Colors",
            extended_help="**Active Workspace Background**\n\nBackground fill of the focused workspace card."
        ),
        ConfigItem(
            label="Inactive Workspace Card Fill",
            key="workspace_inactive_background",
            scope="plugin/hyprspace",
            type_="color",
            default="surface_container",
            options=COLOR_ALIASES,
            group="Colors",
            extended_help="**Inactive Workspace Background**\n\nBackground fill of all secondary workspace cards."
        ),
        ConfigItem(
            label="Active Workspace Card Border",
            key="workspace_active_border",
            scope="plugin/hyprspace",
            type_="color",
            default="primary",
            options=COLOR_ALIASES,
            group="Colors",
            extended_help="**Active Card Border**\n\nBorder tracing active workspace slots."
        ),
        ConfigItem(
            label="Inactive Workspace Card Border",
            key="workspace_inactive_border",
            scope="plugin/hyprspace",
            type_="color",
            default="outline_variant",
            options=COLOR_ALIASES,
            group="Colors",
            extended_help="**Inactive Card Border**\n\nBorder outline on secondary workspace slots."
        ),
        ConfigItem(
            label="Workspace Outer Margin",
            key="workspace_margin",
            scope="plugin/hyprspace",
            type_="int",
            default=10,
            min_val=0,
            max_val=100,
            step=1,
            group="Layout",
            extended_help="**Workspace Margin**\n\nSpacing separation in pixels between consecutive workspace card boxes."
        ),
        ConfigItem(
            label="Workspace Border Width",
            key="workspace_border_size",
            scope="plugin/hyprspace",
            type_="int",
            default=3,
            min_val=0,
            max_val=20,
            step=1,
            group="Layout",
            extended_help="**Workspace Card Border Size**\n\nBorder thickness of workspace cards."
        ),
        ConfigItem(
            label="Compositor Reserved Area",
            key="reserved_area",
            scope="plugin/hyprspace",
            type_="int",
            default=35,
            min_val=0,
            max_val=200,
            step=5,
            group="Layout",
            extended_help="**Reserved Area**\n\nMargin padding (pixels) avoiding overlap with system status bars."
        ),
    ],

    # -------------------------------------------------------------------------
    # TAB 2: WORKSPACE LOGIC
    # -------------------------------------------------------------------------
    2: [
        ConfigItem(
            label="Draw Active Workspace Block",
            key="draw_active_workspace",
            scope="plugin/hyprspace",
            type_="bool",
            default=True,
            group="Behavior",
            extended_help="**Draw Active Workspace**\n\nRenders the focused workspace block inside the panel."
        ),
        ConfigItem(
            label="Show Empty Workspaces",
            key="show_empty_workspace",
            scope="plugin/hyprspace",
            type_="bool",
            default=True,
            group="Behavior",
            extended_help="**Show Empty Workspaces**\n\nRenders existing empty workspaces between active ones."
        ),
        ConfigItem(
            label="Show Special Workspace Block",
            key="show_special_workspace",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Behavior",
            extended_help="**Show Special Workspace**\n\nShows the scratchpad preview panel in overview."
        ),
        ConfigItem(
            label="Dismiss Overview on Background Click",
            key="exit_on_click",
            scope="plugin/hyprspace",
            type_="bool",
            default=True,
            group="Exit",
            extended_help="**Exit on Click**\n\nCloses overview when clicking on empty workspace spacing."
        ),
        ConfigItem(
            label="Dismiss Overview on Workspace Change",
            key="exit_on_switch",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Exit",
            extended_help="**Exit on Switch**\n\nCloses the overview panel as soon as card focus changes."
        ),
        ConfigItem(
            label="Switch to Workspace on Window Drop",
            key="switch_on_drop",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Drag",
            extended_help="**Switch on Drop**\n\nSwitches active workspace to target slot after dropping window."
        ),
        ConfigItem(
            label="Enable Workspace Auto Dragging",
            key="auto_drag",
            scope="plugin/hyprspace",
            type_="bool",
            default=True,
            group="Drag",
            extended_help="**Auto Drag**\n\nAllows windows to be dragged and reordered inside workspace slot previews."
        ),
        ConfigItem(
            label="Enable Mouse Scroll Navigation",
            key="auto_scroll",
            scope="plugin/hyprspace",
            type_="bool",
            default=True,
            group="Drag",
            extended_help="**Auto Scroll**\n\nEnables scroll navigation through active workspace panels."
        ),
        ConfigItem(
            label="Enable Custom Workspace Gaps",
            key="override_gaps",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            is_parent=True,
            expanded=False,
            group="Gaps",
            extended_help="**Override Gaps**\n\nToggles override margins for spaces inside workspace exposure blocks."
        ),
        ConfigItem(
            label="Workspace Inner Gap Value",
            key="gaps_in",
            scope="plugin/hyprspace",
            type_="int",
            default=0,
            min_val=0,
            max_val=100,
            step=1,
            group="Gaps",
            parent_ref="plugin/hyprspace.override_gaps",
            extended_help="**Inner Gaps**\n\nSpaces (pixels) separating individual window layout tiles."
        ),
        ConfigItem(
            label="Workspace Outer Gap Value",
            key="gaps_out",
            scope="plugin/hyprspace",
            type_="int",
            default=0,
            min_val=0,
            max_val=100,
            step=1,
            group="Gaps",
            parent_ref="plugin/hyprspace.override_gaps",
            extended_help="**Outer Gaps**\n\nSpacing separating tiles from workspace card borders."
        ),
    ],

    # -------------------------------------------------------------------------
    # TAB 3: GESTURE CONFIGS
    # -------------------------------------------------------------------------
    3: [
        ConfigItem(
            label="Overview Exit Key Binding",
            key="exit_key",
            scope="plugin/hyprspace",
            type_="string",
            default="Escape",
            group="Keys",
            extended_help="**Exit Key**\n\nKey used to exit the overview. Standard names like 'Escape', 'q' apply."
        ),
        ConfigItem(
            label="Click Release Time Boundary",
            key="click_release_threshold_ms",
            scope="plugin/hyprspace",
            type_="int",
            default=200,
            min_val=50,
            max_val=1000,
            step=25,
            group="Keys",
            extended_help="**Click Release Boundary (ms)**\n\nMaximum delay separating standard clicks from click-dragging actions."
        ),
        ConfigItem(
            label="Disable Swipe Gestures",
            key="disable_gestures",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            is_parent=True,
            expanded=False,
            group="Swipe",
            extended_help="**Disable Gestures**\n\nSwitches off swipe gesture shortcuts."
        ),
        ConfigItem(
            label="Swipe Trigger Finger Count",
            key="swipe_fingers",
            scope="plugin/hyprspace",
            type_="int",
            default=3,
            min_val=3,
            max_val=5,
            step=1,
            group="Swipe",
            parent_ref="plugin/hyprspace.disable_gestures",
            extended_help="**Swipe Fingers**\n\nTouchpad finger count requirement mapping (standard is 3)."
        ),
        ConfigItem(
            label="Swipe Distance Threshold",
            key="swipe_distance",
            scope="plugin/hyprspace",
            type_="int",
            default=300,
            min_val=100,
            max_val=1500,
            step=50,
            group="Swipe",
            parent_ref="plugin/hyprspace.disable_gestures",
            extended_help="**Swipe Distance**\n\nTrackpad traversal pixels required to trigger workspace transitions."
        ),
        ConfigItem(
            label="Swipe Force Speed Value",
            key="swipe_force_speed",
            scope="plugin/hyprspace",
            type_="int",
            default=30,
            min_val=5,
            max_val=150,
            step=5,
            group="Swipe",
            parent_ref="plugin/hyprspace.disable_gestures",
            extended_help="**Swipe Velocity Multiplier**\n\nVelocity scaling constant applied directly to gestures."
        ),
        ConfigItem(
            label="Swipe Action Cancel Ratio",
            key="swipe_cancel_ratio",
            scope="plugin/hyprspace",
            type_="float",
            default=0.5,
            min_val=0.1,
            max_val=0.9,
            step=0.05,
            group="Swipe",
            parent_ref="plugin/hyprspace.disable_gestures",
            extended_help="**Swipe Cancel Ratio**\n\nPercentage required to trigger snaps back to active positions."
        ),
        ConfigItem(
            label="Swipe Trigger Minimum Threshold",
            key="swipe_threshold",
            scope="plugin/hyprspace",
            type_="float",
            default=10.0,
            min_val=1.0,
            max_val=50.0,
            step=1.0,
            group="Swipe",
            parent_ref="plugin/hyprspace.disable_gestures",
            extended_help="**Start Threshold**\n\nMinimum motion boundary required before swipe recognition triggers."
        ),
        ConfigItem(
            label="Swipe Boundary Closed Padding",
            key="swipe_closed_padding",
            scope="plugin/hyprspace",
            type_="float",
            default=10.0,
            min_val=0.0,
            max_val=100.0,
            step=1.0,
            group="Swipe",
            parent_ref="plugin/hyprspace.disable_gestures",
            extended_help="**Closed Padding**\n\nAdditional boundary offsets (pixels) calculated on edge limit swipes."
        ),
        ConfigItem(
            label="Reverse Swipe Gestures",
            key="reverse_swipe",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Swipe",
            extended_help="**Reverse Swipe**\n\nInverts motion direction mapping."
        ),
        ConfigItem(
            label="Mouse Scroll Speed Multiplier",
            key="workspace_scroll_speed",
            scope="plugin/hyprspace",
            type_="float",
            default=2.0,
            min_val=0.5,
            max_val=10.0,
            step=0.5,
            group="Scroll",
            extended_help="**Scroll Speed**\n\nScroll-wheel multiplier applied while navigating between workspace slots."
        ),
    ],

    # -------------------------------------------------------------------------
    # TAB 4: PERFORMANCE & ADVANCED
    # -------------------------------------------------------------------------
    4: [
        ConfigItem(
            label="Disable Overview Blur Filters",
            key="disable_blur",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Performance",
            extended_help="**Disable Blur**\n\nDisables workspace blur rendering. Improves framerates on low-end hardware."
        ),
        ConfigItem(
            label="Card Drag Opacity Value",
            key="drag_alpha",
            scope="plugin/hyprspace",
            type_="float",
            default=0.2,
            min_val=0.0,
            max_val=1.0,
            step=0.05,
            group="Performance",
            extended_help="**Drag Alpha**\n\nTransparency value applied to workspace panels while dragging them."
        ),
        ConfigItem(
            label="Override Animation Speeds",
            key="override_anim_speed",
            scope="plugin/hyprspace",
            type_="float",
            default=0.0,
            min_val=0.0,
            max_val=20.0,
            step=0.5,
            group="Performance",
            extended_help="**Animation Overrides**\n\nOverride duration multiplier for transition fades (0.0 inherits defaults)."
        ),
        ConfigItem(
            label="Hide Wallpaper Background Layers",
            key="hide_background_layers",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Layers",
            extended_help="**Hide Wallpapers**\n\nHides wallpapers behind workspace card borders."
        ),
        ConfigItem(
            label="Hide Top Panels Layers",
            key="hide_top_layers",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Layers",
            extended_help="**Hide Top Panels**\n\nHides uppermost system panels/bars inside exposure views."
        ),
        ConfigItem(
            label="Hide Screen Overlays Layers",
            key="hide_overlay_layers",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Layers",
            extended_help="**Hide Overlays**\n\nHides modal window overlay layers inside overview slots."
        ),
        ConfigItem(
            label="Hide Native Active Layers",
            key="hide_real_layers",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Layers",
            extended_help="**Hide Real Layers**\n\nHides active compositor panels underlying workspace preview cards."
        ),
        ConfigItem(
            label="Affect Panel Strut Bounds",
            key="affect_strut",
            scope="plugin/hyprspace",
            type_="bool",
            default=False,
            group="Layers",
            extended_help="**Affect Strut**\n\nControls reserving display bounds surrounding geometries."
        ),
    ],
}
