from manim import *
import numpy as np

ATOM_COLOR = BLUE_C
BOND_COLOR = BLUE_C
ELECTRON_COLOR = YELLOW
 

class TitleCard(Scene):
    def construct(self):
        title = Text("MODULE - 1 - ORGANIC CHEMISTRY - SOME BASIC CONCEPTS", font_size=48)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

class Introduction(Scene):
    def construct(self):
        # Heading 1: Organic chemistry definition
        heading = MarkupText("<b>Organic chemistry is the\nchemistry of carbon compounds.</b>", font_size=36)
        heading.to_edge(UP)
        self.play(Write(heading))
        # Show a big blue "C" that shrinks to a dot
        C = Text("C", font_size=96, color=BLUE)
        C.move_to(2*UP)
        self.play(FadeIn(C))
        self.play(C.animate.scale(0.08).move_to(ORIGIN))  # visually becomes small
        # Replace the shrunk C with a Dot (cyan)
        small_dot = Dot(point=ORIGIN, radius=0.08, color=ATOM_COLOR)
        self.play(Transform(C, small_dot))
        self.remove(C); self.add(small_dot)

        self.wait(0.5)

        # Change heading to catenation sentence
        new_heading = MarkupText(
            "<b>Carbon atoms have a tendency to form bonds between\ntheir own atoms to form long chains</b>",
            font_size=32
        )
        new_heading.to_edge(UP)
        self.play(Transform(heading, new_heading))

        # Create zig-zag chain (points) and animate dot moving while lines appear

        self.play(small_dot.animate.move_to(np.array([-2.8, 0, 0])), run_time=1)

        zig_points = [np.array([0,0,0])]
        length = 0.8
        for i in range(1,8):
            angle = (np.pi/6) * ((-1)**i)  # alternate up/down
            x = zig_points[-1][0] + length
            y = zig_points[-1][1] + length * np.tan(angle)
            zig_points.append(np.array([x, y, 0]))
        # shift left so centered
        offset = (zig_points[-1][0]/2) * RIGHT
        zig_points = [p - offset for p in zig_points]

        # create lines and small dots for atoms
        chain_lines = VGroup(*[Line(zig_points[i], zig_points[i+1], color=BOND_COLOR, stroke_width=4)
                               for i in range(len(zig_points)-1)])
        chain_dots = VGroup(*[Dot(p, radius=0.06, color=ATOM_COLOR) for p in zig_points])

        # animate: create lines one by one while moving a tracer dot along path
        tracer = Dot(zig_points[0], radius=0.07, color=ATOM_COLOR)
        self.add(tracer)
        for i, line in enumerate(chain_lines):
            self.play(Create(line), MoveAlongPath(tracer, line), Create(chain_dots[i+1]), run_time=0.6)
        self.remove(tracer)

        # Show catenation label under heading
        catenation = MarkupText("<i>This property is called <b>catenation</b></i>", font_size=28)
        catenation.next_to(heading, DOWN, buff=1)
        self.play(FadeIn(catenation))
        self.wait(2)
        
        self.play(FadeOut(chain_lines), FadeOut(chain_dots), FadeOut(small_dot), FadeOut(catenation))  # clear lower graphics

        # Replace heading and catenation with next statement
        heading2 = MarkupText("<b>Carbon atoms can form strong covalent bonds\nwith H, O, N, S and halogens.</b>",
                              font_size=30)
        heading2.to_edge(UP)
        self.play(Transform(heading, heading2))

        # Center C and draw five equally spaced bonds with labels
        center_C = Text("C", font_size=64, color=BLUE)
        center_C.move_to(DOWN*0.2)
        
        self.add(center_C)
        self.play(FadeIn(center_C))

        labels = ["H", "O", "N", "S", "halogens"]
        n = len(labels)
        radius = 1.6
        angles = np.linspace(90*DEGREES, 450*DEGREES, n, endpoint=False)  # start at top, spread equally

        bonds = VGroup()
        label_mobs = VGroup()
        for a, lab in zip(angles, labels):
            pos = center_C.get_center() + radius * np.array([np.cos(a), np.sin(a), 0])
            bond = Line(center_C.get_center(), pos, color=BOND_COLOR, stroke_width=4)
            label = Text(lab, font_size=28).move_to(pos + (0.25 * (pos - center_C.get_center())/np.linalg.norm(pos - center_C.get_center())))
            bonds.add(bond)
            label_mobs.add(label)

        # Animate drawing bonds and labels sequentially
        for b, l in zip(bonds, label_mobs):
            self.play(Create(b), Write(l), run_time=0.5)

        # final pause as requested
        self.wait(2)


