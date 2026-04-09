from manim import *
import numpy as np

class TangentHalfHeadedArrow(Scene):
    def construct(self):
        tail2 = Dot(LEFT*2)
        self.add(tail2)

        # Main curved arrow without tip
        arrow_line = CurvedArrow(
            tail2.get_center(),
            tail2.get_center() + 3 * RIGHT,
            radius=-1.5,
            tip_length=0,   # remove built-in tip
            color=BLUE
        )
        self.add(arrow_line)

        # Compute tangent at the end
        points = arrow_line.get_points()
        tangent_vector = points[-1] - points[-2]
        angle = np.arctan2(tangent_vector[1], tangent_vector[0])

        # Create a vertical half-triangle tip at origin
        tip = Polygon(
            [0, 0, 0],        # tip
            [-0.15, 0.15, 0], # top-left (half of base)
            [-0.15, 0, 0]     # bottom-left (half of base)
        ).set_fill(BLUE, opacity=1).set_stroke(width=0)

        # Rotate tip along tangent
        tip.rotate(angle, about_point=tip.get_vertices()[0])

        # Move tip to the arrow end
        tip.shift(arrow_line.get_end() - tip.get_vertices()[0])

        self.add(tip)
        self.wait()
