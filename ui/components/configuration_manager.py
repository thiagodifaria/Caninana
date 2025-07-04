"""
⚙️ CONFIGURATION MANAGER
Premium settings interface with organized categories and real-time updates
"""

import customtkinter
import json
import os
from .design_system import PremiumDesignSystem, IconManager
from .animated_widgets import PremiumCard
from .status_cards import PremiumStatusCard


class SettingCard(PremiumCard):
    """
    🎛️ Individual Setting Card
    Beautiful card for each configuration option
    """
    
    def __init__(self, parent, title="", description="", setting_type="toggle", **kwargs):
        super().__init__(parent, elevated=False, **kwargs)
        
        self.setting_type = setting_type
        self.value_callback = None
        
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
        
        self.text_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.text_frame.pack(side="left", fill="both", expand=True)
        
        self.title_label = customtkinter.CTkLabel(
            self.text_frame,
            text=title,
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.title_label.pack(anchor="w")
        
        if description:
            self.desc_label = customtkinter.CTkLabel(
                self.text_frame,
                text=description,
                font=customtkinter.CTkFont(size=11),
                text_color=PremiumDesignSystem.TEXT_SECONDARY,
                anchor="w",
                wraplength=300
            )
            self.desc_label.pack(anchor="w", pady=(2, 0))
        
        self.control_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.control_frame.pack(side="right", padx=(PremiumDesignSystem.SPACE_MD, 0))
        
        self.create_control()
        
    def create_control(self):
        """Create control based on setting type"""
        if self.setting_type == "toggle":
            self.control = customtkinter.CTkSwitch(
                self.control_frame,
                text="",
                command=self.on_value_change,
                button_color=PremiumDesignSystem.ICE_PRIMARY,
                progress_color=PremiumDesignSystem.SUCCESS_GREEN
            )
            self.control.pack()
            
        elif self.setting_type == "dropdown":
            self.control = customtkinter.CTkOptionMenu(
                self.control_frame,
                values=["Option 1", "Option 2", "Option 3"],
                command=self.on_value_change,
                fg_color=PremiumDesignSystem.ICE_PRIMARY,
                button_color=PremiumDesignSystem.ICE_SECONDARY,
                button_hover_color=PremiumDesignSystem.ICE_ACCENT
            )
            self.control.pack()
            
        elif self.setting_type == "slider":
            self.control = customtkinter.CTkSlider(
                self.control_frame,
                from_=0,
                to=100,
                command=self.on_value_change,
                button_color=PremiumDesignSystem.ICE_PRIMARY,
                progress_color=PremiumDesignSystem.ICE_SECONDARY
            )
            self.control.pack()
            
        elif self.setting_type == "entry":
            self.control = customtkinter.CTkEntry(
                self.control_frame,
                width=150,
                font=customtkinter.CTkFont(size=12),
                corner_radius=PremiumDesignSystem.RADIUS_SM
            )
            self.control.pack()
            self.control.bind("<KeyRelease>", lambda e: self.on_value_change())
    
    def on_value_change(self, value=None):
        """Handle value change"""
        if self.value_callback:
            current_value = self.get_value()
            self.value_callback(current_value)
    
    def get_value(self):
        """Get current control value"""
        if self.setting_type == "toggle":
            return self.control.get() == 1
        elif self.setting_type == "dropdown":
            return self.control.get()
        elif self.setting_type == "slider":
            return self.control.get()
        elif self.setting_type == "entry":
            return self.control.get()
        return None
    
    def set_value(self, value):
        """Set control value"""
        if self.setting_type == "toggle":
            self.control.select() if value else self.control.deselect()
        elif self.setting_type == "dropdown":
            self.control.set(value)
        elif self.setting_type == "slider":
            self.control.set(value)
        elif self.setting_type == "entry":
            self.control.delete(0, "end")
            self.control.insert(0, str(value))
    
    def set_value_callback(self, callback):
        """Set callback for value changes"""
        self.value_callback = callback


class SettingsCategory(customtkinter.CTkFrame):
    """
    📁 Settings Category Section
    Organized group of related settings
    """
    
    def __init__(self, parent, title="", icon="", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            fg_color="transparent"
        )
        
        self.header_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent",
            height=50
        )
        self.header_frame.pack(
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_MD)
        )
        self.header_frame.pack_propagate(False)
        
        if icon:
            self.icon_label = customtkinter.CTkLabel(
                self.header_frame,
                text=icon,
                font=customtkinter.CTkFont(size=20),
                text_color=PremiumDesignSystem.ICE_PRIMARY
            )
            self.icon_label.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        self.title_label = customtkinter.CTkLabel(
            self.header_frame,
            text=title,
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.title_label.pack(side="left")
        
        self.settings_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.settings_frame.pack(fill="x")
        
    def add_setting(self, setting_card):
        """Add setting card to category"""
        setting_card.pack(
            in_=self.settings_frame,
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_SM)
        )