from manim import *

ATOM_COLOR = BLUE_C
BOND_COLOR = BLUE_C

class Fundamental_Title(Scene):
    def construct(self):
        heading = MarkupText(
            "<b>FUNDAMENTAL CONCEPTS OF\nORGANIC REACTION MECHANISMS</b>",
            font_size=32
        )
        self.play(Write(heading))
        self.wait(1)

        # Move to top-left and scale down at the same time
        self.play(
            heading.animate.scale(0.4).to_corner(UL, buff=0.3),
            run_time=2
        )
        self.wait(1)
 

        


class Fundamental_SubstrateToProduct(Scene):
    def construct(self):
        heading = MarkupText(
            "<b>FUNDAMENTAL CONCEPTS OF\nORGANIC REACTION MECHANISMS</b>",
            font_size=32
        )
        heading.scale(0.4).to_corner(UL, buff=0.3)
        self.add(heading)

        substrate_box = RoundedRectangle(corner_radius=0.2, width=3, height=1.2)
        substrate_label = Text("Substrate\n(organic molecule)", font_size=26)
        substrate_group = VGroup(substrate_box, substrate_label).arrange(DOWN, buff=0.1)
        substrate_group.to_edge(LEFT).shift(1.5 * DOWN)

        reagent_circle = Circle(radius=0.5)
        reagent_label = Text("Attacking\nreagent", font_size=24)
        reagent_group = VGroup(reagent_circle, reagent_label).arrange(DOWN, buff=0.2)
        reagent_group.next_to(substrate_group, UP, buff=0.8)

        intermediate_box = RoundedRectangle(corner_radius=0.2, width=3, height=1.2)
        intermediate_label = Text("[Intermediate]", font_size=26)
        intermediate_group = VGroup(intermediate_box, intermediate_label).arrange(DOWN, buff=0.1)
        intermediate_group.next_to(substrate_group, RIGHT, buff=2)

        product_box = RoundedRectangle(corner_radius=0.2, width=3, height=1.2)
        product_label = Text("Products", font_size=26)
        product_group = VGroup(product_box, product_label).arrange(DOWN, buff=0.1)
        product_group.next_to(intermediate_group, RIGHT, buff=2)

        arrow1 = Arrow(substrate_group.get_right(), intermediate_group.get_left(), buff=0.2)
        arrow2 = Arrow(intermediate_group.get_right(), product_group.get_left(), buff=0.2)

        # self.add(substrate_group, reagent_group, intermediate_group, product_group, arrow1, arrow2)  # Pre-add to avoid animation issues
        self.play(FadeIn(substrate_group), FadeIn(reagent_group))
        self.play(Create(arrow1), FadeIn(intermediate_group))
        self.play(Create(arrow2), FadeIn(product_group))

        bullet = MarkupText(
            "Substrate reacts with an attacking reagent →\n"
            "forms an <b>intermediate</b> and finally <b>products</b>.",
            font_size=26
        ).next_to(intermediate_box, UP, buff=1)
        bullet.move_to(RIGHT*1.5 + UP*1)
        self.play(FadeIn(bullet))
        self.wait(5)

A = Dot(color=ATOM_COLOR).shift(2 * LEFT + 0.5 * DOWN)
B = Dot(color=ATOM_COLOR).shift(2 * RIGHT + 0.5 * DOWN)

bullet2 = MarkupText(
    "<b>Curved arrows show movement of electrons,</b>\n"
    "not the movement of atoms.",
    font_size=26
).shift(UP * 2)

