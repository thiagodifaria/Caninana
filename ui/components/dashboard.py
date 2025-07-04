"""
🏠 PREMIUM DASHBOARD
Beautiful main dashboard with sophisticated layout and visual hierarchy
"""

import customtkinter
from .design_system import PremiumDesignSystem, IconManager
from .status_cards import PremiumStatusCard, QuickActionCard, ActivityItem, StatsCard
from .animated_widgets import PremiumCard


class DashboardHeader(customtkinter.CTkFrame):
    """
    ✨ Premium Dashboard Header
    Beautiful header with welcome message and contextual information
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            fg_color="transparent",
            height=80
        )
        
        self.content_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(
            fill="both",
            expand=True,
            pady=PremiumDesignSystem.SPACE_MD
        )
        
        self.title_label = customtkinter.CTkLabel(
            self.content_frame,
            text="Security Dashboard",
            font=customtkinter.CTkFont(size=28, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.title_label.pack(anchor="w")
        
        self.subtitle_label = customtkinter.CTkLabel(
            self.content_frame,
            text="Your system is protected by Caninana's advanced threat detection engine",
            font=customtkinter.CTkFont(size=14),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        self.subtitle_label.pack(anchor="w", pady=(4, 0))


class QuickStatsGrid(customtkinter.CTkFrame):
    """
    📊 Quick Statistics Grid
    Beautiful stats overview with key security metrics
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        stats_data = [
            ("Files Scanned", "2,847", "Today", "↑ 12%"),
            ("Threats Blocked", "0", "This week", ""),
            ("Last Scan", "2h ago", "Quick scan", "✅"),
            ("Protection", "Active", "Real-time", "🛡️")
        ]
        
        for i, (title, value, subtitle, trend) in enumerate(stats_data):
            card = StatsCard(
                self,
                title=title,
                value=value,
                subtitle=subtitle,
                trend=trend
            )
            card.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=(0 if i == 0 else PremiumDesignSystem.SPACE_SM, 0)
            )


class QuickActionsGrid(customtkinter.CTkFrame):
    """
    🎯 Quick Actions Grid
    Premium action cards for main functions
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        self.grid_columnconfigure((0, 1), weight=1)
        
        self.action_commands = {}
        
        self.create_action_cards()
        
    def create_action_cards(self):
        """Create premium action cards"""
        
        self.quick_scan_card = QuickActionCard(
            self,
            icon="⚡",
            title="Quick Scan",
            description="Fast security check of critical system areas and running processes",
            action_text="Start Scan",
            command=lambda: self.execute_action("quick_scan")
        )
        self.quick_scan_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        self.file_scan_card = QuickActionCard(
            self,
            icon=IconManager.get("file"),
            title="File Scanner",
            description="Scan individual files, folders, or archives for malware and threats",
            action_text="Select File",
            command=lambda: self.execute_action("file_scan")
        )
        self.file_scan_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(PremiumDesignSystem.SPACE_SM, 0)
        )
        
    def execute_action(self, action_name):
        """Execute action command if available"""
        if action_name in self.action_commands:
            self.action_commands[action_name]()
            
    def set_action_command(self, action_name, command):
        """Set command for specific action"""
        self.action_commands[action_name] = command


class RecentActivityPanel(PremiumCard):
    """
    📋 Recent Activity Panel
    Beautiful activity log with timeline styling
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, elevated=False, **kwargs)
        
        self.header_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent",
            height=50
        )
        self.header_frame.pack(
            fill="x",
            padx=PremiumDesignSystem.SPACE_LG,
            pady=(PremiumDesignSystem.SPACE_LG, 0)
        )
        self.header_frame.pack_propagate(False)
        
        self.title_label = customtkinter.CTkLabel(
            self.header_frame,
            text="Recent Activity",
            font=customtkinter.CTkFont(size=16, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.title_label.pack(side="left", pady=PremiumDesignSystem.SPACE_MD)
        
        button_style = PremiumDesignSystem.get_button_style("secondary")
        self.view_all_btn = customtkinter.CTkButton(
            self.header_frame,
            text="View All",
            font=customtkinter.CTkFont(size=12),
            width=80,
            height=28,
            fg_color=button_style["fg_color"],
            hover_color=button_style["hover_color"],
            text_color=button_style["text_color"],
            corner_radius=button_style["corner_radius"],
            border_width=button_style["border_width"],
            border_color=button_style["border_color"]
        )
        self.view_all_btn.pack(side="right", pady=PremiumDesignSystem.SPACE_MD)
        
        self.activity_container = customtkinter.CTkScrollableFrame(
            self,
            fg_color="transparent",
            height=200
        )
        self.activity_container.pack(
            fill="both",
            expand=True,
            padx=PremiumDesignSystem.SPACE_LG,
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
        self.populate_activities()
        
    def populate_activities(self):
        """Add sample activity items"""
        activities = [
            (
                IconManager.get("success"),
                "System scan completed",
                "Full system scan found no threats • 2,847 files checked",
                "2 hours ago"
            ),
            (
                IconManager.get("refresh"),
                "Threat signatures updated",
                "Latest malware definitions applied • 15,243 new signatures",
                "4 hours ago"
            ),
            (
                IconManager.get("shield"),
                "Real-time protection active",
                "Continuous monitoring of system files and processes",
                "Ongoing"
            ),
            (
                IconManager.get("file"),
                "Suspicious file quarantined",
                "Potential threat isolated and moved to secure quarantine",
                "Yesterday"
            ),
            (
                IconManager.get("settings"),
                "Security settings updated",
                "Enhanced protection rules applied to email attachments",
                "2 days ago"
            )
        ]
        
        for icon, title, description, timestamp in activities:
            activity_item = ActivityItem(
                self.activity_container,
                icon=icon,
                title=title,
                description=description,
                timestamp=timestamp
            )
            activity_item.pack(fill="x", pady=(0, PremiumDesignSystem.SPACE_XS))


class PremiumDashboard(customtkinter.CTkFrame):
    """
    🏠 Premium Main Dashboard
    Sophisticated layout with beautiful components and proper spacing
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        
        self.create_header()
        self.create_system_status()
        self.create_stats_section()
        self.create_actions_section()
        self.create_activity_section()
        
    def create_header(self):
        """Create dashboard header"""
        self.header = DashboardHeader(self)
        self.header.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
    def create_system_status(self):
        """Create main system status card"""
        self.system_status = PremiumStatusCard(self)
        self.system_status.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
        self.system_status.set_status(
            "secure",
            "System Protected",
            "All security systems operational • Real-time protection active • Last scan: Today"
        )
        
    def create_stats_section(self):
        """Create statistics overview"""
        self.stats_grid = QuickStatsGrid(self)
        self.stats_grid.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
    def create_actions_section(self):
        """Create quick actions section"""
        self.actions_title = customtkinter.CTkLabel(
            self,
            text="Quick Actions",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.actions_title.grid(
            row=3,
            column=0,
            sticky="w",
            pady=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        self.actions_grid = QuickActionsGrid(self)
        self.actions_grid.grid(
            row=4,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
    def create_activity_section(self):
        """Create activity section"""
        self.activity_panel = RecentActivityPanel(self)
        self.activity_panel.grid(
            row=5,
            column=0,
            sticky="ew"
        )
        
    def set_action_commands(self, commands_dict):
        """Set commands for quick actions"""
        for action, command in commands_dict.items():
            self.actions_grid.set_action_command(action, command)
            
    def update_system_status(self, status_type, title, detail=""):
        """Update main system status"""
        self.system_status.set_status(status_type, title, detail)