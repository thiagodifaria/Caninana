"""
📊 RESULTS DASHBOARD
Comprehensive scan results with detailed analysis and beautiful visualizations
"""

import customtkinter
from datetime import datetime
import random
from .design_system import PremiumDesignSystem, IconManager
from .animated_widgets import PremiumCard
from .status_cards import StatsCard


class ThreatDetails(PremiumCard):
    """
    🚨 Threat Details Card
    Detailed information about detected threats
    """
    
    def __init__(self, parent, threat_data, **kwargs):
        super().__init__(parent, elevated=True, **kwargs)
        
        self.threat_data = threat_data
        
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
        
        self.create_threat_header()
        
        self.create_threat_details()
        
        self.create_action_buttons()
        
    def create_threat_header(self):
        """Create threat header with severity"""
        header_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", pady=(0, PremiumDesignSystem.SPACE_MD))
        
        threat_icon = customtkinter.CTkLabel(
            header_frame,
            text=IconManager.get("danger"),
            font=customtkinter.CTkFont(size=32),
            text_color=PremiumDesignSystem.DANGER_RED
        )
        threat_icon.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_MD))
        
        info_frame = customtkinter.CTkFrame(
            header_frame,
            fg_color="transparent"
        )
        info_frame.pack(side="left", fill="both", expand=True)
        
        threat_name = customtkinter.CTkLabel(
            info_frame,
            text=self.threat_data.get("name", "Unknown Threat"),
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color=PremiumDesignSystem.DANGER_RED,
            anchor="w"
        )
        threat_name.pack(anchor="w")
        
        threat_info = f"Type: {self.threat_data.get('type', 'Unknown')} • Severity: {self.threat_data.get('severity', 'Unknown')}"
        threat_details = customtkinter.CTkLabel(
            info_frame,
            text=threat_info,
            font=customtkinter.CTkFont(size=12),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        threat_details.pack(anchor="w")
        
        severity = self.threat_data.get("severity", "Medium")
        severity_color = self.get_severity_color(severity)
        
        severity_badge = customtkinter.CTkLabel(
            header_frame,
            text=severity.upper(),
            font=customtkinter.CTkFont(size=10, weight="bold"),
            text_color="white",
            fg_color=severity_color,
            corner_radius=PremiumDesignSystem.RADIUS_SM,
            width=80,
            height=24
        )
        severity_badge.pack(side="right")
        
    def create_threat_details(self):
        """Create detailed threat information"""
        details_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color=PremiumDesignSystem.DANGER_LIGHT,
            corner_radius=PremiumDesignSystem.RADIUS_SM
        )
        details_frame.pack(
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_MD)
        )
        
        details_content = customtkinter.CTkFrame(
            details_frame,
            fg_color="transparent"
        )
        details_content.pack(
            fill="x",
            padx=PremiumDesignSystem.SPACE_MD,
            pady=PremiumDesignSystem.SPACE_SM
        )
        
        if "file_path" in self.threat_data:
            path_label = customtkinter.CTkLabel(
                details_content,
                text=f"📁 File: {self.threat_data['file_path']}",
                font=customtkinter.CTkFont(size=11),
                text_color=PremiumDesignSystem.TEXT_PRIMARY,
                anchor="w"
            )
            path_label.pack(anchor="w", pady=(0, 4))
        
        if "description" in self.threat_data:
            desc_label = customtkinter.CTkLabel(
                details_content,
                text=f"Description: {self.threat_data['description']}",
                font=customtkinter.CTkFont(size=11),
                text_color=PremiumDesignSystem.TEXT_PRIMARY,
                anchor="w",
                wraplength=400
            )
            desc_label.pack(anchor="w", pady=(0, 4))
        
        detection_time = self.threat_data.get("detected_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time_label = customtkinter.CTkLabel(
            details_content,
            text=f"⏰ Detected: {detection_time}",
            font=customtkinter.CTkFont(size=11),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        time_label.pack(anchor="w")
        
    def create_action_buttons(self):
        """Create action buttons for threat handling"""
        button_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        button_frame.pack(fill="x")
        
        quarantine_btn = customtkinter.CTkButton(
            button_frame,
            text="🔒 Quarantine",
            command=lambda: self.handle_threat("quarantine"),
            **PremiumDesignSystem.get_button_style("primary")
        )
        quarantine_btn.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        delete_btn = customtkinter.CTkButton(
            button_frame,
            text="🗑️ Delete",
            command=lambda: self.handle_threat("delete"),
            fg_color=PremiumDesignSystem.DANGER_RED,
            hover_color="#B91C1C",
            text_color="white",
            corner_radius=PremiumDesignSystem.RADIUS_MD,
            height=PremiumDesignSystem.BUTTON_HEIGHT
        )
        delete_btn.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        ignore_btn = customtkinter.CTkButton(
            button_frame,
            text="❌ Ignore",
            command=lambda: self.handle_threat("ignore"),
            **PremiumDesignSystem.get_button_style("secondary")
        )
        ignore_btn.pack(side="left")
        
    def get_severity_color(self, severity):
        """Get color based on threat severity"""
        severity_colors = {
            "Low": PremiumDesignSystem.WARNING_AMBER,
            "Medium": "#EA580C",
            "High": PremiumDesignSystem.DANGER_RED,
            "Critical": "#7F1D1D"
        }
        return severity_colors.get(severity, PremiumDesignSystem.WARNING_AMBER)
        
    def handle_threat(self, action):
        """Handle threat action"""
        print(f"Handling threat '{self.threat_data.get('name')}' with action: {action}")


class ScanSummary(customtkinter.CTkFrame):
    """
    📋 Scan Summary Overview
    Beautiful summary of scan results with key metrics
    """
    
    def __init__(self, parent, scan_results, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        self.scan_results = scan_results
        
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        self.create_summary_cards()
        
    def create_summary_cards(self):
        """Create summary statistics cards"""
        
        files_scanned = self.scan_results.get("files_scanned", 0)
        files_card = StatsCard(
            self,
            title="Files Scanned",
            value=str(files_scanned),
            subtitle="Total files",
            trend=""
        )
        files_card.grid(
            row=0, column=0,
            sticky="ew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        threats_found = len(self.scan_results.get("threats", []))
        threat_color = PremiumDesignSystem.DANGER_RED if threats_found > 0 else PremiumDesignSystem.SUCCESS_GREEN
        threats_card = StatsCard(
            self,
            title="Threats Found",
            value=str(threats_found),
            subtitle="Security issues",
            trend="🚨 Action required" if threats_found > 0 else "✅ Clean"
        )
        threats_card.grid(
            row=0, column=1,
            sticky="ew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        duration = self.scan_results.get("duration", "0s")
        duration_card = StatsCard(
            self,
            title="Scan Duration", 
            value=duration,
            subtitle="Total time",
            trend=""
        )
        duration_card.grid(
            row=0, column=2,
            sticky="ew",
            padx=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        scan_type = self.scan_results.get("scan_type", "Unknown")
        type_card = StatsCard(
            self,
            title="Scan Type",
            value=scan_type,
            subtitle="Method used",
            trend=""
        )
        type_card.grid(
            row=0, column=3,
            sticky="ew"
        )


class CleanResults(PremiumCard):
    """
    ✅ Clean Scan Results
    Beautiful display for clean scan results
    """
    
    def __init__(self, parent, scan_results, **kwargs):
        super().__init__(parent, elevated=True, **kwargs)
        
        self.scan_results = scan_results
        
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
        
        header_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", pady=(0, PremiumDesignSystem.SPACE_LG))
        
        success_icon = customtkinter.CTkLabel(
            header_frame,
            text=IconManager.get("success"),
            font=customtkinter.CTkFont(size=48),
            text_color=PremiumDesignSystem.SUCCESS_GREEN
        )
        success_icon.pack(pady=(0, PremiumDesignSystem.SPACE_MD))
        
        success_title = customtkinter.CTkLabel(
            header_frame,
            text="Scan Complete - No Threats Found",
            font=customtkinter.CTkFont(size=20, weight="bold"),
            text_color=PremiumDesignSystem.SUCCESS_GREEN
        )
        success_title.pack(pady=(0, PremiumDesignSystem.SPACE_SM))
        
        files_count = self.scan_results.get("files_scanned", 0)
        success_message = customtkinter.CTkLabel(
            header_frame,
            text=f"All {files_count} files passed security checks. Your system is secure.",
            font=customtkinter.CTkFont(size=14),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            justify="center"
        )
        success_message.pack()
        
        details_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color=PremiumDesignSystem.SUCCESS_LIGHT,
            corner_radius=PremiumDesignSystem.RADIUS_SM
        )
        details_frame.pack(fill="x", pady=(PremiumDesignSystem.SPACE_LG, 0))
        
        details_content = customtkinter.CTkFrame(
            details_frame,
            fg_color="transparent"
        )
        details_content.pack(
            fill="x",
            padx=PremiumDesignSystem.SPACE_MD,
            pady=PremiumDesignSystem.SPACE_SM
        )
        
        scan_details = [
            f"✅ Scanned {files_count} files",
            f"✅ Completed in {self.scan_results.get('duration', 'Unknown')}",
            f"✅ Used {self.scan_results.get('signatures_count', 'Unknown')} threat signatures",
            "✅ No malware, viruses, or suspicious patterns detected"
        ]
        
        for detail in scan_details:
            detail_label = customtkinter.CTkLabel(
                details_content,
                text=detail,
                font=customtkinter.CTkFont(size=12),
                text_color=PremiumDesignSystem.TEXT_PRIMARY,
                anchor="w"
            )
            detail_label.pack(anchor="w", pady=2)


class ResultsDashboard(customtkinter.CTkFrame):
    """
    📊 Premium Results Dashboard
    Comprehensive display of scan results with detailed analysis
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        self.grid_columnconfigure(0, weight=1)
        
        self.scan_results = self.generate_sample_results()
        
        self.create_header()
        self.create_summary_section()
        self.create_results_content()
        self.create_footer()
        
    def create_header(self):
        """Create results header"""
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
            text="📊 Scan Results",
            font=customtkinter.CTkFont(size=24, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(PremiumDesignSystem.SPACE_MD, 4))
        
        subtitle_label = customtkinter.CTkLabel(
            header_frame,
            text="Detailed analysis of your security scan results",
            font=customtkinter.CTkFont(size=14),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        subtitle_label.pack(anchor="w")
        
    def create_summary_section(self):
        """Create scan summary section"""
        self.summary_panel = ScanSummary(
            self,
            self.scan_results
        )
        self.summary_panel.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
    def create_results_content(self):
        """Create main results content"""
        self.content_scroll = customtkinter.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.content_scroll.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        self.grid_rowconfigure(2, weight=1)
        
        threats = self.scan_results.get("threats", [])
        if threats:
            self.show_threat_results(threats)
        else:
            self.show_clean_results()
            
    def create_footer(self):
        """Create footer with actions"""
        footer_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent",
            height=60
        )
        footer_frame.grid(
            row=3,
            column=0,
            sticky="ew"
        )
        footer_frame.grid_propagate(False)
        
        button_frame = customtkinter.CTkFrame(
            footer_frame,
            fg_color="transparent"
        )
        button_frame.pack(pady=PremiumDesignSystem.SPACE_MD)
        
        new_scan_btn = customtkinter.CTkButton(
            button_frame,
            text="🔍 New Scan",
            command=self.start_new_scan,
            **PremiumDesignSystem.get_button_style("success")
        )
        new_scan_btn.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        export_btn = customtkinter.CTkButton(
            button_frame,
            text="📄 Export Results",
            command=self.export_results,
            **PremiumDesignSystem.get_button_style("secondary")
        )
        export_btn.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        back_btn = customtkinter.CTkButton(
            button_frame,
            text="← Back to Dashboard",
            command=self.go_back,
            **PremiumDesignSystem.get_button_style("secondary")
        )
        back_btn.pack(side="left")
        
    def show_threat_results(self, threats):
        """Show threat detection results"""
        threats_header = customtkinter.CTkLabel(
            self.content_scroll,
            text="⚠️ Threats Detected",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color=PremiumDesignSystem.DANGER_RED,
            anchor="w"
        )
        threats_header.pack(
            anchor="w",
            pady=(0, PremiumDesignSystem.SPACE_MD)
        )
        
        for threat in threats:
            threat_card = ThreatDetails(
                self.content_scroll,
                threat
            )
            threat_card.pack(
                fill="x",
                pady=(0, PremiumDesignSystem.SPACE_MD)
            )
            
    def show_clean_results(self):
        """Show clean scan results"""
        clean_card = CleanResults(
            self.content_scroll,
            self.scan_results
        )
        clean_card.pack(fill="x")
        
    def generate_sample_results(self):
        """Generate sample scan results"""
        has_threats = random.choice([True, False])
        
        results = {
            "scan_type": "Full System Scan",
            "files_scanned": random.randint(1000, 5000),
            "duration": f"{random.randint(120, 600)}s",
            "signatures_count": "15,247",
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if has_threats:
            sample_threats = [
                {
                    "name": "Trojan.Win32.Malware",
                    "type": "Trojan",
                    "severity": "High",
                    "file_path": "C:\\Downloads\\suspicious_file.exe",
                    "description": "A trojan horse that attempts to steal sensitive information and create backdoors.",
                    "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                },
                {
                    "name": "Adware.Generic.Popup",
                    "type": "Adware",
                    "severity": "Medium",
                    "file_path": "C:\\Temp\\adware_installer.msi",
                    "description": "Potentially unwanted program that displays advertisements and tracks user behavior.",
                    "detected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ]
            results["threats"] = random.sample(sample_threats, random.randint(1, 2))
        else:
            results["threats"] = []
            
        return results
        
    def set_scan_results(self, results):
        """Set scan results and refresh display"""
        self.scan_results = results
        
        self.summary_panel.destroy()
        self.summary_panel = ScanSummary(self, self.scan_results)
        self.summary_panel.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
        for widget in self.content_scroll.winfo_children():
            widget.destroy()
            
        threats = self.scan_results.get("threats", [])
        if threats:
            self.show_threat_results(threats)
        else:
            self.show_clean_results()
            
    def start_new_scan(self):
        """Start a new scan"""
        if hasattr(self, 'new_scan_callback'):
            self.new_scan_callback()
            
    def export_results(self):
        """Export scan results"""
        print("Exporting scan results...")
        
    def go_back(self):
        """Navigate back to dashboard"""
        if hasattr(self, 'back_callback'):
            self.back_callback()
            
    def set_new_scan_callback(self, callback):
        """Set new scan callback"""
        self.new_scan_callback = callback
        
    def set_back_callback(self, callback):
        """Set back navigation callback"""
        self.back_callback = callback