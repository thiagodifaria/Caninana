"""
💎 PREMIUM STATUS CARDS
Beautiful status displays with advanced visual effects
"""

import customtkinter
from .design_system import PremiumDesignSystem, IconManager
from .animated_widgets import PremiumCard


class PremiumStatusCard(PremiumCard):
    """
    ✨ Premium Status Card with Rich Visual Feedback
    Advanced status display with icons, animations, and beautiful typography
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, elevated=True, hoverable=False, **kwargs)
        
        self.configure(height=100)
        
        self.content_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(
            fill="both", 
            expand=True, 
            padx=PremiumDesignSystem.SPACE_LG,
            pady=PremiumDesignSystem.SPACE_MD
        )
        
        self.icon_container = customtkinter.CTkFrame(
            self.content_frame,
            width=60,
            height=60,
            corner_radius=30,
            fg_color=PremiumDesignSystem.ICE_LIGHT
        )
        self.icon_container.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_MD))
        self.icon_container.pack_propagate(False)
        
        self.status_icon = customtkinter.CTkLabel(
            self.icon_container,
            text=IconManager.get("shield"),
            font=customtkinter.CTkFont(size=28),
            text_color=PremiumDesignSystem.SUCCESS_GREEN
        )
        self.status_icon.pack(expand=True)
        
        self.text_container = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.text_container.pack(side="left", fill="both", expand=True)
        
        self.title_label = customtkinter.CTkLabel(
            self.text_container,
            text="System Protected",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.title_label.pack(anchor="w", pady=(8, 2))
        
        self.detail_label = customtkinter.CTkLabel(
            self.text_container,
            text="All systems operational • Real-time protection active",
            font=customtkinter.CTkFont(size=13),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        self.detail_label.pack(anchor="w")
        
        self.status_bar = customtkinter.CTkFrame(
            self,
            height=4,
            corner_radius=2,
            fg_color=PremiumDesignSystem.SUCCESS_GREEN
        )
        self.status_bar.pack(
            side="bottom", 
            fill="x", 
            padx=PremiumDesignSystem.SPACE_LG,
            pady=(0, PremiumDesignSystem.SPACE_TINY)
        )
        
    def set_status(self, status_type, title, detail=""):
        """Update status with beautiful transitions"""
        config = IconManager.create_status_config(status_type)
        
        self.status_icon.configure(
            text=config["icon"],
            text_color=config["color"]
        )
        
        self.icon_container.configure(fg_color=config["bg_color"])
        
        self.title_label.configure(
            text=title,
            text_color=config["color"]
        )
        self.detail_label.configure(text=detail)
        
        self.status_bar.configure(fg_color=config["color"])
        
        self.configure(border_color=config["border_color"], border_width=2)


class QuickActionCard(PremiumCard):
    """
    🎯 Premium Quick Action Card
    Beautiful action card with hover effects and clear call-to-action
    """
    
    def __init__(self, parent, icon="", title="", description="", action_text="", command=None, **kwargs):
        super().__init__(parent, elevated=False, hoverable=True, **kwargs)
        
        self.configure(height=180)
        self.action_command = command
        
        self.content_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=PremiumDesignSystem.SPACE_LG,
            pady=PremiumDesignSystem.SPACE_LG
        )
        
        self.icon_label = customtkinter.CTkLabel(
            self.content_frame,
            text=icon,
            font=customtkinter.CTkFont(size=36),
            text_color=PremiumDesignSystem.ICE_PRIMARY
        )
        self.icon_label.pack(pady=(0, PremiumDesignSystem.SPACE_MD))
        
        self.title_label = customtkinter.CTkLabel(
            self.content_frame,
            text=title,
            font=customtkinter.CTkFont(size=16, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY
        )
        self.title_label.pack(pady=(0, PremiumDesignSystem.SPACE_XS))
        
        self.desc_label = customtkinter.CTkLabel(
            self.content_frame,
            text=description,
            font=customtkinter.CTkFont(size=12),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            wraplength=200,
            justify="center"
        )
        self.desc_label.pack(pady=(0, PremiumDesignSystem.SPACE_MD))
        
        if action_text and command:
            self.action_button = customtkinter.CTkButton(
                self.content_frame,
                text=action_text,
                command=command,
                **PremiumDesignSystem.get_button_style("primary"),
                width=140
            )
            self.action_button.pack()


class ActivityItem(customtkinter.CTkFrame):
    """
    📋 Premium Activity Item
    Beautiful activity log item with timeline styling
    """
    
    def __init__(self, parent, icon="", title="", description="", timestamp="", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.configure(height=60)
        
        self.container = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.container.pack(
            fill="both",
            expand=True,
            padx=PremiumDesignSystem.SPACE_MD,
            pady=PremiumDesignSystem.SPACE_XS
        )
        
        self.icon_frame = customtkinter.CTkFrame(
            self.container,
            width=40,
            height=40,
            corner_radius=20,
            fg_color=PremiumDesignSystem.ICE_LIGHT
        )
        self.icon_frame.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_MD))
        self.icon_frame.pack_propagate(False)
        
        self.icon_label = customtkinter.CTkLabel(
            self.icon_frame,
            text=icon,
            font=customtkinter.CTkFont(size=16),
            text_color=PremiumDesignSystem.ICE_PRIMARY
        )
        self.icon_label.pack(expand=True)
        
        self.content_area = customtkinter.CTkFrame(
            self.container,
            fg_color="transparent"
        )
        self.content_area.pack(side="left", fill="both", expand=True)
        
        self.title_label = customtkinter.CTkLabel(
            self.content_area,
            text=title,
            font=customtkinter.CTkFont(size=13, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.title_label.pack(anchor="w", fill="x")
        
        self.desc_label = customtkinter.CTkLabel(
            self.content_area,
            text=description,
            font=customtkinter.CTkFont(size=11),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        self.desc_label.pack(anchor="w", fill="x")
        
        if timestamp:
            self.time_label = customtkinter.CTkLabel(
                self.container,
                text=timestamp,
                font=customtkinter.CTkFont(size=10),
                text_color=PremiumDesignSystem.TEXT_MUTED
            )
            self.time_label.pack(side="right", padx=(PremiumDesignSystem.SPACE_SM, 0))


class PremiumStatusIndicator(customtkinter.CTkFrame):
    """
    💎 Premium Status Indicator with Pulse Animation
    Beautiful status display with smooth state transitions
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            **PremiumDesignSystem.get_card_style(),
            height=60
        )
        
        self.current_status = "secure"
        self.pulse_animation = False
        
        self.content_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=16, pady=12)
        
        self.status_dot = customtkinter.CTkFrame(
            self.content_frame,
            width=12,
            height=12,
            corner_radius=6,
            fg_color=PremiumDesignSystem.SUCCESS_GREEN
        )
        self.status_dot.pack(side="left", padx=(0, 12))
        
        self.text_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.text_frame.pack(side="left", fill="both", expand=True)
        
        self.status_label = customtkinter.CTkLabel(
            self.text_frame,
            text="System Protected",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.status_label.pack(anchor="w")
        
        self.detail_label = customtkinter.CTkLabel(
            self.text_frame,
            text="All systems operational",
            font=customtkinter.CTkFont(size=11),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        self.detail_label.pack(anchor="w")
        
    def set_status(self, status_type, title, detail=""):
        """Update status with smooth animation"""
        config = IconManager.create_status_config(status_type)
        
        self.status_dot.configure(fg_color=config["color"])
        self.status_label.configure(
            text=title,
            text_color=config["color"]
        )
        self.detail_label.configure(text=detail)
        
        self.configure(border_color=config["color"], border_width=1)
        
        self.current_status = status_type
        
        if status_type == "scanning":
            self.start_pulse()
        else:
            self.stop_pulse()
    
    def start_pulse(self):
        """Start pulsing animation"""
        if self.pulse_animation:
            return
        self.pulse_animation = True
        self.pulse_dot()
        
    def pulse_dot(self):
        """Animate status dot pulsing"""
        if not self.pulse_animation:
            return
        
        import time
        import math
        current_time = time.time()
        pulse_factor = (math.sin(current_time * 3) + 1) / 2
        
        if self.current_status == "scanning":
            base_color = PremiumDesignSystem.ICE_PRIMARY
            self.status_dot.configure(
                fg_color=base_color if pulse_factor > 0.5 else PremiumDesignSystem.ICE_LIGHT
            )
        
        self.after(100, self.pulse_dot)
        
    def stop_pulse(self):
        """Stop pulsing animation"""
        self.pulse_animation = False


class StatsCard(PremiumCard):
    """
    📊 Premium Statistics Card
    Beautiful stats display with large numbers and context
    """
    
    def __init__(self, parent, title="", value="", subtitle="", trend="", **kwargs):
        super().__init__(parent, elevated=False, **kwargs)
        
        self.configure(height=120)
        
        self.content_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=PremiumDesignSystem.SPACE_LG,
            pady=PremiumDesignSystem.SPACE_MD
        )
        
        self.title_label = customtkinter.CTkLabel(
            self.content_frame,
            text=title,
            font=customtkinter.CTkFont(size=12, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        self.title_label.pack(anchor="w", pady=(0, PremiumDesignSystem.SPACE_XS))
        
        self.value_label = customtkinter.CTkLabel(
            self.content_frame,
            text=value,
            font=customtkinter.CTkFont(size=24, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.value_label.pack(anchor="w", pady=(0, PremiumDesignSystem.SPACE_XS))
        
        self.bottom_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.bottom_frame.pack(anchor="w", fill="x")
        
        if subtitle:
            self.subtitle_label = customtkinter.CTkLabel(
                self.bottom_frame,
                text=subtitle,
                font=customtkinter.CTkFont(size=11),
                text_color=PremiumDesignSystem.TEXT_SECONDARY,
                anchor="w"
            )
            self.subtitle_label.pack(side="left")
        
        if trend:
            trend_color = PremiumDesignSystem.SUCCESS_GREEN if "↑" in trend else PremiumDesignSystem.DANGER_RED
            self.trend_label = customtkinter.CTkLabel(
                self.bottom_frame,
                text=trend,
                font=customtkinter.CTkFont(size=11, weight="bold"),
                text_color=trend_color,
                anchor="e"
            )
            self.trend_label.pack(side="right")
    
    def update_value(self, new_value, trend=None):
        """Update the stats value with optional trend"""
        self.value_label.configure(text=new_value)
        if trend and hasattr(self, 'trend_label'):
            trend_color = PremiumDesignSystem.SUCCESS_GREEN if "↑" in trend else PremiumDesignSystem.DANGER_RED
            self.trend_label.configure(text=trend, text_color=trend_color)