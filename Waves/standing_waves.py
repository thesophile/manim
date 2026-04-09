from manim import *
import numpy as np

CYAN = ManimColor("#00FFFF")


class StandingWave(Scene):
    def construct(self):

        # ── Rectangle (portrait: height > width) ────────────────────────────
        rect_width  = 3.0
        rect_height = 5.0
        rectangle = Rectangle(
            width=rect_width,
            height=rect_height,
            color=CYAN,
            fill_color=ManimColor("#001A1A"),
            fill_opacity=0.3,
            stroke_width=3,
        )
        self.add(rectangle)

        top_y    =  rect_height / 2   #  2.5
        bottom_y = -rect_height / 2   # -2.5
        amp      =  0.35              # LOW amplitude (was ~1.3 before)

        # 2 spatial cycles fit inside the rectangle
        k = 2 * 2 * PI / rect_height
        n_pts = 400

        # ── wave builders ────────────────────────────────────────────────────

        def make_wave(ys, xs, opacity=1.0, width=2.5):
            pts = np.column_stack([xs, ys, np.zeros(len(ys))])
            p = VMobject(color=WHITE, stroke_width=width, stroke_opacity=opacity)
            p.set_points_smoothly(pts)
            return p

        # Incident: travels downward  → phase = k*y - ω*t  (ω*t increases → crests move down)
        def wave_down_full(phase, opacity=1.0, width=2.5):
            ys = np.linspace(top_y, bottom_y, n_pts)
            xs = amp * np.sin(k * ys - phase)
            return make_wave(ys, xs, opacity=opacity, width=width)

        # Reflected: travels upward   → phase = -(k*y + ω*t)
        def wave_up_full(phase, opacity=1.0, width=2.5):
            ys = np.linspace(top_y, bottom_y, n_pts)
            xs = amp * np.sin(-k * ys - phase)
            return make_wave(ys, xs, opacity=opacity, width=width)

        # Standing = superposition of both
        def wave_standing(phase, width=3.0):
            ys = np.linspace(top_y, bottom_y, n_pts)
            xs = amp * (np.sin(k * ys - phase) + np.sin(-k * ys - phase))
            return make_wave(ys, xs, width=width)

        # Wavefront mask: incident wave drawn only from top_y down to y_front
        def wave_down_partial(y_front, phase):
            ys = np.linspace(top_y, y_front, max(2, int(n_pts * abs(top_y - y_front) / rect_height)))
            xs = amp * np.sin(k * ys - phase)
            return make_wave(ys, xs)

        # Wavefront mask: reflected wave drawn only from bottom_y up to y_front
        def wave_up_partial(y_front, phase):
            ys = np.linspace(bottom_y, y_front, max(2, int(n_pts * abs(y_front - bottom_y) / rect_height)))
            xs = amp * np.sin(-k * ys - phase)
            return make_wave(ys, xs)

        # ════════════════════════════════════════════════════════════════════
        # STAGE 1 — Incident wave grows from top, travels to bottom
        #           The wavefront moves downward while the wave keeps moving
        # ════════════════════════════════════════════════════════════════════

        front_d = ValueTracker(top_y)
        phase_t = ValueTracker(0.0)   # single shared phase (ω*t)

        # During stage 1: incident partial (wavefront sweeping down)
        incident_partial = always_redraw(lambda: wave_down_partial(
            front_d.get_value(), phase_t.get_value()
        ))
        self.add(incident_partial)

        travel_time = 3.0
        total_phase_travel = k * rect_height   # phase accumulated over full height

        self.play(
            front_d.animate.set_value(bottom_y),
            phase_t.animate.set_value(total_phase_travel),
            run_time=travel_time,
            rate_func=linear,
        )

        # ════════════════════════════════════════════════════════════════════
        # STAGE 2 — Reflected wave grows from bottom upward
        #           Both waves keep traveling continuously
        # ════════════════════════════════════════════════════════════════════

        front_u = ValueTracker(bottom_y)

        # Switch incident to full (no longer a growing front)
        incident_full = always_redraw(lambda: wave_down_full(
            phase_t.get_value(), opacity=0.7, width=2.0
        ))
        reflected_partial = always_redraw(lambda: wave_up_partial(
            front_u.get_value(), phase_t.get_value()
        ))

        self.remove(incident_partial)
        self.add(incident_full, reflected_partial)

        phase_at_reflection_start = phase_t.get_value()

        self.play(
            front_u.animate.set_value(top_y),
            phase_t.animate.set_value(phase_at_reflection_start + total_phase_travel),
            run_time=travel_time,
            rate_func=linear,
        )

        # ════════════════════════════════════════════════════════════════════
        # STAGE 3 — Both waves fully present and continuously moving
        #           Standing wave emerges as their superposition
        # ════════════════════════════════════════════════════════════════════

        reflected_full = always_redraw(lambda: wave_up_full(
            phase_t.get_value(), opacity=0.7, width=2.0
        ))
        stand = always_redraw(lambda: wave_standing(phase_t.get_value(), width=3.0))

        self.remove(reflected_partial)
        self.add(reflected_full, stand)

        label = Text("Standing Wave", font_size=26, color=CYAN)
        label.next_to(rectangle, DOWN, buff=0.35)
        self.play(FadeIn(label), run_time=0.5)

        # Animate several oscillation cycles — all three waves moving together
        phase_now = phase_t.get_value()
        self.play(
            phase_t.animate.set_value(phase_now + 8 * PI),
            run_time=8,
            rate_func=linear,
        )

        # ════════════════════════════════════════════════════════════════════
        # STAGE 4 — Fade traveling waves; pure standing wave remains
        # ════════════════════════════════════════════════════════════════════

        self.play(FadeOut(incident_full), FadeOut(reflected_full), run_time=1.2)

        phase_now = phase_t.get_value()
        self.play(
            phase_t.animate.set_value(phase_now + 4 * PI),
            run_time=4,
            rate_func=linear,
        )

        self.wait(1)
