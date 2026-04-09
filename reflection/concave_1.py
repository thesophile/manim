
from scipy import optimize
from manim import *

class optics(Scene):
    def construct(self):
        mirror = Arc(radius=4, start_angle=-60*DEGREES, angle=120*DEGREES)
        self.add(mirror)

        m = ValueTracker(0)
        b = ValueTracker(0)

        def f(x):
            return np.array([x, m.get_value()*x + b.get_value(), 0])

        def opt(x):
            return np.linalg.norm(mirror.point_from_proportion(x[0]) - f(x[1]))

        rays = []
        reflections = []

        for y in np.linspace(start=-3, stop=3, num=15):
            b.set_value(y)
            intersect = optimize.minimize(opt, x0=[0, 0], bounds=[(0.01, 0.99), (-7, 7)], tol=1e-4)
            if intersect.success:
                dot = Dot().move_to(mirror.point_from_proportion(intersect.x[0]))
                self.add(dot)
                tplot = ParametricFunction(f, t_range=[-7, intersect.x[1]], color=YELLOW)
                rays.append(tplot)
                sec = Line(mirror.point_from_proportion(intersect.x[0] - 0.05),
                           mirror.point_from_proportion(intersect.x[0] + 0.05))
                angle = (sec.get_angle() - Line(tplot.get_start(), tplot.get_end()).get_angle())
                refl = tplot.copy().set_color(ORANGE).rotate(angle=-180*DEGREES + 2*angle,
                                                              about_point=tplot.get_end())
                reflections.append(refl.reverse_direction())

        # Animate all rays and reflections at once
        self.play(AnimationGroup(*[Create(ray) for ray in rays],
                                 lag_ratio=0),run_time=3)
                                 
        self.play(AnimationGroup(*[Create(reflection) for reflection in reflections],
                                 lag_ratio=0), run_time=3)
