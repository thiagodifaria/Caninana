"""
📝 LOG ANALYZER
Advanced log analysis and system monitoring with beautiful visualizations
"""

import customtkinter
import json
import os
from datetime import datetime, timedelta
from .design_system import PremiumDesignSystem, IconManager
from .animated_widgets import PremiumCard
from .status_cards import StatsCard


class LogLevel:
    """Log level constants"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEntry:
    """Individual log entry"""
    
    def __init__(self, timestamp, level, message, component="System", details=None):
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.component = component
        self.details = details or {}
        
    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "message": self.message,
            "component": self.component,
            "details": self.details
        }
    
    @classmethod
    def from_dict(cls, data):
        timestamp = datetime.fromisoformat(data["timestamp"])
        return cls(
            timestamp,
            data["level"],
            data["message"],
            data.get("component", "System"),
            data.get("details", {})
        )


class LogViewer(PremiumCard):
    """
    📜 Premium Log Viewer
    Beautiful log display with syntax highlighting and filtering
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, elevated=True, **kwargs)
        
        self.log_entries = []
        self.filtered_entries = []
        
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
        
        self.create_log_header()
        self.create_log_display()
        
    def create_log_header(self):
        """Create log viewer header with controls"""
        header_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent",
            height=40
        )
        header_frame.pack(
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_MD)
        )
        header_frame.pack_propagate(False)
        
        title_label = customtkinter.CTkLabel(
            header_frame,
            text="System Logs",
            font=customtkinter.CTkFont(size=16, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        title_label.pack(side="left")
        
        self.level_filter = customtkinter.CTkOptionMenu(
            header_frame,
            values=["All Levels", "INFO", "WARNING", "ERROR", "CRITICAL"],
            command=self.apply_level_filter,
            width=120,
            fg_color=PremiumDesignSystem.ICE_PRIMARY,
            button_color=PremiumDesignSystem.ICE_SECONDARY
        )
        self.level_filter.pack(side="right", padx=(PremiumDesignSystem.SPACE_SM, 0))
        
        self.auto_scroll = customtkinter.CTkSwitch(
            header_frame,
            text="Auto-scroll",
            font=customtkinter.CTkFont(size=11),
            button_color=PremiumDesignSystem.ICE_PRIMARY,
            progress_color=PremiumDesignSystem.SUCCESS_GREEN
        )
        self.auto_scroll.pack(side="right", padx=(PremiumDesignSystem.SPACE_SM, 0))
        self.auto_scroll.select()
        
    def create_log_display(self):
        """Create scrollable log display"""
        self.log_frame = customtkinter.CTkScrollableFrame(
            self.content_frame,
            fg_color=PremiumDesignSystem.FROST_LIGHT,
            corner_radius=PremiumDesignSystem.RADIUS_SM
        )
        self.log_frame.pack(fill="both", expand=True)
        
        self.load_sample_logs()
        self.apply_level_filter()
        
    def load_sample_logs(self):
        """Load sample log entries"""
        now = datetime.now()
        
        sample_logs = [
            LogEntry(now - timedelta(minutes=1), LogLevel.INFO, "System scan completed successfully", "Scanner"),
            LogEntry(now - timedelta(minutes=3), LogLevel.WARNING, "Suspicious file detected in downloads", "RealTime"),
            LogEntry(now - timedelta(minutes=5), LogLevel.INFO, "Virus definitions updated", "Updater"),
            LogEntry(now - timedelta(minutes=8), LogLevel.ERROR, "Failed to connect to cloud service", "CloudLookup"),
            LogEntry(now - timedelta(minutes=12), LogLevel.INFO, "File quarantined successfully", "Quarantine"),
            LogEntry(now - timedelta(minutes=15), LogLevel.CRITICAL, "Multiple threats detected in system", "Scanner"),
            LogEntry(now - timedelta(minutes=20), LogLevel.INFO, "Real-time protection enabled", "Protection"),
            LogEntry(now - timedelta(minutes=25), LogLevel.WARNING, "High CPU usage detected", "Monitor"),
            LogEntry(now - timedelta(minutes=30), LogLevel.INFO, "Configuration saved", "Settings"),
            LogEntry(now - timedelta(minutes=35), LogLevel.DEBUG, "Debug logging enabled", "System")
        ]
        
        self.log_entries = sample_logs
        
    def apply_level_filter(self, selected_level=None):
        """Apply log level filter"""
        if selected_level == "All Levels" or selected_level is None:
            self.filtered_entries = self.log_entries.copy()
        else:
            self.filtered_entries = [
                entry for entry in self.log_entries 
                if entry.level == selected_level
            ]
            
        self.refresh_log_display()
        
    def refresh_log_display(self):
        """Refresh the log display"""
        for widget in self.log_frame.winfo_children():
            widget.destroy()
            
        for entry in reversed(self.filtered_entries):
            log_item = LogItem(self.log_frame, entry)
            log_item.pack(
                fill="x",
                pady=(0, PremiumDesignSystem.SPACE_TINY),
                padx=PremiumDesignSystem.SPACE_SM
            )
            
        if self.auto_scroll.get():
            self.log_frame._parent_canvas.yview_moveto(1.0)
            
    def add_log_entry(self, entry):
        """Add new log entry"""
        self.log_entries.append(entry)
        self.apply_level_filter(self.level_filter.get())


class LogItem(customtkinter.CTkFrame):
    """
    📄 Individual Log Item
    Beautiful display for single log entry with level-based styling
    """
    
    def __init__(self, parent, log_entry, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.log_entry = log_entry
        
        level_config = self.get_level_config()
        
        self.configure(
            fg_color=level_config["bg_color"],
            corner_radius=PremiumDesignSystem.RADIUS_SM,
            border_width=1,
            border_color=level_config["border_color"],
            height=60
        )
        
        content_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        content_frame.pack(
            fill="both",
            expand=True,
            padx=PremiumDesignSystem.SPACE_SM,
            pady=PremiumDesignSystem.SPACE_XS
        )
        
        top_row = customtkinter.CTkFrame(
            content_frame,
            fg_color="transparent"
        )
        top_row.pack(fill="x")
        
        timestamp_label = customtkinter.CTkLabel(
            top_row,
            text=log_entry.timestamp.strftime("%H:%M:%S"),
            font=customtkinter.CTkFont(size=10, family="Consolas"),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        timestamp_label.pack(side="left")
        
        level_badge = customtkinter.CTkLabel(
            top_row,
            text=log_entry.level,
            font=customtkinter.CTkFont(size=9, weight="bold"),
            text_color=level_config["text_color"],
            fg_color=level_config["badge_color"],
            corner_radius=PremiumDesignSystem.RADIUS_TINY,
            width=60,
            height=16
        )
        level_badge.pack(side="right")
        
        component_label = customtkinter.CTkLabel(
            top_row,
            text=f"[{log_entry.component}]",
            font=customtkinter.CTkFont(size=10, weight="bold"),
            text_color=level_config["text_color"],
            anchor="w"
        )
        component_label.pack(side="right", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        message_label = customtkinter.CTkLabel(
            content_frame,
            text=log_entry.message,
            font=customtkinter.CTkFont(size=11),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w",
            wraplength=500
        )
        message_label.pack(anchor="w", fill="x")
        
    def get_level_config(self):
        """Get styling configuration based on log level"""
        level_configs = {
            LogLevel.DEBUG: {
                "bg_color": PremiumDesignSystem.FROST_WHITE,
                "border_color": PremiumDesignSystem.BORDER_LIGHT,
                "badge_color": PremiumDesignSystem.TEXT_MUTED,
                "text_color": "white"
            },
            LogLevel.INFO: {
                "bg_color": PremiumDesignSystem.ICE_LIGHT,
                "border_color": PremiumDesignSystem.ICE_PRIMARY,
                "badge_color": PremiumDesignSystem.ICE_PRIMARY,
                "text_color": "white"
            },
            LogLevel.WARNING: {
                "bg_color": PremiumDesignSystem.WARNING_LIGHT,
                "border_color": PremiumDesignSystem.WARNING_AMBER,
                "badge_color": PremiumDesignSystem.WARNING_AMBER,
                "text_color": "white"
            },
            LogLevel.ERROR: {
                "bg_color": PremiumDesignSystem.DANGER_LIGHT,
                "border_color": PremiumDesignSystem.DANGER_RED,
                "badge_color": PremiumDesignSystem.DANGER_RED,
                "text_color": "white"
            },
            LogLevel.CRITICAL: {
                "bg_color": PremiumDesignSystem.DANGER_LIGHT,
                "border_color": PremiumDesignSystem.DANGER_RED,
                "badge_color": "#7F1D1D",
                "text_color": "white"
            }
        }
        
        return level_configs.get(
            self.log_entry.level,
            level_configs[LogLevel.INFO]
        )


class SystemMonitor(customtkinter.CTkFrame):
    """
    📊 System Monitor Dashboard
    Real-time system monitoring with beautiful charts and metrics
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        self.grid_columnconfigure((0, 1), weight=1)
        
        self.create_system_stats()
        self.create_activity_monitor()
        
    def create_system_stats(self):
        """Create system statistics cards"""
        stats_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        stats_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        cpu_card = StatsCard(
            stats_frame,
            title="CPU Usage",
            value="23%",
            subtitle="Average",
            trend="↓ 5% lower"
        )
        cpu_card.grid(
            row=0, column=0,
            sticky="ew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        memory_card = StatsCard(
            stats_frame,
            title="Memory",
            value="4.2GB",
            subtitle="8GB total",
            trend="↑ 0.8GB"
        )
        memory_card.grid(
            row=0, column=1,
            sticky="ew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        processes_card = StatsCard(
            stats_frame,
            title="Processes",
            value="247",
            subtitle="Running",
            trend="↑ 12 new"
        )
        processes_card.grid(
            row=0, column=2,
            sticky="ew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        network_card = StatsCard(
            stats_frame,
            title="Network",
            value="1.2MB/s",
            subtitle="Download",
            trend="↑ Active"
        )
        network_card.grid(
            row=0, column=3,
            sticky="ew"
        )
        
    def create_activity_monitor(self):
        """Create activity monitoring section"""
        activity_card = PremiumCard(
            self,
            elevated=True
        )
        activity_card.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        activity_header = customtkinter.CTkLabel(
            activity_card,
            text="Recent Activity",
            font=customtkinter.CTkFont(size=16, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY
        )
        activity_header.pack(
            pady=(PremiumDesignSystem.SPACE_LG, PremiumDesignSystem.SPACE_SM)
        )
        
        activities = [
            ("🔍", "File scan initiated", "2 seconds ago"),
            ("⚠️", "Suspicious activity detected", "1 minute ago"),
            ("✅", "System update completed", "5 minutes ago"),
            ("🛡️", "Protection rules updated", "10 minutes ago")
        ]
        
        for icon, activity, time in activities:
            activity_item = customtkinter.CTkFrame(
                activity_card,
                fg_color="transparent"
            )
            activity_item.pack(
                fill="x",
                padx=PremiumDesignSystem.SPACE_LG,
                pady=PremiumDesignSystem.SPACE_XS
            )
            
            icon_label = customtkinter.CTkLabel(
                activity_item,
                text=icon,
                font=customtkinter.CTkFont(size=14),
                width=30
            )
            icon_label.pack(side="left")
            
            text_frame = customtkinter.CTkFrame(
                activity_item,
                fg_color="transparent"
            )
            text_frame.pack(side="left", fill="both", expand=True)
            
            activity_label = customtkinter.CTkLabel(
                text_frame,
                text=activity,
                font=customtkinter.CTkFont(size=12),
                text_color=PremiumDesignSystem.TEXT_PRIMARY,
                anchor="w"
            )
            activity_label.pack(anchor="w")
            
            time_label = customtkinter.CTkLabel(
                activity_item,
                text=time,
                font=customtkinter.CTkFont(size=10),
                text_color=PremiumDesignSystem.TEXT_MUTED
            )
            time_label.pack(side="right")
        
        logs_card = PremiumCard(
            self,
            elevated=True
        )
        logs_card.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(PremiumDesignSystem.SPACE_SM, 0)
        )
        
        self.grid_rowconfigure(1, weight=1)
        
        self.log_viewer = LogViewer(logs_card)
        self.log_viewer.pack(fill="both", expand=True)


class LogAnalyzer(customtkinter.CTkFrame):
    """
    📝 Premium Log Analyzer Interface
    Comprehensive log analysis with monitoring and visualization
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_header()
        self.create_monitor_dashboard()
        self.create_footer()
        
    def create_header(self):
        """Create analyzer header"""
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
            text="📝 Log Analyzer",
            font=customtkinter.CTkFont(size=24, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(PremiumDesignSystem.SPACE_MD, 4))
        
        subtitle_label = customtkinter.CTkLabel(
            header_frame,
            text="Monitor system activity and analyze security logs in real-time",
            font=customtkinter.CTkFont(size=14),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        subtitle_label.pack(anchor="w")
        
    def create_monitor_dashboard(self):
        """Create monitoring dashboard"""
        self.monitor = SystemMonitor(self)
        self.monitor.grid(
            row=1,
            column=0,
            sticky="nsew"
        )
        
    def create_footer(self):
        """Create footer with navigation"""
        footer_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent",
            height=60
        )
        footer_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(PremiumDesignSystem.SPACE_LG, 0)
        )
        footer_frame.grid_propagate(False)
        
        button_frame = customtkinter.CTkFrame(
            footer_frame,
            fg_color="transparent"
        )
        button_frame.pack(pady=PremiumDesignSystem.SPACE_MD)
        
        export_btn = customtkinter.CTkButton(
            button_frame,
            text="📄 Export Logs",
            command=self.export_logs,
            **PremiumDesignSystem.get_button_style("secondary")
        )
        export_btn.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        clear_btn = customtkinter.CTkButton(
            button_frame,
            text="🗑️ Clear Logs",
            command=self.clear_logs,
            **PremiumDesignSystem.get_button_style("secondary")
        )
        clear_btn.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        back_btn = customtkinter.CTkButton(
            button_frame,
            text="← Back to Dashboard",
            command=self.go_back,
            **PremiumDesignSystem.get_button_style("secondary")
        )
        back_btn.pack(side="left")
        
    def export_logs(self):
        """Export system logs"""
        print("Exporting system logs...")
        
    def clear_logs(self):
        """Clear system logs"""
        print("Clearing system logs...")
        
    def go_back(self):
        """Navigate back to dashboard"""
        if hasattr(self, 'back_callback'):
            self.back_callback()
            
    def set_back_callback(self, callback):
        """Set back navigation callback"""
        self.back_callback = callback
        
    def add_log_entry(self, level, message, component="System", details=None):
        """Add new log entry"""
        entry = LogEntry(datetime.now(), level, message, component, details)
        self.monitor.log_viewer.add_log_entry(entry)