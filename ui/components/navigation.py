"""
🧭 PREMIUM NAVIGATION SYSTEM
Sophisticated sidebar with efficient space usage and premium styling
"""

import customtkinter
from .design_system import PremiumDesignSystem, IconManager
from .animated_widgets import PremiumCard
from .status_cards import PremiumStatusIndicator


class PremiumNavButton(customtkinter.CTkButton):
    """
    🎯 Premium Navigation Button
    Sophisticated navigation item with hover effects and active states
    """
    
    def __init__(self, parent, icon="", text="", active=False, **kwargs):
        self.is_active = active
        
        base_style = {
            "corner_radius": PremiumDesignSystem.RADIUS_MD,
            "height": 48,
            "anchor": "w",
            "font": customtkinter.CTkFont(size=14, weight="normal")
        }
        
        if active:
            style = {
                **base_style,
                "fg_color": PremiumDesignSystem.ICE_PRIMARY,
                "hover_color": PremiumDesignSystem.ICE_SECONDARY,
                "text_color": "white",
                "border_width": 0
            }
        else:
            style = {
                **base_style,
                "fg_color": "transparent",
                "hover_color": PremiumDesignSystem.ICE_LIGHT,
                "text_color": PremiumDesignSystem.TEXT_PRIMARY,
                "border_width": 0
            }
        
        display_text = f"{icon}  {text}" if icon else text
        
        final_style = {**style, **kwargs, "text": display_text}
        super().__init__(parent, **final_style)
        
    def set_active(self, active=True):
        """Set button active state"""
        self.is_active = active
        if active:
            self.configure(
                fg_color=PremiumDesignSystem.ICE_PRIMARY,
                hover_color=PremiumDesignSystem.ICE_SECONDARY,
                text_color="white"
            )
        else:
            self.configure(
                fg_color="transparent",
                hover_color=PremiumDesignSystem.ICE_LIGHT,
                text_color=PremiumDesignSystem.TEXT_PRIMARY
            )


