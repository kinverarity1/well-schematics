import matplotlib.pyplot as plt
from matplotlib import patches as mpatches
from matplotlib import transforms as mtransforms


def draw_simple(
    pzone_top,
    pzone_bottom,
    casing_top=0,
    pzone_type="S",
    ax=None,
    tight_layout=True,
    depth_tick_markers=False,
):
    """Draw simple well schematic.

    Args:
        pzone_top (float): top of the production zone
        pzone_bottom (float): bottom of the production zone
        casing_top (float): top of the casing
        pzone_type (str): either "S" for screen, "SC" for slotted casing,
            or "OH" for open hole.
        ax (matplotlib.Axes): to draw in
        tight_layout (bool): run tight_layout() on ax.figure to rearrange
            things to fit.
        depth_tick_markers (bool): show tick markers for the vertical
            depth axis. Labels will always appear.

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
        else:
            hatch = None
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
    for side in ["left", "right", "bottom", "top"]:
        ax.spines[side].set_visible(False)
    if not depth_tick_markers:
        ax.yaxis.set_ticks_position("none")
    ax.set_facecolor("white")
    ax.set_xticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(pzone_bottom + 1, casing_top - 1)
    if tight_layout:
        ax.figure.tight_layout()

    return patches
