"""
✨ PREMIUM ANIMATED WIDGETS
Advanced animated components with glassmorphism effects
"""

import customtkinter
import tkinter as tk
from tkinter import Canvas
import math
import time
from .design_system import PremiumDesignSystem, VisualEffects


class GlassProgressBar(customtkinter.CTkFrame):
    """
    ❄️ Premium Glass Progress Bar with Flowing Animation
    Features glassmorphism effect and smooth gradient animation
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            **VisualEffects.create_frost_effect(),
            height=12
        )
        
        self.progress_value = 0.0
        self.animation_running = False
        self.animation_offset = 0
        
        self.canvas = Canvas(
            self,
            height=8,
            highlightthickness=0,
            bg=PremiumDesignSystem.FROST_WHITE,
            bd=0
        )
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)
        
        self.canvas.bind('<Configure>', self.on_canvas_resize)
        
    def on_canvas_resize(self, event=None):
        """Handle canvas resize"""
        if hasattr(self, 'progress_value'):
            self.update_progress_visual()
    
    def set_progress(self, value):
        """Set progress with smooth animation"""
        if not 0.0 <= value <= 1.0:
            return
        self.progress_value = value
        self.update_progress_visual()
        
    def update_progress_visual(self):
        """Update progress bar with premium gradients"""
        self.canvas.delete("all")
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1:
            self.after(10, self.update_progress_visual)
            return
        
        self.canvas.create_rectangle(
            0, 0, width, height,
            fill=PremiumDesignSystem.FROST_MEDIUM,
            outline="",
            tags="background"
        )
        
        progress_width = int(width * self.progress_value)
        if progress_width > 0:
            segments = min(progress_width, 100)
            segment_width = progress_width / segments if segments > 0 else 0
            
            for i in range(segments):
                ratio = i / segments if segments > 0 else 0
                
                start_rgb = (30, 58, 138)
                end_rgb = (96, 165, 250)
                
                r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
                g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
                b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                x1 = i * segment_width
                x2 = (i + 1) * segment_width
                
                self.canvas.create_rectangle(
                    x1, 0, x2, height,
                    fill=color,
                    outline="",
                    tags="progress"
                )
    
    def start_indeterminate_animation(self):
        """Start flowing indeterminate animation"""
        if self.animation_running:
            return
        self.animation_running = True
        self.animate_flow()
        
    def animate_flow(self):
        """Create flowing wave animation"""
        if not self.animation_running:
            return
        
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width > 1:
            self.canvas.create_rectangle(
                0, 0, width, height,
                fill=PremiumDesignSystem.FROST_MEDIUM,
                outline=""
            )
            
            wave_width = 80
            wave_speed = 3
            self.animation_offset += wave_speed
            
            for layer in range(3):
                alpha_factor = 1.0 - (layer * 0.3)
                wave_x = (self.animation_offset + layer * 30) % (width + wave_width) - wave_width
                
                for i in range(wave_width):
                    alpha = math.sin(i * math.pi / wave_width) * alpha_factor
                    if alpha > 0:
                        base_color = [59, 130, 246]
                        intensity = int(255 * alpha)
                        
                        color = f"#{base_color[0]:02x}{base_color[1]:02x}{base_color[2]:02x}"
                        
                        x = wave_x + i
                        if 0 <= x < width:
                            self.canvas.create_line(
                                x, 0, x, height,
                                fill=color,
                                width=1
                            )
        
        self.after(50, self.animate_flow)
        
    def stop_animation(self):
        """Stop the flowing animation"""
        self.animation_running = False


class PremiumStatusIndicator(customtkinter.CTkFrame):
    """
    💎 Premium Status Indicator with Pulse Animation
    Beautiful status display with smooth state transitions
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.configure(
            **VisualEffects.create_elevated_card(),
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
        from .design_system import IconManager
        
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


class FloatingActionButton(customtkinter.CTkButton):
    """
    🌟 Premium Floating Action Button
    Elevated button with hover animations and premium styling
    """
    
    def __init__(self, parent, icon="", **kwargs):
        style = PremiumDesignSystem.get_button_style("primary")
        
        style.update({
            "width": 56,
            "height": 56,
            "corner_radius": 28,
            "text": icon,
            "font": customtkinter.CTkFont(size=20),
            "border_width": 0
        })
        
        final_style = {**style, **kwargs}
        
        super().__init__(parent, **final_style)
        
        self.bind("<Enter>", self.on_hover_enter)
        self.bind("<Leave>", self.on_hover_leave)
        
    def on_hover_enter(self, event):
        """Handle hover enter with smooth animation"""
        self.configure(
            fg_color=PremiumDesignSystem.ICE_ACCENT
        )
        
    def on_hover_leave(self, event):
        """Handle hover leave"""
        self.configure(
            fg_color=PremiumDesignSystem.ICE_PRIMARY
        )


class PremiumCard(customtkinter.CTkFrame):
    """
    💎 Premium Card Component with Advanced Styling
    Beautiful card with shadows, borders, and hover effects
    """
    
    def __init__(self, parent, elevated=False, hoverable=False, **kwargs):
        self.elevated = elevated
        self.hoverable = hoverable
        
        if elevated:
            card_style = VisualEffects.create_elevated_card()
        else:
            card_style = PremiumDesignSystem.get_card_style()
            
        card_style.update(kwargs)
        
        super().__init__(parent, **card_style)
        
        if hoverable:
            self.bind("<Enter>", self.on_hover_enter)
            self.bind("<Leave>", self.on_hover_leave)
            
    def on_hover_enter(self, event):
        """Handle card hover enter"""
        if self.hoverable:
            self.configure(
                border_color=PremiumDesignSystem.ICE_ACCENT,
                border_width=2
            )
            
    def on_hover_leave(self, event):
        """Handle card hover leave"""  
        if self.hoverable:
            self.configure(
                border_color=PremiumDesignSystem.BORDER_LIGHT,
                border_width=1
            )