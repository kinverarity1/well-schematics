from matplotlib import patches as mpatches


class WellComponent:
    """Component of a well, e.g. casing, screen.

    Args:
        top (float): top depth
        bottom (float): bottom depth
        diameter (float): diameter

    """
    def __init__(self, top: float, bottom: float, diameter: float):
        self.top = top
        self.bottom = bottom
        self.diameter = diameter
        self.left_diameter_fraction = 0.25
        self.right_diameter_fraction = 0.75


class Casing(WellComponent):
    facecolor = "k"
    fill = True


class SlottedCasing(WellComponent):
    facecolor = "k"
    fill = False
    hatch_density = 3
    hatch_symbol = "/"

    @property
    def hatch(self):
        return self.hatch_symbol * self.hatch_density

    def get_left_artist(self):
        return mpatches.Rectangle(
                (1 / 4, seg_from),
                pipe_width * 0.9,
                seg_length,
                facecolor="k",
                fill=False,
                hatch=hatch,
                transform=t,
            )

class WirewoundScreen(WellComponent):
    facecolor = "k"
    fill = False
    hatch_density = 3
    hatch_symbol = "-"

    @property
    def hatch(self):
        return self.hatch_symbol * self.hatch_density

    def get_left_artist(self):
        return mpatches.Rectangle(
                (1 / 4, seg_from),
                pipe_width * 0.9,
                seg_length,
                facecolor="k",
                fill=False,
                hatch=hatch,
                transform=t,
            )

class Well:

    diameters_to_fractions = {
        1: ((0.25, 0.75), ),
        2: ((0.2, 0.8), (0.3, 0.7)),
    }

    def __init__(self, components):
        self.components = components

    @property
    def diameters_mapping(self):
        diameters = {c.diameter: [] for c in self.components}
        for c in self.components:
            diameters[c.diameter].append(c)
        return diameters

    @property
    def diameters(self):
        return sorted(tuple([c.diameter for c in self.components]))

    def plot(self):
        # Go through and set diameter fractions on the whole well.
        for diameter in self.diameters:
