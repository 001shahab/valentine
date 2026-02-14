#!/usr/bin/env python3
"""
💕  Mathematical Valentine's Heart Animation  💕
═══════════════════════════════════════════════════

A beautiful animated visualization of the mathematical heart curve:

    y = |x|^(2/3) + 0.9 · sin(kx) · √(3 − x²)

As k increases from 0 to 50, a simple arch transforms
into a stunning, oscillating heart shape.

Created with love by Prof. Shahab Anbarjafari
3S Holding OÜ  |  Tartu, Estonia
Contact: shb@3sholding.com

Usage:
    python valentine.py

Controls:
    SPACE   –  Pause / Resume
    R       –  Restart animation
    UP/DOWN –  Speed up / slow down
    Q / ESC –  Quit
"""

# ═══════════════════════════════════════════════════════════════════════
# I import my essential libraries here.
# NumPy handles the math, Matplotlib brings the visuals to life.
# ═══════════════════════════════════════════════════════════════════════

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyBboxPatch
import matplotlib.patheffects as path_effects
import itertools
import sys


class ValentineHeart:
    """
    I am the heart of this project — pun absolutely intended.

    I animate the mathematical heart curve, transforming a gentle
    arch into a beautiful oscillating heart shape over time.

    Created by Prof. Shahab Anbarjafari
    3S Holding OÜ, Tartu, Estonia
    """

    # ─── My animation parameters ─────────────────────────────────────
    K_FINAL = 50              # I push k all the way to 50 for a richly detailed heart
    NUM_POINTS = 3000         # I want my curve silky smooth
    BUILD_FRAMES = 100        # I build the heart over this many frames
    PULSE_FRAMES = 60         # I pulse the completed heart for this many frames
    INITIAL_FPS = 3           # I start the heart animation at 3 FPS as requested
    SPLASH_FPS = 15           # I use a smoother FPS for the splash screen button glow

    # ─── My color palette — dark romantic aesthetic ──────────────────
    COLORS = {
        'bg':           '#0a0a0a',  # Deep dark background, almost black
        'heart':        '#ff1744',  # Vibrant red for the main heart line
        'heart_glow':   '#ff4444',  # Softer red for the glow layers
        'title':        '#ff1744',  # Bold red for the title
        'title_shadow': '#660000',  # Dark red shadow behind the title
        'formula':      '#bbbbbb',  # Light gray for the formula text
        'k_value':      '#ff6e7f',  # Warm pink for the live k readout
        'axis':         '#333333',  # Subtle gray for the axes
        'grid':         '#1a1a1a',  # Very faint grid lines
        'info':         '#444444',  # Dim text for the controls hint
        'credit':       '#333333',  # Very subtle credit text
        'message':      '#ff6e7f',  # Warm pink for the final message
        'btn_face':     '#cc1133',  # Rich red for the start button
        'btn_hover':    '#ff2255',  # Brighter red when hovering the button
        'btn_glow':     '#ff1744',  # Glow halo around the start button
        'btn_edge':     '#ff4466',  # Button border color
        'btn_text':     '#ffffff',  # White text on the button
        'splash_sub':   '#ff6e7f',  # Warm pink for the splash subtitle
        'splash_hint':  '#555555',  # Dim hint text on splash screen
    }

    def __init__(self):
        """
        I set up everything I need for the animation: the math,
        the figure, the plot elements, and the keyboard events.
        """
        # I create my x-axis data points spanning the valid domain.
        # My formula requires 3 - x² ≥ 0, so x must live in [-√3, √3].
        self.x = np.linspace(-np.sqrt(3), np.sqrt(3), self.NUM_POINTS)

        # I track my animation state internally
        self._frame = 0
        self._paused = False
        self._fps = self.INITIAL_FPS
        self._completed = False   # I flip this when the build phase finishes
        self._started = False     # I wait for the user to press Start
        self._splash_tick = 0     # I use this to pulse the start button
        self._hovering_btn = False  # I track whether the mouse is over the button

        # I build all visual elements
        self._create_figure()
        self._create_plot_elements()
        self._create_start_screen()
        self._connect_events()

    # ═══════════════════════════════════════════════════════════════
    #  Mathematical Core
    # ═══════════════════════════════════════════════════════════════

    def _heart_curve(self, k, amplitude=0.9):
        """
        I compute my beloved heart curve:

            y = |x|^(2/3) + amplitude · sin(kx) · √(3 − x²)

        The |x|^(2/3) term creates the foundational arch shape.
        The sin(kx) term adds oscillations that sculpt the heart.
        The √(3 − x²) term constrains everything within the domain.

        Parameters:
            k         : Controls oscillation frequency (0 → 50)
            amplitude : Wave amplitude (default 0.9, I modulate it for pulsing)

        Returns:
            y values for every point on my x-axis
        """
        base = np.abs(self.x) ** (2.0 / 3.0)
        wave = amplitude * np.sin(k * self.x)
        envelope = np.sqrt(np.maximum(0.0, 3.0 - self.x ** 2))
        return base + wave * envelope

    @staticmethod
    def _ease_in_out(t):
        """
        I use smooth Hermite interpolation for cinematic easing.
        This makes the build-up start slowly, accelerate through
        the middle, and decelerate gracefully at the end.

            f(t) = 3t² − 2t³    for t ∈ [0, 1]

        It's a classic trick from computer graphics that I love.
        """
        t = np.clip(t, 0.0, 1.0)
        return t * t * (3.0 - 2.0 * t)

    # ═══════════════════════════════════════════════════════════════
    #  Visual Setup
    # ═══════════════════════════════════════════════════════════════

    def _create_figure(self):
        """
        I carefully craft my figure and axes to achieve the dark,
        romantic aesthetic that matches the original inspiration.
        """
        # I create a generously sized figure with a dark background
        self.fig = plt.figure(
            figsize=(10, 9),
            facecolor=self.COLORS['bg'],
        )

        # I try to set a nice window title (some backends may not support this)
        try:
            self.fig.canvas.manager.set_window_title(
                '💕 Mathematical Valentine — Prof. Shahab Anbarjafari'
            )
        except AttributeError:
            pass

        # I leave room above for the title and below for the formula
        self.fig.subplots_adjust(left=0.08, right=0.95, bottom=0.14, top=0.84)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(self.COLORS['bg'])

        # I frame the view to show the heart nicely
        self.ax.set_xlim(-2.1, 2.1)
        self.ax.set_ylim(-1.5, 2.8)

        # I style the axes to be subtle but present
        for spine in ('bottom', 'left'):
            self.ax.spines[spine].set_color(self.COLORS['axis'])
            self.ax.spines[spine].set_linewidth(0.8)
        for spine in ('top', 'right'):
            self.ax.spines[spine].set_visible(False)

        self.ax.tick_params(
            colors=self.COLORS['axis'],
            labelsize=9,
            length=4,
            width=0.8,
        )

        # I add a very subtle grid for reference
        self.ax.grid(
            True,
            color=self.COLORS['grid'],
            linewidth=0.5,
            alpha=0.6,
        )

    def _create_plot_elements(self):
        """
        I create all the visual elements that make this animation
        shine: the heart curve with neon glow, the title, the live
        formula display, and credits.
        """
        # ─── The Heart Curve (with neon glow effect) ─────────────
        # I draw the curve three times at different widths and
        # opacities to create a beautiful neon glow effect.

        # Layer 1 — Outer glow: wide, very transparent
        self._glow_outer, = self.ax.plot(
            [], [],
            color=self.COLORS['heart_glow'],
            linewidth=8,
            alpha=0.1,
            solid_capstyle='round',
        )

        # Layer 2 — Inner glow: medium, semi-transparent
        self._glow_inner, = self.ax.plot(
            [], [],
            color=self.COLORS['heart_glow'],
            linewidth=4,
            alpha=0.25,
            solid_capstyle='round',
        )

        # Layer 3 — Core line: thin, nearly opaque
        self._core_line, = self.ax.plot(
            [], [],
            color=self.COLORS['heart'],
            linewidth=1.8,
            alpha=0.95,
            solid_capstyle='round',
        )

        # I group them for easy batch updates
        self._curve_layers = [
            self._glow_outer,
            self._glow_inner,
            self._core_line,
        ]

        # ─── Title: "Happy Valentine's!" ─────────────────────────
        # I give the title a text-stroke glow to make it pop
        self._title = self.fig.text(
            0.5, 0.92,
            "Happy Valentine's!",
            fontsize=34,
            fontweight='bold',
            fontfamily='serif',
            color=self.COLORS['title'],
            ha='center',
            va='center',
            path_effects=[
                path_effects.withStroke(
                    linewidth=5,
                    foreground=self.COLORS['title_shadow'],
                ),
                path_effects.Normal(),
            ],
        )

        # ─── Mathematical Formula ────────────────────────────────
        # I display the formula so everyone can appreciate the math
        self._formula = self.fig.text(
            0.5, 0.065,
            r'$y \;=\; x^{\,2/3} \;+\; 0.9\;\sin(kx)\;\sqrt{3 - x^2}$',
            fontsize=17,
            color=self.COLORS['formula'],
            ha='center',
            va='center',
        )

        # ─── Live k Value Display ────────────────────────────────
        # I show the current k value so viewers can follow along
        self._k_display = self.fig.text(
            0.5, 0.022,
            'k = 0.00',
            fontsize=15,
            fontweight='bold',
            color=self.COLORS['k_value'],
            ha='center',
            va='center',
        )

        # ─── Completion / Status Message ─────────────────────────
        # I keep this hidden until the heart is fully built
        self._message = self.fig.text(
            0.5, 0.86,
            '',
            fontsize=13,
            fontfamily='serif',
            fontstyle='italic',
            color=self.COLORS['message'],
            ha='center',
            va='center',
            alpha=0,
        )

        # ─── Controls Hint (bottom-right) ────────────────────────
        self.fig.text(
            0.97, 0.004,
            '[SPACE] Pause   [R] Restart   [↑↓] Speed   [Q] Quit',
            fontsize=7.5,
            color=self.COLORS['info'],
            ha='right',
            va='bottom',
        )

        # ─── Author Credit (bottom-left) ─────────────────────────
        self.fig.text(
            0.03, 0.004,
            'Prof. Shahab Anbarjafari  •  3S Holding OÜ  •  Tartu, Estonia',
            fontsize=7.5,
            color=self.COLORS['credit'],
            ha='left',
            va='bottom',
        )

    # ═══════════════════════════════════════════════════════════════
    #  Start Screen
    # ═══════════════════════════════════════════════════════════════

    def _create_start_screen(self):
        """
        I create a beautiful splash screen with a glowing Start
        button so the user can begin the animation when they're ready.
        The button pulses with a soft neon glow to invite a click.
        """
        # I keep a list of all splash-only elements so I can
        # cleanly remove them when the animation starts.
        self._splash_elements = []

        # ─── Romantic subtitle beneath the title ─────────────────
        sub = self.fig.text(
            0.5, 0.87,
            'A Mathematical Love Letter',
            fontsize=15,
            fontfamily='serif',
            fontstyle='italic',
            color=self.COLORS['splash_sub'],
            ha='center',
            va='center',
            alpha=0.85,
        )
        self._splash_elements.append(sub)

        # ─── Start Button — Outer Glow Halo ──────────────────────
        # I draw a slightly larger, soft-edged rectangle behind
        # the button to create the characteristic neon glow.
        glow_w, glow_h = 0.28, 0.10
        self._btn_glow = FancyBboxPatch(
            (0.5 - glow_w / 2, 0.46 - glow_h / 2),
            glow_w, glow_h,
            boxstyle='round,pad=0.025',
            facecolor=self.COLORS['btn_glow'],
            edgecolor='none',
            alpha=0.12,
            transform=self.fig.transFigure,
            zorder=9,
        )
        self.fig.patches.append(self._btn_glow)
        self._splash_elements.append(self._btn_glow)

        # ─── Start Button — Main Body ────────────────────────────
        # I use a FancyBboxPatch with rounded corners for that
        # modern, pill-shaped button look.
        btn_w, btn_h = 0.22, 0.07
        self._btn_patch = FancyBboxPatch(
            (0.5 - btn_w / 2, 0.46 - btn_h / 2),
            btn_w, btn_h,
            boxstyle='round,pad=0.018',
            facecolor=self.COLORS['btn_face'],
            edgecolor=self.COLORS['btn_edge'],
            linewidth=2,
            alpha=0.95,
            transform=self.fig.transFigure,
            zorder=10,
        )
        self.fig.patches.append(self._btn_patch)
        self._splash_elements.append(self._btn_patch)

        # ─── Start Button — Label ────────────────────────────────
        btn_label = self.fig.text(
            0.5, 0.46,
            '♥   S t a r t',
            fontsize=21,
            fontweight='bold',
            color=self.COLORS['btn_text'],
            ha='center',
            va='center',
            zorder=11,
            path_effects=[
                path_effects.withStroke(
                    linewidth=2,
                    foreground='#aa0022',
                ),
                path_effects.Normal(),
            ],
        )
        self._splash_elements.append(btn_label)

        # ─── Hint text below the button ──────────────────────────
        hint = self.fig.text(
            0.5, 0.39,
            'click the button to begin the magic',
            fontsize=10,
            fontstyle='italic',
            color=self.COLORS['splash_hint'],
            ha='center',
            va='center',
        )
        self._splash_elements.append(hint)

    def _remove_start_screen(self):
        """
        I cleanly remove all splash screen elements so the
        animation canvas is clear and ready to draw the heart.
        """
        for element in self._splash_elements:
            # Patches live in fig.patches, text lives in fig.texts
            if isinstance(element, FancyBboxPatch):
                if element in self.fig.patches:
                    self.fig.patches.remove(element)
            else:
                element.remove()
        self._splash_elements.clear()

    def _is_over_button(self, event):
        """
        I check whether the mouse cursor is inside the start
        button area. I use figure-coordinate hit testing.
        """
        if event.x is None or event.y is None:
            return False
        # I convert pixel coordinates to figure-relative [0, 1]
        fig_xy = self.fig.transFigure.inverted().transform(
            (event.x, event.y)
        )
        fx, fy = fig_xy
        # My button is centered at (0.5, 0.46) with size (0.22, 0.07)
        return (0.5 - 0.13) <= fx <= (0.5 + 0.13) and \
               (0.46 - 0.045) <= fy <= (0.46 + 0.045)

    def _start_animation(self):
        """
        I am called when the user clicks Start. I tear down the
        splash screen and kick off the heart-building animation.
        """
        self._started = True
        self._remove_start_screen()

        # I switch from the smooth splash FPS to the requested 3 FPS
        if hasattr(self, '_anim') and self._anim.event_source:
            self._anim.event_source.interval = 1000 // self._fps

        self.fig.canvas.draw_idle()

    def _connect_events(self):
        """
        I wire up keyboard, mouse click, and mouse motion events
        so the user can interact with me at every stage.
        """
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
        self.fig.canvas.mpl_connect('button_press_event', self._on_click)
        self.fig.canvas.mpl_connect('motion_notify_event', self._on_motion)

    # ═══════════════════════════════════════════════════════════════
    #  Animation Engine
    # ═══════════════════════════════════════════════════════════════

    def _update(self, _tick):
        """
        I am called once per frame by matplotlib's animation system.
        I handle three distinct phases:

            Splash   : Pulsing Start button, waiting for user
            Building : k ramps from 0 → 50 with cinematic easing
            Pulsing  : k = 50, gentle breathing effect
        """
        # ─── Splash Screen Phase ─────────────────────────────────
        # If the user hasn't clicked Start yet, I just pulse the
        # button glow to make it feel alive and inviting.
        if not self._started:
            self._splash_tick += 1
            # I create a smooth sine pulse for the glow intensity
            pulse = 0.08 + 0.14 * np.sin(
                2.0 * np.pi * self._splash_tick / 30.0
            )
            self._btn_glow.set_alpha(max(0.0, pulse))
            self.fig.canvas.draw_idle()
            return

        # ─── Paused State ────────────────────────────────────────
        # If I'm paused, I do nothing — the display freezes in place
        if self._paused:
            return

        frame = self._frame

        if frame < self.BUILD_FRAMES:
            # ─── Phase 1: Building the Heart ─────────────────────
            # I map the current frame to a progress value [0, 1]
            t = frame / max(1, self.BUILD_FRAMES - 1)

            # I apply cinematic easing so the build feels dramatic
            k = self.K_FINAL * self._ease_in_out(t)
            amplitude = 0.9

            # I fade the curve in gradually as it forms
            alpha_factor = 0.4 + 0.6 * t

            # I haven't finished building yet
            self._completed = False

        else:
            # ─── Phase 2: Pulsing / Breathing ────────────────────
            pulse_idx = frame - self.BUILD_FRAMES
            k = self.K_FINAL

            # I modulate the amplitude slightly to create a
            # gentle "breathing" effect — the heart is alive!
            breath = np.sin(2.0 * np.pi * pulse_idx / 20.0)
            amplitude = 0.9 + 0.035 * breath

            alpha_factor = 1.0

            # I reveal the completion message the first time
            if not self._completed:
                self._completed = True
                self._message.set_text('Made with ♥ and Mathematics')
                self._message.set_alpha(0.7)

        # ─── I compute the curve and update all layers ───────────
        y = self._heart_curve(k, amplitude)

        for layer in self._curve_layers:
            layer.set_data(self.x, y)

        # I adjust opacity for the fade-in during the build phase
        self._core_line.set_alpha(0.95 * alpha_factor)
        self._glow_inner.set_alpha(0.25 * alpha_factor)
        self._glow_outer.set_alpha(0.10 * alpha_factor)

        # I update the live k readout
        self._k_display.set_text(f'k = {k:.2f}')

        # I advance my frame counter
        self._frame += 1

        # After the pulse cycle ends, I loop back to keep pulsing
        if self._frame >= self.BUILD_FRAMES + self.PULSE_FRAMES:
            self._frame = self.BUILD_FRAMES

        # I ask matplotlib to refresh the canvas
        self.fig.canvas.draw_idle()

    # ═══════════════════════════════════════════════════════════════
    #  Interactivity
    # ═══════════════════════════════════════════════════════════════

    def _on_click(self, event):
        """
        I handle mouse clicks. Before the animation starts, I check
        if the user clicked my beautiful Start button.
        """
        if not self._started:
            if self._is_over_button(event):
                self._start_animation()

    def _on_motion(self, event):
        """
        I handle mouse movement to create a hover effect on the
        Start button — it brightens when the cursor is over it,
        making it feel responsive and inviting.
        """
        if not self._started:
            over = self._is_over_button(event)
            if over and not self._hovering_btn:
                # I light up the button when the mouse enters
                self._hovering_btn = True
                self._btn_patch.set_facecolor(self.COLORS['btn_hover'])
                self._btn_patch.set_alpha(1.0)
                self._btn_patch.set_linewidth(2.5)
                self.fig.canvas.draw_idle()
            elif not over and self._hovering_btn:
                # I dim the button back to normal when the mouse leaves
                self._hovering_btn = False
                self._btn_patch.set_facecolor(self.COLORS['btn_face'])
                self._btn_patch.set_alpha(0.95)
                self._btn_patch.set_linewidth(2.0)
                self.fig.canvas.draw_idle()

    def _on_key_press(self, event):
        """
        I handle keyboard input to make the experience interactive.
        Because what's a Valentine without a bit of interactivity?
        """
        # If we're on the splash screen, Enter or Space can also start
        if not self._started:
            if event.key in (' ', 'enter'):
                self._start_animation()
            elif event.key in ('q', 'escape'):
                plt.close('all')
            return

        if event.key == ' ':
            # I toggle pause / resume
            self._paused = not self._paused
            if self._paused:
                self._message.set_text('⏸  Paused — press SPACE to continue')
                self._message.set_alpha(0.6)
            else:
                if self._completed:
                    self._message.set_text('Made with ♥ and Mathematics')
                    self._message.set_alpha(0.7)
                else:
                    self._message.set_text('')
                    self._message.set_alpha(0)
            self.fig.canvas.draw_idle()

        elif event.key == 'r':
            # I restart the entire animation from scratch
            self._frame = 0
            self._completed = False
            self._paused = False
            self._message.set_text('')
            self._message.set_alpha(0)
            # I clear the curves so the restart feels clean
            for layer in self._curve_layers:
                layer.set_data([], [])
            self._k_display.set_text('k = 0.00')
            self.fig.canvas.draw_idle()

        elif event.key in ('q', 'escape'):
            # I gracefully close everything and exit
            plt.close('all')

        elif event.key == 'up':
            # I increase the animation speed (capped at 30 FPS)
            self._fps = min(30, self._fps + 1)
            if hasattr(self, '_anim') and self._anim.event_source:
                self._anim.event_source.interval = 1000 // self._fps

        elif event.key == 'down':
            # I decrease the animation speed (minimum 1 FPS)
            self._fps = max(1, self._fps - 1)
            if hasattr(self, '_anim') and self._anim.event_source:
                self._anim.event_source.interval = 1000 // self._fps

    # ═══════════════════════════════════════════════════════════════
    #  Entry Point
    # ═══════════════════════════════════════════════════════════════

    def run(self):
        """
        I start the show! The window opens with a beautiful Start
        button. Once the user clicks it, the heart animation begins
        at 3 FPS. Speed is adjustable with UP/DOWN arrow keys.
        """
        # I start the timer at the splash-screen FPS so the
        # button glow pulses smoothly. When the user clicks Start,
        # I switch to the requested 3 FPS for the heart animation.
        self._anim = FuncAnimation(
            self.fig,
            self._update,
            frames=itertools.count(),       # I generate frames forever
            interval=1000 // self.SPLASH_FPS,  # Smooth splash pulsing
            blit=False,                     # I need full redraws for text updates
            cache_frame_data=False,         # I don't need frame caching
        )

        # I show the window — this blocks until the user closes it
        plt.show()


# ═════════════════════════════════════════════════════════════════════
#  I start the animation when this script is run directly.
# ═════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # I greet the user with a warm console message
    print()
    print("  ╔═══════════════════════════════════════════════════════╗")
    print("  ║        💕  Mathematical Valentine's Heart  💕        ║")
    print("  ║                                                       ║")
    print("  ║   Created by Prof. Shahab Anbarjafari                 ║")
    print("  ║   3S Holding OÜ  |  Tartu, Estonia                   ║")
    print("  ║   Contact: shb@3sholding.com                         ║")
    print("  ║                                                       ║")
    print("  ║   Controls:                                           ║")
    print("  ║     START ··· Click the button or press SPACE/ENTER   ║")
    print("  ║     SPACE ··· Pause / Resume                          ║")
    print("  ║     R ······· Restart animation                       ║")
    print("  ║     ↑ / ↓ ·· Speed up / slow down                    ║")
    print("  ║     Q / ESC · Quit                                    ║")
    print("  ╚═══════════════════════════════════════════════════════╝")
    print()

    # I create and launch my Valentine heart animation
    heart = ValentineHeart()
    heart.run()
