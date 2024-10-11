def create_tube(self, cfg):
    """
        create tube shape with cathode/anode
        Returns:
         - tube Group where
           - tube[0] is the actual tube
           - tube[1] is the heater element
           - tube[2] is the cathode
           - tube[3] is the anode
    """
    def cylinder(base_radius, bump_factor, transition_length, height):
        """create cylindrical part, bumping the base radius"""
        def cylinder_transition(u, v):
            """
                compute function to transition from
                base_radius to base_radius*bump_factor
                over transition_length distance.
            """
            z = height * u
            if z <= height / 2 - transition_length / 2:
                radius = base_radius
            elif z >= height / 2 + transition_length / 2:
                radius = bump_factor*base_radius
            else:
                t = (z - (height / 2 - transition_length / 2)) / transition_length
                radius = (1 - t) * base_radius + t * bump_factor * base_radius
            x = radius * np.cos(v)
            y = radius * np.sin(v)
            return np.array([x, y, z])
        cylinder_surface = Surface(
            cylinder_transition,
            u_range=[0, 1],
            v_range=[0, TAU],
            fill_color=self.parse_eval(cfg.tube_color),
            stroke_color=self.parse_eval(cfg.tube_color),
            stroke_width=0,
            fill_opacity=float(cfg.default_opacity),
            checkerboard_colors=False,
            #resolution=(60,60),
        )
        cylinder_surface.set(opacity=0.5)
        return cylinder_surface
    def bulb(base_radius, bulb_radius, transition_length, length):
        """create bulby part"""
        def bulb_transition(u, v):
            z = transition_length * u
            if z <= transition_length:
                radius = base_radius + (bulb_radius - base_radius) * (z / transition_length)**2
            else:
                bulb_z = z - transition_length
                bulb_factor = 1 - (bulb_z / (length - transition_length))**2
                radius = bulb_radius*np.sqrt(bulb_factor)
            x = radius * np.cos(v)
            y = radius * np.sin(v)
            return np.array([x, y, z])

        def bulb_func(u, v):
            r = bulb_radius * u
            x = r * np.cos(v)
            y = r * np.sin(v)
            z = transition_length + bulb_radius * (1 - u**2)
            return np.array([x, y, z])

        transition = Surface(
            bulb_transition,
            u_range=[0, 1],
            v_range=[0, TAU],
            fill_color=self.parse_eval(cfg.tube_color),
            stroke_color=self.parse_eval(cfg.tube_color),
            stroke_width=0,
            fill_opacity=float(cfg.default_opacity),
            checkerboard_colors=False,
            #resolution=(60,60),
        )
        return Group(
            transition,
            Surface(
                bulb_func,
                u_range=[0, 1],
                v_range=[0, TAU],
                fill_color=self.parse_eval(cfg.bulb_color),
                stroke_color=self.parse_eval(cfg.bulb_color),
                fill_opacity=float(cfg.default_opacity),
                stroke_width=0,
                checkerboard_colors=False,
                #resolution=(60,60),
            ),
        )
    def hollow_cylinder(inner_radius, outer_radius, height):
        """create a hallow cylinder"""
        def outer_cylinder_surface(u, v):
            x = outer_radius * np.cos(v)
            y = outer_radius * np.sin(v)
            z = height * u
            return np.array([x, y, z])
        def inner_cylinder_surface(u, v):
            x = inner_radius * np.cos(v)
            y = inner_radius * np.sin(v)
            z = height * u
            return np.array([x, y, z])
        return Group(
            Surface(
                outer_cylinder_surface,
                u_range=[0, 1],
                v_range=[0, TAU],
                fill_color=self.parse_eval(cfg.material_colors[0]),
                stroke_color=self.parse_eval(cfg.material_colors[0]),
                fill_opacity=float(cfg.default_opacity),
                stroke_width=0,
                checkerboard_colors=False,
            ),
            Surface(
                inner_cylinder_surface,
                u_range=[0, 1],
                v_range=[0, TAU],
                fill_color=self.parse_eval(cfg.material_colors[0]),
                stroke_color=self.parse_eval(cfg.material_colors[0]),
                fill_opacity=float(cfg.default_opacity),
                stroke_width=0,
                checkerboard_colors=False,
                #resolution=(60,60),
            ),
            AnnularSector(
                inner_radius=inner_radius,
                outer_radius=outer_radius,
                angle=TAU,
                fill_opacity=float(cfg.default_opacity),
                fill_color=self.parse_eval(cfg.material_colors[0]),
                stroke_width=0,
            ),
            AnnularSector(
                inner_radius=inner_radius,
                outer_radius=outer_radius,
                angle=TAU,
                fill_opacity=float(cfg.default_opacity),
                fill_color=self.parse_eval(cfg.material_colors[0]),
                stroke_width=0,
            ).move_to(np.array([0,0,height]))
        )
    cyl1 = cylinder(0.5, 1.5, 1, 3).rotate(PI/2, axis=UP)
    cyl2 = cylinder(0.75, 0.666667, 0.5, 2).rotate(PI/2, axis=UP)
    cyl3 = cylinder(0.5, 1.0, 0.0, 1).rotate(PI/2, axis=UP)
    cyl4 = cylinder(0.5, 1.4, 1, 2).rotate(PI/2, axis=UP)
    cyl5 = cylinder(0.7, 1.0, 0.0, 2).rotate(PI/2, axis=UP)
    bul1 = bulb(0.7, 0.8, 0.5, 3).rotate(PI/2, axis=UP)
    heater = Cylinder(
        radius=0.4, height=0.5, show_ends=True,
        direction=RIGHT,
        fill_color=RED,
        stroke_color=RED,
        stroke_width=0,
        fill_opacity=1.0,
        #resolution=(60,60),
    )
    cathode = Cylinder(
        radius=0.5, height=0.3, show_ends=True,
        direction=RIGHT,
        fill_color=self.parse_eval(cfg.material_colors[0]),
        stroke_color=self.parse_eval(cfg.material_colors[0]),
        stroke_width=0,
        fill_opacity=0.9,
        #resolution=(60,60),
    )
    anode = hollow_cylinder(inner_radius=0.1, outer_radius=0.5, height=0.3).rotate(PI/2, axis=UP)
    return Group(
        Group(
            cyl1,
            cyl2.next_to(cyl1, RIGHT, buff=0.0),
            cyl3.next_to(cyl2, RIGHT, buff=0.0),
            cyl4.next_to(cyl3, RIGHT, buff=0.0),
            cyl5.next_to(cyl4, RIGHT, buff=0.0),
            bul1.next_to(cyl5, RIGHT, buff=0.0),
        ), # tube
        heater.move_to(cyl1.get_left()),
        cathode.move_to(cyl2.get_right()),
        anode.move_to(cyl3.get_right()),
        ThreeDAxes(),
    )