class BrandHeader(customtkinter.CTkFrame):
    """
    🐍 Premium Brand Header
    Compact, elegant branding section
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            fg_color=PremiumDesignSystem.ICE_LIGHT,
            corner_radius=PremiumDesignSystem.RADIUS_LG,
            height=100
        )
        
        self.brand_container = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.brand_container.pack(
            fill="both",
            expand=True,
            padx=PremiumDesignSystem.SPACE_LG,
            pady=PremiumDesignSystem.SPACE_MD
        )
        
        self.header_row = customtkinter.CTkFrame(
            self.brand_container,
            fg_color="transparent"
        )
        self.header_row.pack(fill="x")
        
        self.logo_label = customtkinter.CTkLabel(
            self.header_row,
            text=IconManager.get("caninana"),
            font=customtkinter.CTkFont(size=32),
            text_color=PremiumDesignSystem.ICE_PRIMARY
        )
        self.logo_label.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        self.text_container = customtkinter.CTkFrame(
            self.header_row,
            fg_color="transparent"
        )
        self.text_container.pack(side="left", fill="both", expand=True)
        
        self.brand_name = customtkinter.CTkLabel(
            self.text_container,
            text="Caninana",
            font=customtkinter.CTkFont(size=22, weight="bold"),
            text_color=PremiumDesignSystem.ICE_PRIMARY,
            anchor="w"
        )
        self.brand_name.pack(anchor="w")
        
        self.brand_subtitle = customtkinter.CTkLabel(
            self.text_container,
            text="Premium Security",
            font=customtkinter.CTkFont(size=11),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        self.brand_subtitle.pack(anchor="w")


class PremiumSidebar(customtkinter.CTkFrame):
    """
    ✨ Premium Navigation Sidebar
    Sophisticated navigation with efficient space usage
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            width=PremiumDesignSystem.SIDEBAR_WIDTH,
            corner_radius=0,
            fg_color=PremiumDesignSystem.FROST_WHITE,
            border_width=1,
            border_color=PremiumDesignSystem.BORDER_LIGHT
        )
        
        self.pack_propagate(False)
        
        self.active_nav_item = None
        self.nav_buttons = {}
        
        self.create_brand_section()
        self.create_main_navigation()
        self.create_status_section()
        self.create_footer_section()
        
    def create_brand_section(self):
        """Create compact brand header"""
        self.brand_header = BrandHeader(self)
        self.brand_header.pack(
            fill="x",
            padx=PremiumDesignSystem.SPACE_MD,
            pady=(PremiumDesignSystem.SPACE_MD, PremiumDesignSystem.SPACE_LG)
        )
        
    def create_main_navigation(self):
        """Create main navigation menu"""
        self.nav_container = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.nav_container.pack(
            fill="x",
            padx=PremiumDesignSystem.SPACE_MD
        )
        
        self.nav_title = customtkinter.CTkLabel(
            self.nav_container,
            text="NAVIGATION",
            font=customtkinter.CTkFont(size=10, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_MUTED,
            anchor="w"
        )
        self.nav_title.pack(
            anchor="w",
            pady=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        nav_items = [
            ("dashboard", IconManager.get("dashboard"), "Dashboard", True),
            ("quick_scan", "⚡", "Quick Scan", False),
            ("file_scan", IconManager.get("file"), "File Scanner", False),
            ("history", IconManager.get("history"), "Scan History", False),
            ("quarantine", IconManager.get("quarantine"), "Quarantine", False),
            ("settings", IconManager.get("settings"), "Settings", False)
        ]
        
        for nav_id, icon, text, is_active in nav_items:
            btn = PremiumNavButton(
                self.nav_container,
                icon=icon,
                text=text,
                active=is_active,
                command=lambda item=nav_id: self.on_nav_click(item)
            )
            btn.pack(
                fill="x",
                pady=(0, PremiumDesignSystem.SPACE_XS)
            )
            self.nav_buttons[nav_id] = btn
            
            if is_active:
                self.active_nav_item = nav_id
                
    def create_status_section(self):
        """Create compact status indicator"""
        self.status_container = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.status_container.pack(
            fill="x",
            padx=PremiumDesignSystem.SPACE_MD,
            pady=PremiumDesignSystem.SPACE_LG
        )
        
        self.status_title = customtkinter.CTkLabel(
            self.status_container,
            text="SYSTEM STATUS",
            font=customtkinter.CTkFont(size=10, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_MUTED,
            anchor="w"
        )
        self.status_title.pack(
            anchor="w",
            pady=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        self.status_indicator = PremiumStatusIndicator(self.status_container)
        self.status_indicator.pack(fill="x")
        
        self.status_indicator.set_status(
            "secure",
            "Protection Active",
            "Real-time monitoring enabled"
        )
        
    def create_footer_section(self):
        """Create compact footer with essential info"""
        self.footer_container = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.footer_container.pack(
            side="bottom",
            fill="x",
            padx=PremiumDesignSystem.SPACE_MD,
            pady=PremiumDesignSystem.SPACE_MD
        )
        
        self.version_label = customtkinter.CTkLabel(
            self.footer_container,
            text="Version 3.0.0",
            font=customtkinter.CTkFont(size=10),
            text_color=PremiumDesignSystem.TEXT_MUTED,
            anchor="w"
        )
        self.version_label.pack(anchor="w")
        
        self.update_label = customtkinter.CTkLabel(
            self.footer_container,
            text="Signatures updated today",
            font=customtkinter.CTkFont(size=9),
            text_color=PremiumDesignSystem.TEXT_MUTED,
            anchor="w"
        )
        self.update_label.pack(anchor="w", pady=(2, 0))
        
    def on_nav_click(self, nav_item):
        """Handle navigation item click"""
        if self.active_nav_item and self.active_nav_item in self.nav_buttons:
            self.nav_buttons[self.active_nav_item].set_active(False)
            
        if nav_item in self.nav_buttons:
            self.nav_buttons[nav_item].set_active(True)
            self.active_nav_item = nav_item
            
        if hasattr(self, 'navigation_callback'):
            self.navigation_callback(nav_item)
            
    def set_navigation_callback(self, callback):
        """Set callback for navigation events"""
        self.navigation_callback = callback
        
    def update_status(self, status_type, title, detail=""):
        """Update sidebar status indicator"""
        self.status_indicator.set_status(status_type, title, detail)