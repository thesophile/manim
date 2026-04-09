

class Plane_mirror(Scene):
    def construct(self):
        mirror= Line(4*LEFT,4*RIGHT).shift(DOWN*2)
        mirror_lines = VGroup()
        for i in range(17):
            mirror_line = Line(mirror.get_start(), mirror.get_start()+0.5*DOWN)
            mirror_line.rotate(-30*DEGREES, about_point=mirror.get_start())
            mirror_line.shift(0.5*i*RIGHT)
            mirror_lines.add(mirror_line)

        normal = DashedLine(UP,DOWN*3).shift(UP)
        dot = Dot(point=DOWN*2)

        m_label = Text("Plane mirror", font_size=30).next_to(mirror.get_end())
        n_label = Text("Normal", font_size=30).next_to(normal.get_start(),LEFT)

        incident_ray = Arrow(start=LEFT*6, end=dot.get_center(), buff = 0,color=BLUE)
        incident_ray.rotate(-10*DEGREES, about_point=dot.get_center())
        i_label = Text("incident ray",font_size=30).next_to(incident_ray.get_start(), RIGHT)


        reflected_ray= Arrow(start= dot.get_center() , end=RIGHT*6, buff = 0,color=GOLD)
        r_label = Text("reflected ray",font_size=30).next_to(reflected_ray.get_end(), LEFT)

        reflected_ray.rotate(10*DEGREES, about_point=dot.get_center())

        angle_radius = 0.8

        i_angle = Angle(incident_ray, normal, radius=angle_radius, quadrant=(-1,-1),other_angle=True, color= BLUE)
        r_angle = Angle(reflected_ray, normal, radius=angle_radius, quadrant=(1,-1),other_angle=False, color=GOLD)


        def i_angle_updater(mob):
            new_angle = Angle(incident_ray, normal, radius=angle_radius, quadrant=(-1,-1), other_angle=True, color = BLUE)
            mob.become(new_angle)

        def r_angle_updater(mob):
            new_angle = Angle(reflected_ray, normal, radius=angle_radius, quadrant=(1,-1), other_angle=False, color = GOLD)
            mob.become(new_angle)


        # Add the updater to the angle
        i_angle.add_updater(i_angle_updater)
        r_angle.add_updater(r_angle_updater)

        i_angle_label = MathTex("i", color=BLUE).move_to(i_angle.point_from_proportion(0.5)+0.5*UP)
        r_angle_label = MathTex("r", color=GOLD).move_to(r_angle.point_from_proportion(0.5)+0.5*UP)



        self.wait()

        self.play(Create (mirror),Create(mirror_lines),run_time=2)
        self.play(Write(m_label))
   
        self.add(dot)        

        self.play(Create (normal))
        self.play(Write(n_label))

        self.play(Create(incident_ray),run_time=3)
        self.play(Write(i_label))

        self.play(Create(reflected_ray),run_time=3)
        self.play(Write(r_label))

        self.play(Create (i_angle), Create(i_angle_label))
        self.play(Create (r_angle), Create(r_angle_label))


        self.play(
                  incident_ray.animate.rotate(-30*DEGREES, about_point=dot.get_center())
                  ,reflected_ray.animate.rotate(30*DEGREES, about_point=dot.get_center())
                  ,run_time=3
                 )

        self.play(
                  incident_ray.animate.rotate(30*DEGREES, about_point=dot.get_center())
                  ,reflected_ray.animate.rotate(-30*DEGREES, about_point=dot.get_center())
                  ,run_time=3
                 )

        self.wait()

        i_copy = i_angle_label.copy()
        self.play(i_copy.animate.shift(3*RIGHT+ 3*UP))
        self.wait()

        equal= Text("=").next_to(i_copy,RIGHT)
        self.play(Write(equal))

        r_copy = r_angle_label.copy()
        self.play(r_copy.animate.next_to(equal,RIGHT))
        self.wait()

        i_text = Text("incident angle", color=BLUE, font_size=30).next_to(equal,LEFT)

        r_text = Text("reflected angle", color=GOLD, font_size=30).next_to(equal,RIGHT)

        self.play(Transform (i_copy,i_text))
        self.play(Transform (r_copy,r_text))


        self.wait(2)
