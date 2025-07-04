"""
🐍 CANINANA PREMIUM DESIGN SYSTEM
Ultra-modern, ice-inspired security interface with glassmorphism effects
"""

class PremiumDesignSystem:
    """
    ❄️ ICE-INSPIRED PREMIUM DESIGN SYSTEM
    
    A sophisticated design system inspired by ice crystals, arctic landscapes,
    and premium security aesthetics. Features glassmorphism, subtle gradients,
    and organic curves that convey trust and sophistication.
    """
    
    ICE_PRIMARY = "#1E3A8A"
    ICE_SECONDARY = "#3B82F6"
    ICE_LIGHT = "#EFF6FF"
    ICE_ACCENT = "#60A5FA"
    ICE_ULTRA_LIGHT = "#F8FAFC"
    
    FROST_WHITE = "#FFFFFF"
    FROST_LIGHT = "#F8FAFC"
    FROST_MEDIUM = "#F1F5F9"
    FROST_OVERLAY = "#F8FAFC"
    
    SNAKE_GREEN = "#059669"
    SNAKE_LIGHT = "#D1FAE5"
    SNAKE_ACCENT = "#10B981"
    
    SUCCESS_GREEN = "#059669"
    SUCCESS_LIGHT = "#ECFDF5"
    WARNING_AMBER = "#D97706"
    WARNING_LIGHT = "#FFFBEB"
    DANGER_RED = "#DC2626"
    DANGER_LIGHT = "#FEF2F2"
    
    TEXT_PRIMARY = "#0F172A"
    TEXT_SECONDARY = "#475569"
    TEXT_MUTED = "#94A3B8"
    BORDER_LIGHT = "#E2E8F0"
    BORDER_MEDIUM = "#CBD5E1"
    BORDER_ACCENT = "#3B82F6"
    
    SHADOW_SUBTLE = "0 1px 3px rgba(0, 0, 0, 0.05)"
    SHADOW_CARD = "0 4px 15px rgba(0, 0, 0, 0.08)"
    SHADOW_ELEVATED = "0 8px 30px rgba(0, 0, 0, 0.12)"
    SHADOW_DRAMATIC = "0 20px 50px rgba(0, 0, 0, 0.15)"
    
    FONT_BRAND = ("Segoe UI", 36, "bold")
    FONT_HERO = ("Segoe UI", 28, "bold")
    FONT_HEADING = ("Segoe UI", 20, "bold")
    FONT_SUBHEADING = ("Segoe UI", 16, "normal")
    FONT_BODY = ("Segoe UI", 14, "normal")
    FONT_CAPTION = ("Segoe UI", 12, "normal")
    FONT_MICRO = ("Segoe UI", 10, "normal")
    
    SPACE_MICRO = 2
    SPACE_TINY = 4
    SPACE_XS = 8
    SPACE_SM = 12
    SPACE_MD = 16
    SPACE_LG = 24
    SPACE_XL = 32
    SPACE_2XL = 48
    SPACE_3XL = 64
    SPACE_4XL = 96
    
    RADIUS_NONE = 0
    RADIUS_TINY = 4
    RADIUS_SM = 8
    RADIUS_MD = 12
    RADIUS_LG = 16
    RADIUS_XL = 20
    RADIUS_2XL = 24
    RADIUS_FULL = 9999
    
    TRANSITION_FAST = "0.15s"
    TRANSITION_NORMAL = "0.25s"
    TRANSITION_SLOW = "0.35s"
    
    SIDEBAR_WIDTH = 280
    CARD_MIN_HEIGHT = 120
    BUTTON_HEIGHT = 44
    INPUT_HEIGHT = 48
    
    @classmethod
    def get_gradient_background(cls):
        """Get premium gradient background colors"""
        return {
            "start": cls.ICE_ULTRA_LIGHT,
            "end": cls.FROST_LIGHT
        }
    
    @classmethod
    def get_card_style(cls, elevated=False):
        """Get premium card styling"""
        return {
            "fg_color": cls.FROST_WHITE,
            "corner_radius": cls.RADIUS_LG,
            "border_width": 1,
            "border_color": cls.BORDER_LIGHT
        }
    
    @classmethod
    def get_button_style(cls, variant="primary"):
        """Get premium button styling"""
        styles = {
            "primary": {
                "fg_color": cls.ICE_PRIMARY,
                "hover_color": cls.ICE_SECONDARY,
                "text_color": "white",
                "corner_radius": cls.RADIUS_MD,
                "border_width": 0,
                "height": cls.BUTTON_HEIGHT
            },
            "secondary": {
                "fg_color": cls.FROST_WHITE,
                "hover_color": cls.ICE_LIGHT,
                "text_color": cls.ICE_PRIMARY,
                "corner_radius": cls.RADIUS_MD,
                "border_width": 2,
                "border_color": cls.ICE_PRIMARY,
                "height": cls.BUTTON_HEIGHT
            },
            "success": {
                "fg_color": cls.SNAKE_GREEN,
                "hover_color": cls.SNAKE_ACCENT,
                "text_color": "white",
                "corner_radius": cls.RADIUS_MD,
                "border_width": 0,
                "height": cls.BUTTON_HEIGHT
            }
        }
        return styles.get(variant, styles["primary"])


