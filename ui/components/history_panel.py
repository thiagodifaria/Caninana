"""
📊 SCAN HISTORY PANEL
Beautiful scan history with filtering, search, and detailed view
"""

import customtkinter
from datetime import datetime, timedelta
import random
from .design_system import PremiumDesignSystem, IconManager
from .animated_widgets import PremiumCard
from .status_cards import StatsCard


class HistoryFilterBar(customtkinter.CTkFrame):
    """
    🔍 Premium Filter Bar
    Advanced filtering and search capabilities
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            **PremiumDesignSystem.get_card_style(),
            height=60
        )
        
        self.filter_callback = None
        
        self.content_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=PremiumDesignSystem.SPACE_LG,
            pady=PremiumDesignSystem.SPACE_SM
        )
        
        self.search_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.search_frame.pack(side="left", fill="y")
        
        self.search_entry = customtkinter.CTkEntry(
            self.search_frame,
            placeholder_text="🔍 Search scans...",
            width=200,
            font=customtkinter.CTkFont(size=12),
            corner_radius=PremiumDesignSystem.RADIUS_SM
        )
        self.search_entry.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_MD))
        self.search_entry.bind("<KeyRelease>", self.on_search_change)
        
        self.filter_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.filter_frame.pack(side="left", fill="y")
        
        self.result_filter = customtkinter.CTkOptionMenu(
            self.filter_frame,
            values=["All Results", "Clean Files", "Threats Found", "Errors"],
            command=self.on_filter_change,
            width=120,
            fg_color=PremiumDesignSystem.ICE_PRIMARY,
            button_color=PremiumDesignSystem.ICE_SECONDARY,
            button_hover_color=PremiumDesignSystem.ICE_ACCENT
        )
        self.result_filter.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        self.time_filter = customtkinter.CTkOptionMenu(
            self.filter_frame,
            values=["All Time", "Today", "This Week", "This Month"],
            command=self.on_filter_change,
            width=120,
            fg_color=PremiumDesignSystem.ICE_PRIMARY,
            button_color=PremiumDesignSystem.ICE_SECONDARY,
            button_hover_color=PremiumDesignSystem.ICE_ACCENT
        )
        self.time_filter.pack(side="left")
        
        self.actions_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.actions_frame.pack(side="right", fill="y")
        
        export_style = PremiumDesignSystem.get_button_style("secondary")
        self.export_btn = customtkinter.CTkButton(
            self.actions_frame,
            text="📄 Export",
            width=80,
            command=self.export_history,
            fg_color=export_style["fg_color"],
            hover_color=export_style["hover_color"],
            text_color=export_style["text_color"],
            corner_radius=export_style["corner_radius"],
            border_width=export_style["border_width"],
            border_color=export_style["border_color"],
            height=export_style["height"]
        )
        self.export_btn.pack(side="right", padx=(PremiumDesignSystem.SPACE_SM, 0))
        
        clear_style = PremiumDesignSystem.get_button_style("secondary")
        self.clear_btn = customtkinter.CTkButton(
            self.actions_frame,
            text="🗑️ Clear",
            width=80,
            command=self.clear_history,
            fg_color=clear_style["fg_color"],
            hover_color=clear_style["hover_color"],
            text_color=clear_style["text_color"],
            corner_radius=clear_style["corner_radius"],
            border_width=clear_style["border_width"],
            border_color=clear_style["border_color"],
            height=clear_style["height"]
        )
        self.clear_btn.pack(side="right")
        
    def on_search_change(self, event=None):
        """Handle search text change"""
        if self.filter_callback:
            self.filter_callback()
            
    def on_filter_change(self, value=None):
        """Handle filter change"""
        if self.filter_callback:
            self.filter_callback()
            
    def get_filters(self):
        """Get current filter values"""
        return {
            "search": self.search_entry.get(),
            "result": self.result_filter.get(),
            "time": self.time_filter.get()
        }
        
    def set_filter_callback(self, callback):
        """Set callback for filter changes"""
        self.filter_callback = callback
        
    def export_history(self):
        """Export scan history"""
        print("Exporting scan history...")
        
    def clear_history(self):
        """Clear scan history"""
        print("Clearing scan history...")


class HistoryItem(PremiumCard):
    """
    📋 Individual History Item
    Beautiful card displaying scan details
    """
    
    def __init__(self, parent, scan_data, **kwargs):
        super().__init__(parent, elevated=False, hoverable=True, **kwargs)
        
        self.scan_data = scan_data
        self.configure(height=80)
        
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
        
        self.status_frame = customtkinter.CTkFrame(
            self.content_frame,
            width=50,
            fg_color="transparent"
        )
        self.status_frame.pack(side="left", fill="y")
        self.status_frame.pack_propagate(False)
        
        status_config = self.get_status_config()
        self.status_icon = customtkinter.CTkLabel(
            self.status_frame,
            text=status_config["icon"],
            font=customtkinter.CTkFont(size=24),
            text_color=status_config["color"]
        )
        self.status_icon.pack(expand=True)
        
        self.details_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.details_frame.pack(
            side="left", 
            fill="both", 
            expand=True, 
            padx=(PremiumDesignSystem.SPACE_MD, 0)
        )
        
        self.filename_label = customtkinter.CTkLabel(
            self.details_frame,
            text=scan_data.get("filename", "Unknown File"),
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.filename_label.pack(anchor="w")
        
        result_text = self.get_result_text()
        self.result_label = customtkinter.CTkLabel(
            self.details_frame,
            text=result_text,
            font=customtkinter.CTkFont(size=11),
            text_color=status_config["color"],
            anchor="w"
        )
        self.result_label.pack(anchor="w")
        
        scan_info = f"Size: {scan_data.get('size', 'Unknown')} • Duration: {scan_data.get('duration', 'Unknown')}"
        self.info_label = customtkinter.CTkLabel(
            self.details_frame,
            text=scan_info,
            font=customtkinter.CTkFont(size=10),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        self.info_label.pack(anchor="w")
        
        self.meta_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.meta_frame.pack(side="right", fill="y")
        
        self.time_label = customtkinter.CTkLabel(
            self.meta_frame,
            text=scan_data.get("timestamp", "Unknown"),
            font=customtkinter.CTkFont(size=10),
            text_color=PremiumDesignSystem.TEXT_MUTED,
            anchor="e"
        )
        self.time_label.pack(side="top", anchor="e")
        
        if scan_data.get("result") == "threat":
            button_style = PremiumDesignSystem.get_button_style("secondary")
            self.action_btn = customtkinter.CTkButton(
                self.meta_frame,
                text="Details",
                width=60,
                height=24,
                font=customtkinter.CTkFont(size=10),
                fg_color=button_style["fg_color"],
                hover_color=button_style["hover_color"],
                text_color=button_style["text_color"],
                corner_radius=button_style["corner_radius"],
                border_width=button_style["border_width"],
                border_color=button_style["border_color"]
            )
            self.action_btn.pack(side="bottom", anchor="e", pady=(4, 0))
    
    def get_status_config(self):
        """Get status configuration based on scan result"""
        result = self.scan_data.get("result", "clean")
        
        if result == "clean":
            return {
                "icon": IconManager.get("success"),
                "color": PremiumDesignSystem.SUCCESS_GREEN
            }
        elif result == "threat":
            return {
                "icon": IconManager.get("danger"),
                "color": PremiumDesignSystem.DANGER_RED
            }
        elif result == "error":
            return {
                "icon": IconManager.get("error"),
                "color": PremiumDesignSystem.WARNING_AMBER
            }
        else:
            return {
                "icon": IconManager.get("info"),
                "color": PremiumDesignSystem.TEXT_SECONDARY
            }
    
    def get_result_text(self):
        """Get result description text"""
        result = self.scan_data.get("result", "clean")
        
        if result == "clean":
            return "No threats detected"
        elif result == "threat":
            threats = self.scan_data.get("threats", [])
            if threats:
                return f"Threats found: {', '.join(threats[:2])}"
            return "Malware detected"
        elif result == "error":
            return "Scan failed"
        else:
            return "Unknown result"


class HistoryStats(customtkinter.CTkFrame):
    """
    📈 History Statistics Overview
    Beautiful stats cards showing scan history metrics
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.create_stats_cards()
        
    def create_stats_cards(self):
        """Create statistics cards"""
        
        self.total_scans_card = StatsCard(
            self,
            title="Total Scans",
            value="1,247",
            subtitle="All time",
            trend="↑ 23 this week"
        )
        self.total_scans_card.grid(
            row=0, column=0,
            sticky="ew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        self.clean_files_card = StatsCard(
            self,
            title="Clean Files",
            value="1,239",
            subtitle="99.4%",
            trend="↑ 99.4%"
        )
        self.clean_files_card.grid(
            row=0, column=1,
            sticky="ew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        self.threats_card = StatsCard(
            self,
            title="Threats Found",
            value="8",
            subtitle="0.6%",
            trend="↓ 2 this month"
        )
        self.threats_card.grid(
            row=0, column=2,
            sticky="ew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        self.avg_time_card = StatsCard(
            self,
            title="Avg Scan Time",
            value="2.3s",
            subtitle="Per file",
            trend="↓ 15% faster"
        )
        self.avg_time_card.grid(
            row=0, column=3,
            sticky="ew"
        )
    
    def update_stats(self, history_data):
        """Update stats based on history data"""
        total_scans = len(history_data)
        clean_scans = sum(1 for item in history_data if item.get("result") == "clean")
        threat_scans = sum(1 for item in history_data if item.get("result") == "threat")
        
        self.total_scans_card.update_value(str(total_scans))
        self.clean_files_card.update_value(str(clean_scans))
        self.threats_card.update_value(str(threat_scans))


