from manim import *
import numpy as np

CYAN = ManimColor("#00FFFF")


class ChendaAnimation(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0a0a0f"

        # --- Parameters ---
        R = 1.5       # radius of cylinder
        H = 2.8       # height of cylinder
        resolution = 40  # smoothness

        # ── Title ──────────────────────────────────────────────────────────────
        title = Text("ചെണ്ട  ·  Chenda", font_size=38, color=CYAN)
        #subtitle = Text("Kerala Percussion Instrument", font_size=20, color=WHITE)
        #subtitle.set_opacity(0.6)
        #VGroup(title, subtitle).arrange(DOWN, buff=0.2).to_edge(UP)

        #self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1)
        #self.play(FadeIn(subtitle), run_time=0.6)
        self.wait(0.4)

        # ── Camera setup ───────────────────────────────────────────────────────
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.18)

        # ─────────────────────────────────────────────────────────────────────
        # 1. WIREFRAME CYLINDER  (vertical line strips + top/bottom rings)
        # ─────────────────────────────────────────────────────────────────────
        n_lines = 20          # vertical wire lines
        n_rings = 6           # horizontal rings along the body

        wireframe_group = VGroup()

        # Vertical lines
        for i in range(n_lines):
            angle = i / n_lines * TAU
            x = R * np.cos(angle)
            y = R * np.sin(angle)
            line = Line3D(
                start=np.array([x, y, -H / 2]),
                end=np.array([x, y,  H / 2]),
                color=CYAN,
                thickness=0.012,
            )
            wireframe_group.add(line)

        # Horizontal rings
        for k in range(n_rings):
            z = -H / 2 + k / (n_rings - 1) * H
            ring_pts = [
                np.array([R * np.cos(t), R * np.sin(t), z])
                for t in np.linspace(0, TAU, resolution, endpoint=False)
            ]
            ring = VMobject(color=CYAN, stroke_width=1.6, stroke_opacity=0.55)
            ring.set_points_as_corners([*ring_pts, ring_pts[0]])
            wireframe_group.add(ring)

        self.play(
            *[Create(m, run_time=2) for m in wireframe_group],
            lag_ratio=0.04,
        )
        self.wait(0.5)

        # ─────────────────────────────────────────────────────────────────────
        # 2. DRUM HEADS  (top and bottom filled circles — fade in)
        # ─────────────────────────────────────────────────────────────────────
        def make_drum_head(z_val):
            head = Circle(radius=R, color=CYAN, fill_opacity=0, stroke_width=0)
            head.set_fill(CYAN, opacity=0)
            # Rotate into XY plane at height z_val
            # head.rotate(PI / 2, axis=RIGHT)
            head.move_to(np.array([0, 0, z_val]))
            return head

        top_head    = make_drum_head( H / 2)
        bottom_head = make_drum_head(-H / 2)

        self.add(top_head, bottom_head)
        self.play(
            top_head.animate.set_fill(CYAN, opacity=0.35).set_stroke(CYAN, width=2, opacity=0.9),
            bottom_head.animate.set_fill(CYAN, opacity=0.35).set_stroke(CYAN, width=2, opacity=0.9),
            run_time=1.8,
            rate_func=smooth,
        )
        self.wait(0.4)

        # ─────────────────────────────────────────────────────────────────────
        # 3. ROPE  (zigzag between top rim and bottom rim)
        #    Traditional Chenda: laces bind the two heads to the barrel
        # ─────────────────────────────────────────────────────────────────────
        n_zigzag = 36          # number of V-points (should be even)
        rope_color = "#f5c518"  # warm golden-yellow rope
        rope_radius = R + 0.05  # slightly outside the drum surface

        rope_points = []
        for i in range(n_zigzag + 1):
            frac = i / n_zigzag          # 0 → 1
            angle = frac * TAU * 1.5     # 1.5 loops so laces wrap around nicely
            # Alternate between top rim and bottom rim
            z = (H / 2 - 0.05) if (i % 2 == 0) else (-H / 2 + 0.05)
            x = rope_radius * np.cos(angle)
            y = rope_radius * np.sin(angle)
            rope_points.append(np.array([x, y, z]))

        rope = VMobject(color=rope_color, stroke_width=2.8, stroke_opacity=0.95)
        rope.set_points_as_corners(rope_points)

        self.play(Create(rope, run_time=3.5, rate_func=linear))
        self.wait(0.5)

        # ─────────────────────────────────────────────────────────────────────
        # 4. FINISHING TOUCHES — brief glow pulse on drum heads
        # ─────────────────────────────────────────────────────────────────────
        self.play(
            top_head.animate.set_fill(CYAN, opacity=0.65),
            bottom_head.animate.set_fill(CYAN, opacity=0.65),
            run_time=0.6, rate_func=there_and_back,
        )
        self.play(
            top_head.animate.set_fill(CYAN, opacity=0.35),
            bottom_head.animate.set_fill(CYAN, opacity=0.35),
            run_time=0.6,
        )

        # ─────────────────────────────────────────────────────────────────────
        # 5. Final slow rotation showcase
        # ─────────────────────────────────────────────────────────────────────
        self.wait(4)
        self.stop_ambient_camera_rotation()