class ConfigurationManager(customtkinter.CTkFrame):
    """
    ⚙️ Premium Configuration Manager
    Comprehensive settings interface with beautiful organization
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        self.config_data = {}
        self.config_file = "caninana_config.json"
        
        self.grid_columnconfigure(0, weight=1)
        
        self.create_header()
        self.create_settings_content()
        self.create_footer()
        
        self.load_configuration()
        
    def create_header(self):
        """Create settings header"""
        header_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent",
            height=80
        )
        header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        header_frame.grid_propagate(False)
        
        title_label = customtkinter.CTkLabel(
            header_frame,
            text="⚙️ Settings",
            font=customtkinter.CTkFont(size=24, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(PremiumDesignSystem.SPACE_MD, 4))
        
        subtitle_label = customtkinter.CTkLabel(
            header_frame,
            text="Configure Caninana's security features and preferences",
            font=customtkinter.CTkFont(size=14),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        subtitle_label.pack(anchor="w")
        
    def create_settings_content(self):
        """Create scrollable settings content"""
        self.settings_scroll = customtkinter.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.settings_scroll.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        self.grid_rowconfigure(1, weight=1)
        
        self.create_protection_settings()
        self.create_scan_settings()
        self.create_interface_settings()
        self.create_advanced_settings()
        
    def create_protection_settings(self):
        """Create protection settings category"""
        protection_category = SettingsCategory(
            self.settings_scroll,
            title="Protection Settings",
            icon=IconManager.get("shield")
        )
        protection_category.pack(
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
        realtime_card = SettingCard(
            protection_category,
            title="Real-time Protection",
            description="Monitor system files and processes in real-time",
            setting_type="toggle"
        )
        realtime_card.set_value_callback(lambda v: self.update_config("realtime_protection", v))
        protection_category.add_setting(realtime_card)
        
        downloads_card = SettingCard(
            protection_category,
            title="Scan Downloads",
            description="Automatically scan downloaded files for threats",
            setting_type="toggle"
        )
        downloads_card.set_value_callback(lambda v: self.update_config("scan_downloads", v))
        protection_category.add_setting(downloads_card)
        
        email_card = SettingCard(
            protection_category,
            title="Email Protection",
            description="Scan email attachments and links",
            setting_type="toggle"
        )
        email_card.set_value_callback(lambda v: self.update_config("email_protection", v))
        protection_category.add_setting(email_card)
        
    def create_scan_settings(self):
        """Create scan settings category"""
        scan_category = SettingsCategory(
            self.settings_scroll,
            title="Scan Settings",
            icon=IconManager.get("scan")
        )
        scan_category.pack(
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
        sensitivity_card = SettingCard(
            scan_category,
            title="Scan Sensitivity",
            description="Adjust the sensitivity of threat detection",
            setting_type="dropdown"
        )
        sensitivity_card.control.configure(values=["Low", "Medium", "High", "Maximum"])
        sensitivity_card.set_value_callback(lambda v: self.update_config("scan_sensitivity", v))
        scan_category.add_setting(sensitivity_card)
        
        archive_card = SettingCard(
            scan_category,
            title="Scan Archives",
            description="Extract and scan compressed files and archives",
            setting_type="toggle"
        )
        archive_card.set_value_callback(lambda v: self.update_config("scan_archives", v))
        scan_category.add_setting(archive_card)
        
        timeout_card = SettingCard(
            scan_category,
            title="Scan Timeout (minutes)",
            description="Maximum time to spend scanning a single file",
            setting_type="entry"
        )
        timeout_card.set_value_callback(lambda v: self.update_config("scan_timeout", v))
        scan_category.add_setting(timeout_card)
        
    def create_interface_settings(self):
        """Create interface settings category"""
        interface_category = SettingsCategory(
            self.settings_scroll,
            title="Interface Settings",
            icon="🎨"
        )
        interface_category.pack(
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
        notifications_card = SettingCard(
            interface_category,
            title="Show Notifications",
            description="Display system notifications for scan results",
            setting_type="toggle"
        )
        notifications_card.set_value_callback(lambda v: self.update_config("show_notifications", v))
        interface_category.add_setting(notifications_card)
        
        autostart_card = SettingCard(
            interface_category,
            title="Start with Windows",
            description="Launch Caninana automatically when Windows starts",
            setting_type="toggle"
        )
        autostart_card.set_value_callback(lambda v: self.update_config("auto_start", v))
        interface_category.add_setting(autostart_card)
        
        theme_card = SettingCard(
            interface_category,
            title="Interface Theme",
            description="Choose the visual theme for the application",
            setting_type="dropdown"
        )
        theme_card.control.configure(values=["Light", "Dark", "Auto"])
        theme_card.set_value_callback(lambda v: self.update_config("theme", v))
        interface_category.add_setting(theme_card)
        
    def create_advanced_settings(self):
        """Create advanced settings category"""
        advanced_category = SettingsCategory(
            self.settings_scroll,
            title="Advanced Settings",
            icon="🔧"
        )
        advanced_category.pack(
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
        cloud_card = SettingCard(
            advanced_category,
            title="Cloud Lookup",
            description="Use cloud services for enhanced threat detection",
            setting_type="toggle"
        )
        cloud_card.set_value_callback(lambda v: self.update_config("cloud_lookup", v))
        advanced_category.add_setting(cloud_card)
        
        debug_card = SettingCard(
            advanced_category,
            title="Debug Logging",
            description="Enable detailed logging for troubleshooting",
            setting_type="toggle"
        )
        debug_card.set_value_callback(lambda v: self.update_config("debug_logging", v))
        advanced_category.add_setting(debug_card)
        
        update_card = SettingCard(
            advanced_category,
            title="Update Check Frequency",
            description="How often to check for signature updates",
            setting_type="dropdown"
        )
        update_card.control.configure(values=["Every Hour", "Daily", "Weekly", "Manual"])
        update_card.set_value_callback(lambda v: self.update_config("update_frequency", v))
        advanced_category.add_setting(update_card)
        
    def create_footer(self):
        """Create settings footer with actions"""
        footer_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent",
            height=60
        )
        footer_frame.grid(
            row=2,
            column=0,
            sticky="ew"
        )
        footer_frame.grid_propagate(False)
        
        button_frame = customtkinter.CTkFrame(
            footer_frame,
            fg_color="transparent"
        )
        button_frame.pack(pady=PremiumDesignSystem.SPACE_MD)
        
        save_button = customtkinter.CTkButton(
            button_frame,
            text="💾 Save Settings",
            command=self.save_configuration,
            **PremiumDesignSystem.get_button_style("success")
        )
        save_button.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        reset_button = customtkinter.CTkButton(
            button_frame,
            text="🔄 Reset to Defaults",
            command=self.reset_to_defaults,
            **PremiumDesignSystem.get_button_style("secondary")
        )
        reset_button.pack(side="left")
        
    def update_config(self, key, value):
        """Update configuration value"""
        self.config_data[key] = value
        
    def load_configuration(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config_data = json.load(f)
            else:
                self.config_data = self.get_default_config()
        except Exception as e:
            print(f"Error loading configuration: {e}")
            self.config_data = self.get_default_config()
            
    def save_configuration(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config_data, f, indent=2)
            print("Configuration saved successfully")
        except Exception as e:
            print(f"Error saving configuration: {e}")
            
    def get_default_config(self):
        """Get default configuration values"""
        return {
            "realtime_protection": True,
            "scan_downloads": True,
            "email_protection": True,
            "scan_sensitivity": "Medium",
            "scan_archives": True,
            "scan_timeout": "5",
            "show_notifications": True,
            "auto_start": False,
            "theme": "Light",
            "cloud_lookup": True,
            "debug_logging": False,
            "update_frequency": "Daily"
        }
        
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.config_data = self.get_default_config()
        print("Settings reset to defaults")
        
    def get_config(self, key, default=None):
        """Get configuration value"""
        return self.config_data.get(key, default)
        
    def set_config(self, key, value):
        """Set configuration value"""
        self.config_data[key] = value