class ScanHistoryPanel(customtkinter.CTkFrame):
    """
    📊 Premium Scan History Panel
    Comprehensive history view with filtering and statistics
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        self.history_data = self.generate_sample_data()
        self.filtered_data = self.history_data.copy()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.create_header()
        self.create_stats_section()
        self.create_filter_section()
        self.create_history_list()
        self.create_footer()
        
    def create_header(self):
        """Create history panel header"""
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
            text="📊 Scan History",
            font=customtkinter.CTkFont(size=24, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(PremiumDesignSystem.SPACE_MD, 4))
        
        subtitle_label = customtkinter.CTkLabel(
            header_frame,
            text="View and manage your scan history and results",
            font=customtkinter.CTkFont(size=14),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        subtitle_label.pack(anchor="w")
        
    def create_stats_section(self):
        """Create statistics section"""
        self.stats_panel = HistoryStats(self)
        self.stats_panel.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
    def create_filter_section(self):
        """Create filter and search section"""
        self.filter_bar = HistoryFilterBar(self)
        self.filter_bar.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_MD)
        )
        self.filter_bar.set_filter_callback(self.apply_filters)
        
    def create_history_list(self):
        """Create scrollable history list"""
        self.history_frame = customtkinter.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.history_frame.grid(
            row=3,
            column=0,
            sticky="nsew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
        self.populate_history_list()
        
    def create_footer(self):
        """Create footer with navigation"""
        footer_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent",
            height=60
        )
        footer_frame.grid(
            row=4,
            column=0,
            sticky="ew"
        )
        footer_frame.grid_propagate(False)
        
        back_style = PremiumDesignSystem.get_button_style("secondary")
        back_button = customtkinter.CTkButton(
            footer_frame,
            text="← Back to Dashboard",
            command=self.go_back,
            fg_color=back_style["fg_color"],
            hover_color=back_style["hover_color"],
            text_color=back_style["text_color"],
            corner_radius=back_style["corner_radius"],
            border_width=back_style["border_width"],
            border_color=back_style["border_color"],
            height=back_style["height"]
        )
        back_button.pack(pady=PremiumDesignSystem.SPACE_MD)
        
    def generate_sample_data(self):
        """Generate sample scan history data"""
        sample_data = []
        
        filenames = [
            "document.pdf", "application.exe", "image.jpg", "archive.zip",
            "script.py", "presentation.pptx", "suspicious_file.exe", "malware.dll",
            "clean_app.msi", "photo.png", "video.mp4", "trojan.exe"
        ]
        
        results = ["clean", "clean", "clean", "threat", "clean", "error"]
        
        for i in range(50):
            filename = random.choice(filenames)
            result = random.choice(results)
            
            days_ago = random.randint(0, 30)
            timestamp = datetime.now() - timedelta(days=days_ago)
            
            scan_data = {
                "filename": filename,
                "result": result,
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M"),
                "size": f"{random.randint(1, 999)} KB",
                "duration": f"{random.randint(1, 30)}s",
                "threats": ["Trojan.Win32.Example", "Malware.Generic"] if result == "threat" else []
            }
            
            sample_data.append(scan_data)
            
        return sorted(sample_data, key=lambda x: x["timestamp"], reverse=True)
    
    def populate_history_list(self):
        """Populate history list with filtered data"""
        for widget in self.history_frame.winfo_children():
            widget.destroy()
            
        for scan_data in self.filtered_data:
            history_item = HistoryItem(
                self.history_frame,
                scan_data
            )
            history_item.pack(
                fill="x",
                pady=(0, PremiumDesignSystem.SPACE_SM)
            )
            
    def apply_filters(self):
        """Apply current filters to history data"""
        filters = self.filter_bar.get_filters()
        
        filtered = self.history_data.copy()
        
        if filters["search"]:
            search_term = filters["search"].lower()
            filtered = [
                item for item in filtered
                if search_term in item["filename"].lower()
            ]
        
        if filters["result"] != "All Results":
            result_map = {
                "Clean Files": "clean",
                "Threats Found": "threat", 
                "Errors": "error"
            }
            if filters["result"] in result_map:
                target_result = result_map[filters["result"]]
                filtered = [
                    item for item in filtered
                    if item["result"] == target_result
                ]
        
        if filters["time"] != "All Time":
            now = datetime.now()
            if filters["time"] == "Today":
                cutoff = now - timedelta(days=1)
            elif filters["time"] == "This Week":
                cutoff = now - timedelta(days=7)
            elif filters["time"] == "This Month":
                cutoff = now - timedelta(days=30)
            else:
                cutoff = None
                
            if cutoff:
                filtered = [
                    item for item in filtered
                    if datetime.strptime(item["timestamp"], "%Y-%m-%d %H:%M") >= cutoff
                ]
        
        self.filtered_data = filtered
        self.populate_history_list()
        
        self.stats_panel.update_stats(filtered)
        
    def go_back(self):
        """Navigate back to dashboard"""
        if hasattr(self, 'back_callback'):
            self.back_callback()
            
    def set_back_callback(self, callback):
        """Set back navigation callback"""
        self.back_callback = callback