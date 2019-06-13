import matplotlib.pyplot as plt
from matplotlib import patches as mpatches
from matplotlib import transforms as mtransforms


def draw_simple(pzone_top, pzone_bottom, casing_top=0, pzone_type="S", ax=None):
    """Draw simple well schematic.

    Args:
        pzone_top (float): top of the production zone
        pzone_bottom (float): bottom of the production zone
        casing_top (float): top of the casing
        pzone_type (str): either "S" (screen), "SC" (slotted casing)
            or "OH" (open hole)
        ax (matplotlib.Axes): to draw in

    The simple model used here assumes that a well consists of solid casing
    of one diameter from top, and then immediately below that, one type of
    production zone, of the same diameter.

    Returns: a list of the artists created.

    """
    if ax is None:
        fig = plt.figure(figsize=(1, 5))
        ax = fig.add_subplot(111)

    t = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)

    pipe_width = 0.08
    casing_bottom = pzone_top
    casing_height = casing_bottom - casing_top
    pzone_height = pzone_bottom - pzone_top
    hatch_density = 3

    patches = []

    casing_left = mpatches.Rectangle(
        (1 / 4, casing_top), pipe_width, casing_height, facecolor="k", transform=t
    )
    casing_right = mpatches.Rectangle(
        (3 / 4 - pipe_width, casing_top),
        pipe_width,
        casing_height,
        facecolor="k",
        transform=t,
    )
    patches += [casing_left, casing_right]

    if pzone_type != "OH":
        if pzone_type == "S":
            hatch = "-" * hatch_density
        elif pzone_type == "SC":
            hatch = "/" * hatch_density
        pzone_left = mpatches.Rectangle(
            (1 / 4, pzone_top),
            pipe_width * 0.9,
            pzone_height,
            facecolor="k",
            fill=False,
            hatch=hatch,
            transform=t,
        )
        pzone_right = mpatches.Rectangle(
            (3 / 4 - pipe_width, pzone_top),
            pipe_width * 0.9,
            pzone_height,
            facecolor="k",
            fill=False,
            hatch=hatch,
            transform=t,
        )
        patches += [pzone_left, pzone_right]

    for patch in patches:
        ax.add_artist(patch)

    ax.grid(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_facecolor("white")
    ax.set_xticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(pzone_bottom + 1, casing_top - 1)

    return patches