class IconManager:
    """
    ❄️ Premium Icon Management System
    Beautiful, scalable icons for the Caninana interface
    """
    
    ICONS = {
        "shield": "🛡️",
        "scan": "🔍",
        "protection": "🔒",
        "threat": "⚠️",
        "danger": "🚨",
        "success": "✅",
        
        "dashboard": "🏠",
        "file": "📁",
        "settings": "⚙️",
        "history": "📊",
        "quarantine": "🔒",
        "refresh": "🔄",
        
        "loading": "⏳",
        "complete": "✅",
        "error": "❌",
        "info": "ℹ️",
        
        "snake": "🐍",
        "caninana": "🐍",
        "premium": "💎",
        "secure": "🔐"
    }
    
    @classmethod
    def get(cls, icon_name, fallback=""):
        """Get icon by name with fallback"""
        return cls.ICONS.get(icon_name, fallback)
    
    @classmethod
    def create_status_config(cls, status_type):
        """Get complete status configuration with icons and colors"""
        configs = {
            "secure": {
                "icon": cls.get("shield"),
                "color": PremiumDesignSystem.SUCCESS_GREEN,
                "bg_color": PremiumDesignSystem.SUCCESS_LIGHT,
                "border_color": PremiumDesignSystem.SUCCESS_GREEN
            },
            "scanning": {
                "icon": cls.get("scan"),
                "color": PremiumDesignSystem.ICE_PRIMARY,
                "bg_color": PremiumDesignSystem.ICE_LIGHT,
                "border_color": PremiumDesignSystem.ICE_PRIMARY
            },
            "warning": {
                "icon": cls.get("threat"),
                "color": PremiumDesignSystem.WARNING_AMBER,
                "bg_color": PremiumDesignSystem.WARNING_LIGHT,
                "border_color": PremiumDesignSystem.WARNING_AMBER
            },
            "danger": {
                "icon": cls.get("danger"),
                "color": PremiumDesignSystem.DANGER_RED,
                "bg_color": PremiumDesignSystem.DANGER_LIGHT,
                "border_color": PremiumDesignSystem.DANGER_RED
            }
        }
        return configs.get(status_type, configs["secure"])


class VisualEffects:
    """
    ✨ Advanced Visual Effects System
    Glassmorphism, gradients, and premium animations
    """
    
    @staticmethod
    def create_frost_effect():
        """Create glassmorphism frost effect"""
        return {
            "fg_color": PremiumDesignSystem.FROST_WHITE,
            "corner_radius": PremiumDesignSystem.RADIUS_LG,
            "border_width": 1,
            "border_color": PremiumDesignSystem.BORDER_LIGHT
        }
    
    @staticmethod
    def create_elevated_card():
        """Create elevated card with premium shadow"""
        return {
            **PremiumDesignSystem.get_card_style(),
            "border_width": 0
        }
    
    @staticmethod
    def create_gradient_overlay():
        """Create subtle gradient overlay"""
        return {
            "fg_color": PremiumDesignSystem.FROST_LIGHT,
            "corner_radius": 0
        }