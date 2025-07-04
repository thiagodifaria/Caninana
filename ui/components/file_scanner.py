"""
🔍 PREMIUM FILE SCANNER
Sophisticated file scanning interface with beautiful animations
"""

import customtkinter
import os
from tkinter import filedialog
from .design_system import PremiumDesignSystem, IconManager
from .status_cards import PremiumStatusCard
from .animated_widgets import PremiumCard, GlassProgressBar


class FileDropZone(PremiumCard):
    """
    📁 Premium File Drop Zone
    Beautiful drag-and-drop area with visual feedback
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, elevated=False, hoverable=True, **kwargs)
        
        self.configure(
            height=180,
            fg_color=PremiumDesignSystem.ICE_LIGHT,
            border_width=2,
            border_color=PremiumDesignSystem.BORDER_MEDIUM
        )
        
        self.selected_file = None
        self.file_callback = None
        
        self.content_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=PremiumDesignSystem.SPACE_XL,
            pady=PremiumDesignSystem.SPACE_XL
        )
        
        self.drop_icon = customtkinter.CTkLabel(
            self.content_frame,
            text="📁",
            font=customtkinter.CTkFont(size=48),
            text_color=PremiumDesignSystem.ICE_PRIMARY
        )
        self.drop_icon.pack(pady=(0, PremiumDesignSystem.SPACE_MD))
        
        self.drop_text = customtkinter.CTkLabel(
            self.content_frame,
            text="Select a file to scan",
            font=customtkinter.CTkFont(size=16, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY
        )
        self.drop_text.pack(pady=(0, PremiumDesignSystem.SPACE_XS))
        
        self.instructions = customtkinter.CTkLabel(
            self.content_frame,
            text="Click browse or drag and drop a file here",
            font=customtkinter.CTkFont(size=12),
            text_color=PremiumDesignSystem.TEXT_SECONDARY
        )
        self.instructions.pack(pady=(0, PremiumDesignSystem.SPACE_MD))
        
        self.browse_btn = customtkinter.CTkButton(
            self.content_frame,
            text="📁 Browse Files",
            command=self.browse_file,
            **PremiumDesignSystem.get_button_style("primary")
        )
        self.browse_btn.pack()
        
    def browse_file(self):
        """Open file browser"""
        filepath = filedialog.askopenfilename(
            title="Select File to Scan",
            filetypes=[
                ("All Files", "*.*"),
                ("Executable Files", "*.exe *.msi *.bat *.cmd *.scr"),
                ("Documents", "*.pdf *.doc *.docx *.xls *.xlsx *.ppt *.pptx"),
                ("Archives", "*.zip *.rar *.7z *.tar *.gz *.bz2"),
                ("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
                ("Scripts", "*.py *.js *.vbs *.ps1 *.sh *.php"),
                ("Media", "*.mp3 *.mp4 *.avi *.mov *.wmv")
            ]
        )
        
        if filepath:
            self.set_selected_file(filepath)
            
    def set_selected_file(self, filepath):
        """Set selected file and update UI"""
        self.selected_file = filepath
        filename = os.path.basename(filepath)
        
        self.drop_icon.configure(text="✅")
        self.drop_text.configure(
            text=f"Selected: {filename}",
            text_color=PremiumDesignSystem.SUCCESS_GREEN
        )
        
        file_size = self.get_file_size(filepath)
        self.instructions.configure(
            text=f"File size: {file_size} • Click scan to analyze"
        )
        
        self.configure(
            border_color=PremiumDesignSystem.SUCCESS_GREEN,
            fg_color=PremiumDesignSystem.SUCCESS_LIGHT
        )
        
        if self.file_callback:
            self.file_callback(filepath)
    
    def get_file_size(self, filepath):
        """Get human-readable file size"""
        try:
            size = os.path.getsize(filepath)
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} PB"
        except:
            return "Unknown"
    
    def set_file_callback(self, callback):
        """Set callback for file selection"""
        self.file_callback = callback
        
    def reset(self):
        """Reset drop zone to initial state"""
        self.selected_file = None
        self.drop_icon.configure(text="📁")
        self.drop_text.configure(
            text="Select a file to scan",
            text_color=PremiumDesignSystem.TEXT_PRIMARY
        )
        self.instructions.configure(
            text="Click browse or drag and drop a file here"
        )
        self.configure(
            border_color=PremiumDesignSystem.BORDER_MEDIUM,
            fg_color=PremiumDesignSystem.ICE_LIGHT
        )


class ScanProgressPanel(PremiumCard):
    """
    ⏳ Premium Scan Progress Panel
    Beautiful progress display with detailed status
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, elevated=True, **kwargs)
        
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
        
        self.header_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        self.header_frame.pack(fill="x", pady=(0, PremiumDesignSystem.SPACE_SM))
        
        self.progress_title = customtkinter.CTkLabel(
            self.header_frame,
            text="Scan Progress",
            font=customtkinter.CTkFont(size=14, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        self.progress_title.pack(side="left")
        
        self.progress_percent = customtkinter.CTkLabel(
            self.header_frame,
            text="0%",
            font=customtkinter.CTkFont(size=12, weight="bold"),
            text_color=PremiumDesignSystem.ICE_PRIMARY,
            anchor="e"
        )
        self.progress_percent.pack(side="right")
        
        self.progress_bar = GlassProgressBar(self.content_frame)
        self.progress_bar.pack(
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_SM)
        )
        
        self.status_message = customtkinter.CTkLabel(
            self.content_frame,
            text="Ready to scan...",
            font=customtkinter.CTkFont(size=11),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        self.status_message.pack(anchor="w")
        
        self.pack_forget()
        
    def show_progress(self):
        """Show progress panel"""
        self.pack(
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
    def hide_progress(self):
        """Hide progress panel"""
        self.pack_forget()
        
    def set_progress(self, value, message=""):
        """Update progress value and message"""
        self.progress_bar.set_progress(value)
        self.progress_percent.configure(text=f"{int(value * 100)}%")
        if message:
            self.status_message.configure(text=message)
            
    def start_indeterminate(self, message="Scanning..."):
        """Start indeterminate progress"""
        self.progress_bar.start_indeterminate_animation()
        self.progress_percent.configure(text="")
        self.status_message.configure(text=message)
        
    def stop_progress(self):
        """Stop progress animation"""
        self.progress_bar.stop_animation()


class ScanResultsPanel(PremiumCard):
    """
    📊 Premium Scan Results Panel
    Beautiful results display with detailed information
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, elevated=True, **kwargs)
        
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
        
        self.pack_forget()
        
    def show_results(self, scan_result, filename):
        """Show scan results"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        if scan_result.threat_detected:
            self.show_threat_detected(scan_result, filename)
        else:
            self.show_clean_result(filename)
            
        self.pack(
            fill="x",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
    def show_threat_detected(self, scan_result, filename):
        """Show threat detection results"""
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
        
        text_frame = customtkinter.CTkFrame(
            header_frame,
            fg_color="transparent"
        )
        text_frame.pack(side="left", fill="both", expand=True)
        
        title_label = customtkinter.CTkLabel(
            text_frame,
            text="Threat Detected!",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color=PremiumDesignSystem.DANGER_RED,
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = customtkinter.CTkLabel(
            text_frame,
            text=f"Malicious content found in {filename}",
            font=customtkinter.CTkFont(size=12),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        subtitle_label.pack(anchor="w")
        
        threats_text = ", ".join(scan_result.detected_signatures)
        detail_label = customtkinter.CTkLabel(
            self.content_frame,
            text=f"Detected threats: {threats_text}",
            font=customtkinter.CTkFont(size=12),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w",
            wraplength=400
        )
        detail_label.pack(anchor="w", pady=(0, PremiumDesignSystem.SPACE_MD))
        
        action_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        action_frame.pack(fill="x")
        
        quarantine_btn = customtkinter.CTkButton(
            action_frame,
            text="🔒 Quarantine File",
            **PremiumDesignSystem.get_button_style("primary")
        )
        quarantine_btn.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_SM))
        
        delete_btn = customtkinter.CTkButton(
            action_frame,
            text="🗑️ Delete File",
            fg_color=PremiumDesignSystem.DANGER_RED,
            hover_color="#B91C1C",
            text_color="white",
            corner_radius=PremiumDesignSystem.RADIUS_MD,
            height=PremiumDesignSystem.BUTTON_HEIGHT
        )
        delete_btn.pack(side="left")
        
    def show_clean_result(self, filename):
        """Show clean scan results"""
        header_frame = customtkinter.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", pady=(0, PremiumDesignSystem.SPACE_MD))
        
        success_icon = customtkinter.CTkLabel(
            header_frame,
            text=IconManager.get("success"),
            font=customtkinter.CTkFont(size=32),
            text_color=PremiumDesignSystem.SUCCESS_GREEN
        )
        success_icon.pack(side="left", padx=(0, PremiumDesignSystem.SPACE_MD))
        
        text_frame = customtkinter.CTkFrame(
            header_frame,
            fg_color="transparent"
        )
        text_frame.pack(side="left", fill="both", expand=True)
        
        title_label = customtkinter.CTkLabel(
            text_frame,
            text="File is Clean",
            font=customtkinter.CTkFont(size=18, weight="bold"),
            text_color=PremiumDesignSystem.SUCCESS_GREEN,
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        subtitle_label = customtkinter.CTkLabel(
            text_frame,
            text=f"{filename} passed all security checks",
            font=customtkinter.CTkFont(size=12),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        subtitle_label.pack(anchor="w")
        
        detail_label = customtkinter.CTkLabel(
            self.content_frame,
            text="No malware, viruses, or suspicious patterns detected",
            font=customtkinter.CTkFont(size=12),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        detail_label.pack(anchor="w")
        
    def hide_results(self):
        """Hide results panel"""
        self.pack_forget()


class PremiumFileScanner(customtkinter.CTkFrame):
    """
    🔍 Premium File Scanner Interface
    Sophisticated file scanning with beautiful UI and animations
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color="transparent")
        
        self.scan_callback = None
        self.back_callback = None
        
        self.grid_columnconfigure(0, weight=1)
        
        self.create_header()
        self.create_file_selection()
        self.create_scan_controls()
        self.create_progress_section()
        self.create_results_section()
        self.create_footer()
        
    def create_header(self):
        """Create scanner header"""
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
            text="🔍 File Scanner",
            font=customtkinter.CTkFont(size=24, weight="bold"),
            text_color=PremiumDesignSystem.TEXT_PRIMARY,
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(PremiumDesignSystem.SPACE_MD, 4))
        
        subtitle_label = customtkinter.CTkLabel(
            header_frame,
            text="Advanced malware detection for individual files and archives",
            font=customtkinter.CTkFont(size=14),
            text_color=PremiumDesignSystem.TEXT_SECONDARY,
            anchor="w"
        )
        subtitle_label.pack(anchor="w")
        
    def create_file_selection(self):
        """Create file selection area"""
        self.drop_zone = FileDropZone(self)
        self.drop_zone.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        self.drop_zone.set_file_callback(self.on_file_selected)
        
    def create_scan_controls(self):
        """Create scan control buttons"""
        controls_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent"
        )
        controls_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, PremiumDesignSystem.SPACE_LG)
        )
        
        self.scan_button = customtkinter.CTkButton(
            controls_frame,
            text="🔍 Scan File",
            state="disabled",
            command=self.start_scan,
            **PremiumDesignSystem.get_button_style("success"),
            width=140
        )
        self.scan_button.pack(side="left")
        
        self.clear_button = customtkinter.CTkButton(
            controls_frame,
            text="🗑️ Clear",
            command=self.clear_selection,
            **PremiumDesignSystem.get_button_style("secondary"),
            width=100
        )
        self.clear_button.pack(
            side="left",
            padx=(PremiumDesignSystem.SPACE_SM, 0)
        )
        
    def create_progress_section(self):
        """Create progress section"""
        self.progress_panel = ScanProgressPanel(self)
        self.progress_panel.grid(
            row=3,
            column=0,
            sticky="ew"
        )
        
    def create_results_section(self):
        """Create results section"""
        self.results_panel = ScanResultsPanel(self)
        self.results_panel.grid(
            row=4,
            column=0,
            sticky="ew"
        )
        
    def create_footer(self):
        """Create footer with back button"""
        footer_frame = customtkinter.CTkFrame(
            self,
            fg_color="transparent",
            height=60
        )
        footer_frame.grid(
            row=5,
            column=0,
            sticky="ew",
            pady=(PremiumDesignSystem.SPACE_LG, 0)
        )
        footer_frame.grid_propagate(False)
        
        back_button = customtkinter.CTkButton(
            footer_frame,
            text="← Back to Dashboard",
            command=self.go_back,
            **PremiumDesignSystem.get_button_style("secondary")
        )
        back_button.pack(pady=PremiumDesignSystem.SPACE_MD)
        
    def on_file_selected(self, filepath):
        """Handle file selection"""
        self.scan_button.configure(state="normal")
        
    def start_scan(self):
        """Start file scan"""
        if not self.drop_zone.selected_file:
            return
            
        self.progress_panel.show_progress()
        self.progress_panel.start_indeterminate("Initializing scan...")
        
        self.scan_button.configure(state="disabled", text="⏳ Scanning...")
        self.clear_button.configure(state="disabled")
        
        self.results_panel.hide_results()
        
        if self.scan_callback:
            self.scan_callback(self.drop_zone.selected_file)
            
    def clear_selection(self):
        """Clear file selection"""
        self.drop_zone.reset()
        self.scan_button.configure(state="disabled")
        self.progress_panel.hide_progress()
        self.results_panel.hide_results()
        
    def go_back(self):
        """Navigate back to dashboard"""
        if self.back_callback:
            self.back_callback()
            
    def set_scan_callback(self, callback):
        """Set scan callback"""
        self.scan_callback = callback
        
    def set_back_callback(self, callback):
        """Set back navigation callback"""
        self.back_callback = callback
        
    def update_progress(self, value, message=""):
        """Update scan progress"""
        self.progress_panel.set_progress(value, message)
        
    def show_scan_results(self, scan_result, filename):
        """Show scan results"""
        self.results_panel.show_results(scan_result, filename)
        
        self.scan_button.configure(state="normal", text="🔍 Scan File")
        self.clear_button.configure(state="normal")
        
        self.progress_panel.hide_progress()
        
    def show_scan_error(self, error_message):
        """Show scan error"""
        self.scan_button.configure(state="normal", text="🔍 Scan File")
        self.clear_button.configure(state="normal")
        self.progress_panel.hide_progress()