def cathode_ray_step(self, cfg, context):
    # Layout elements and text should not rotate with camera
    # so their positions are fixed
    self.add_fixed_orientation_mobjects(self.layout)

    # Create the tube group
    create_tube = context.get('create_tube')
    tube = create_tube(self, cfg).shift(4*LEFT+3*DOWN)

    # save initial camera state and rotate it
    orig_phi = self.camera.get_phi()
    orig_theta = self.camera.get_theta()

    bulb_txt = Text("Fluorescent coating").move_to(6*RIGHT)
    bulb_arr = Arrow3D(bulb_txt, tube[0][-1].get_right())
    heater_txt = Text("Heater").move_to(9*LEFT+2*DOWN)
    heater_arr = Arrow3D(heater_txt.get_top()+UP, tube[1].get_left())
    cathode_txt = Text("Cathode").move_to(6*LEFT+8*UP+np.array([0,0,1.5]))
    cathode_arr = Arrow3D(cathode_txt.get_right()+1.5*DOWN, tube[2].get_right()+np.array([0,0,0.5]))
    anode_txt = Text("Anode").move_to(9*LEFT+8*UP+np.array([0,0,1.5]))
    anode_arr = Arrow3D(anode_txt.get_left()+DOWN, tube[3][-1].get_top())

    ray_end = tube[0][-1].get_right()
    ray_start = tube[2][-1].get_center()

    legend = Group(
        Group(tube[0], bulb_txt, bulb_arr),
        Group(tube[1], heater_txt, heater_arr),
        Group(tube[2], cathode_txt, cathode_arr),
        Group(tube[3], anode_txt, anode_arr),
    )

    for item in legend:
        self.set_camera_orientation(phi=orig_phi, theta=orig_theta)
        self.add_fixed_orientation_mobjects(item[1])
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.play(FadeIn(item, run_time=self.fadein_rt))
        self.next_slide()

    ray = Line(ray_start, ray_end, color=RED)

    p2 = tube[2][-2].get_bottom()
    p3 = tube[3][-1].get_bottom()
    src = Circle(radius=0.2, color=WHITE).move_to((p2+p3)/2+3*DOWN)
    plus = Text("-").next_to(src, 2*LEFT+0.5*DOWN)
    minus = Text("+").next_to(src, 2*RIGHT+0.5*DOWN)
    self.add_fixed_orientation_mobjects(plus, minus)
    power_source = Group(
        Line(p2, p2+3*DOWN),
        Line(p3, p3+3*DOWN),
        src,
        Line(p2+3*DOWN, src),
        Line(p3+3*DOWN, src),
    )
    self.play(
        FadeIn(power_source, runt_ime=self.fadein_rt),
        FadeIn(ray, run_time=self.fadein_rt),
    )

    self.next_slide()
    ray_end2 = ray_end + np.array([0,0,0.4])
    curved_ray = CubicBezier(
        ray_start, ray_start+RIGHT,
        ray_end, ray_end2,
        color=RED
    )
    plus_charge = Group(
        Circle(radius=0.5, color=BLUE_C),
        Text("+", font_size=self.b_size, color=BLUE_C)
    ).move_to(RIGHT+UP+np.array([0,0,2]))
    minus_charge = Group(
        Circle(radius=0.5, color=RED_C),
        Text("+", font_size=self.b_size, color=RED_C)
    ).move_to(RIGHT+UP+np.array([0,0,-2]))
    self.add_fixed_orientation_mobjects(minus_charge, plus_charge)
    self.play(
        Transform(ray, curved_ray, run_time=2*self.transform_rt),
        FadeIn(minus_charge, run_time=self.fadein_rt),
        FadeIn(plus_charge, run_time=self.fadein_rt),
    )
    self.next_slide()
    self.play(
        Transform(ray, Line(ray_start, ray_end, color=RED), run_time=2*self.transform_rt),
        FadeOut(minus_charge, run_time=self.fadeout_rt),
        FadeOut(plus_charge, run_time=self.fadeout_rt),
    )

    self.next_slide()

    def magnet_shape(radius, height, gap, color):
        arm_left = Cylinder(
            radius=radius,
            height=height,
            direction=UP,
            fill_color=GRAY,
            stroke_width=0,
            checkerboard_colors=False,
        ).move_to(LEFT * gap/2 + UP)
        arm_right = Cylinder(
            radius=radius,
            height=height,
            direction=UP,
            fill_color=BLUE,
            stroke_width=0,
            checkerboard_colors=False,
        ).move_to(RIGHT * gap/2 + UP)
        n = Text("N", font_size=self.b_size).next_to(arm_left, UP)
        s = Text("S", font_size=self.b_size).next_to(arm_right, UP)
        return (VGroup(arm_left, n), VGroup(arm_right, s))

    (mag_l, mag_r) = magnet_shape(0.2, 1.5, 4, WHITE)
    
    ZDOWN = np.array([0,0,-1])
    mag_l = mag_l.rotate(PI/2, axis=UP).rotate(PI/2, axis=RIGHT).move_to(tube[0][-1].get_right()+2*DOWN+2*LEFT+ZDOWN)
    mag_r = mag_r.rotate(PI/2, axis=UP).rotate(PI/2, axis=RIGHT).move_to(tube[0][-1].get_right()+4*UP+2*LEFT+ZDOWN)
    ray_end3 = ray_end + np.array([0,0,-0.2])
    new_curved_ray = CubicBezier(
        ray_start, ray_start+RIGHT,
        ray_end, ray_end3,
        color=RED
    )
    self.play(
        Transform(ray, new_curved_ray, run_time=2*self.transform_rt),
        FadeIn(mag_l, run_time=self.fadein_rt),
        FadeIn(mag_r, run_time=self.fadein_rt),
    )

    self.next_slide()
    self.play(
        Transform(ray, Line(ray_start, ray_end, color=RED), run_time=2*self.transform_rt),
        FadeOut(mag_l, run_time=self.fadeout_rt),
        FadeOut(mag_r, run_time=self.fadeout_rt),
    )
    txt = Text("Different materials").move_to(LEFT+3*DOWN)
    self.add_fixed_orientation_mobjects(txt)
    self.play(
        tube[2].animate.set_fill(self.parse_eval(cfg.material_colors[1])),
        tube[3].animate.set_fill(self.parse_eval(cfg.material_colors[1])),
        FadeIn(txt, run_time=self.fadein_rt),
    )
    self.set_camera_orientation(phi=orig_phi, theta=orig_theta)
