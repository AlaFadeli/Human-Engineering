import numpy as np
from manim import *

# Define a function to plot different types of money over time
def money_evolution(x, money_type):
    if money_type == "Commodity Money":
        # Example of commodity money function, e.g., gold
        return 50 * np.sin(x / 10) + 50
    elif money_type == "Fiat Money":
        # Example of fiat money (currency not backed by a physical commodity)
        return 30 * np.cos(x / 20) + 50
    elif money_type == "Cryptocurrency":
        # Example of cryptocurrency (e.g., Bitcoin)
        return 40 * np.sin(x / 15) + 30
    else:
        return 0

def money_timeline_step(self, cfg, context):
    # First slide, draw timeline and the evolution of money types
    money_types = context.get("money_types")
    graphs = VGroup()
    grid = Axes(x_range=[-100, 100, 20], y_range=[0, 100, 20],
                x_length=10, y_length=5, tips=False,
                axis_config={"color": BLACK})
    graphs += grid
    graphs += Text("Timeline of Money Types", font_size=self.s_size).next_to(grid, UP)
    graphs += grid.plot(lambda x: money_evolution(x, "Commodity Money"), color=BLUE).set_label("Commodity Money")
    self.play(
        FadeIn(graphs[:-1], run_time=self.fadein_rt),
        DrawBorderThenFill(graphs[-1], run_time=3*self.drawborderthenfill_rt)
    )
    self.last = graphs
    self.next_slide()

    # Show Fiat Money
    graphs += grid.plot(lambda x: money_evolution(x, "Fiat Money"), color=GREEN).set_label("Fiat Money")
    self.play(
        DrawBorderThenFill(graphs[-1], run_time=3*self.drawborderthenfill_rt)
    )
    self.next_slide()

    # Show Cryptocurrency
    graphs += grid.plot(lambda x: money_evolution(x, "Cryptocurrency"), color=YELLOW).set_label("Cryptocurrency")
    self.play(
        DrawBorderThenFill(graphs[-1], run_time=3*self.drawborderthenfill_rt)
    )
    self.next_slide()

    # Final slide with labels and titles
    labels = [Text("Commodity Money", font_size=self.s_size).next_to(graphs[1], UP),
              Text("Fiat Money", font_size=self.s_size).next_to(graphs[1], DOWN),
              Text("Cryptocurrency", font_size=self.s_size).next_to(graphs[1], RIGHT)]
    self.play(FadeIn(labels, run_time=self.fadein_rt))
    self.next_slide()