bullet3 = MarkupText(
    "<b>Full arrowhead:</b> movement of <b>two</b> electrons\n"
    "<b>Half-headed arrow:</b> movement of <b>one</b> electron.",
    font_size=26
).shift(UP * 2)

heading = MarkupText(
    "<b>FUNDAMENTAL CONCEPTS OF\nORGANIC REACTION MECHANISMS</b>",
    font_size=32
)
heading.scale(0.4).to_corner(UL, buff=0.3)

electrons = VGroup(
    Dot(A.get_center() + 0.3 * UP, radius=0.05),
    Dot(A.get_center() + 0.15 * UP + 0.15 * RIGHT, radius=0.05),
)

curved_arrow = CurvedArrow(
    A.get_center() + 0.3 * UP,
    B.get_center() + 0.3 * UP,
    radius=2
)

bond = Line(A.get_center(), B.get_center(), color=BOND_COLOR, stroke_width=4)

class Fundamental_CurvedArrows(Scene):
    def construct(self):

        self.add(heading)
        # Curved arrows = electrons move, not atoms
        self.play(FadeIn(bullet2))

        self.play(Create(A), Create(B), Create(bond))
        self.play(FadeIn(electrons))
        self.play(Create(curved_arrow))
        self.play(electrons.animate.shift(4 * RIGHT), run_time=1.5)
        self.wait(1)
        self.play(*map(FadeOut, [A, B, bond, electrons, curved_arrow]))
        self.wait(1)

class Fundamental_CurvedArrows2(Scene):
    def construct(self):
        # Full vs half-headed

        self.add(heading)

        self.play(Transform(bullet2, bullet3))

        # Tail and electron pair (first two dots appear)
        tail1 = Dot(5 * LEFT + 0.5 * DOWN, radius=0.05)
        e_pair = VGroup(
            Dot(tail1.get_center() + 0.2 * DOWN + 0.12 * LEFT, radius=0.04),
            Dot(tail1.get_center() + 0.2 * DOWN + 0.12 * RIGHT, radius=0.04),
        )

        self.play(FadeIn(e_pair))

        # Full arrow (arrow1) from tail1 to head
        full_arrow = CurvedArrow(
            tail1.get_center(),
            tail1.get_center() + 3 * RIGHT,
            radius=-1.5
        )
        label_full = Text("2 electrons", font_size=24).next_to(full_arrow, DOWN, buff=0.3)

        self.play(Create(full_arrow), FadeIn(label_full))

        self.play(e_pair.animate.shift(3 * RIGHT), run_time=1.5)

        tail2 = Dot(2 * RIGHT + 0.5 * DOWN, radius=0.05)
        single_e = Dot(tail2.get_center() + 0.2 * DOWN, radius=0.04)

        self.play(FadeIn(single_e))

        # half arrow (arrow1) from tail1 to head
        half_arrow = CurvedArrow(
            tail2.get_center(),
            tail2.get_center() + 3 * RIGHT,
            radius=-1.5,
            tip_length=0,   # remove built-in tip
        )
        # Compute tangent at the end
        points = half_arrow.get_points()
        tangent_vector = points[-1] - points[-2]
        angle = np.arctan2(tangent_vector[1], tangent_vector[0])

        # Create a vertical half-triangle tip at origin
        tip = Polygon(
            [0, 0, 0],        # tip
            [-0.15, 0.15, 0], # top-left (half of base)
            [-0.15, 0, 0]     # bottom-left (half of base)
        ).set_fill(WHITE, opacity=1).set_stroke(width=0)

        # Rotate tip along tangent
        tip.rotate(angle, about_point=tip.get_vertices()[0])

        # Move tip to the arrow end
        tip.shift(half_arrow.get_end() - tip.get_vertices()[0])

        # self.add(tip)

        label_half = Text("1 electron", font_size=24).next_to(half_arrow, DOWN, buff=0.3)

        self.play(Create(half_arrow),Create(tip), FadeIn(label_half))

        self.play(single_e.animate.shift(3 * RIGHT), run_time=1.5)

        self.wait(2)






 