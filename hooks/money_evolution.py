from manim import *

# Hook function for money evolution
def money_evolution(self, cfg, context):
    # Define the timeline as a simple horizontal line
    timeline = Line(LEFT * 6, RIGHT * 6, color=BLACK)

    # Text for each stage of money evolution with simple colors
    stages = [
        ("Barter System", LEFT * 5, GREEN),
        ("Metal Coins", LEFT * 2, BLUE),
        ("Paper Money", RIGHT * 2, RED),
        ("Digital Currency", RIGHT * 5, YELLOW)
    ]

    # Title text at the top
    title = Text("Evolution of Money", font_size=36, color=PURPLE).to_edge(UP)

    # Fade in the title and timeline
    self.play(FadeIn(title))
    self.play(DrawBorderThenFill(timeline))

    # Create and animate each stage of money evolution
    for stage, position, color in stages:
        stage_text = Text(stage, font_size=24, color=color).move_to(position)
        self.play(Write(stage_text))
        self.play(stage_text.animate.shift(RIGHT * 1))  # Animate each stage moving to the right

    # Optional: Make each stage of money pulse for interactivity (simple emphasis)
    for stage, position, color in stages:
        stage_text = Text(stage, font_size=24, color=color).move_to(position)
        self.play(stage_text.animate.scale(1.2).set_color(WHITE))
        self.play(stage_text.animate.scale(1/1.2).set_color(color))

    # Fade out all objects
    self.play(FadeOut(title, timeline, *[Text(stage, font_size=24, color=color).move_to(position) for stage, position, color in stages]))


