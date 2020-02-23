from . import plots


def draw_simple(pzone_top, pzone_bottom, casing_top=0, pzone_type="screen", **kwargs):
    """Draw simple well schematic.

    Args:
        pzone_top (float): top of the production zone
        pzone_bottom (float): bottom of the production zone
        casing_top (float): top of the casing
        pzone_type (str): either "screen", "slotted casing", or
            "open hole".

    All keyword arguments documented in :func:`plot_single_diameter_well`
    are also accepted here.

    The simple model used here assumes that a well consists of solid casing
    of one diameter from top, and then immediately below that, one type of
    production zone, of the same diameter.

    Returns: a list of the *matplotlib.Artists* created.

    """
    segments = [
        {"type": "casing", "top": casing_top, "bottom": pzone_top},
        {"type": pzone_type, "top": pzone_top, "bottom": pzone_bottom},
    ]

    return plots.plot_single_diameter_well(segments, **kwargs)
