import os

import well_schematics as ws

artists = ws.plot_single_diameter_well(
    [
        {"type": "casing", "top": -0.5, "bottom": 27},
        {"type": "screen", "top": 27, "bottom": 36},
    ]
)

artists[0].axes.figure.savefig(
    os.path.join(os.path.dirname(__file__), "example_simplest.png")
)
