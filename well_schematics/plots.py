import matplotlib.pyplot as plt
from matplotlib import patches as mpatches
from matplotlib import transforms as mtransforms


PZONE_MAPPING = {
    "OH": "open hole",
    "open hole": "open hole",
    "open-hole": "open hole",
    "open": "open hole",
    "S": "wirewound screen",
    "screen": "wirewound screen",
    "wirewound screen": "wirewound screen",
    "SC": "slotted casing",
    "slots": "slotted casing",
    "slotted": "slotted casing",
    "slotted casing": "slotted casing",
}


def plot_single_diameter_well(
    segments,
    ax=None,
    tight_layout=True,
    depth_tick_markers=False,
    pipe_width=0.08,
    hatch_density=3,
):
    """Draw casing in a well which is a single diameter construction.

    Args:
        segments (sequence of dicts): each dict should be in the
            form ``{"type": <str>, "top": <float>, "bottom": <float>}``.
            The "type" should be either "casing", "pipe", "blank", or "sump",
            or a production zone type (either "screen", "slotted casing" or
            "open hole"). "top" and "bottom" are the top and bottom of each
            segment.
        ax (matplotlib.Axes): to draw in
        tight_layout (bool): run tight_layout() on ax.figure to rearrange
            things to fit.
        depth_tick_markers (bool): show tick markers for the vertical
            depth axis. Labels will always appear.
        pipe_width (float): width of pipe
        hatch_density (int): density of screen hatching

    Returns: a list of the artists created.

    """
    if ax is None:
        fig = plt.figure(figsize=(1, 5))
        ax = fig.add_subplot(111)

    t = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
    patches = []
    for segment in segments:
        seg_type = segment["type"]
        seg_from = segment["top"]
        seg_to = segment["bottom"]
        seg_length = seg_to - seg_from

        if seg_type in PZONE_MAPPING:
            seg_type = PZONE_MAPPING[seg_type]
            if seg_type == "wirewound screen":
                hatch = "-" * hatch_density
            elif seg_type == "slotted casing":
                hatch = "/" * hatch_density
            else:
                hatch = None
            seg_left = mpatches.Rectangle(
                (1 / 4, seg_from),
                pipe_width * 0.9,
                seg_length,
                facecolor="k",
                fill=False,
                hatch=hatch,
                transform=t,
            )
            seg_right = mpatches.Rectangle(
                (3 / 4 - pipe_width, seg_from),
                pipe_width * 0.9,
                seg_length,
                facecolor="k",
                fill=False,
                hatch=hatch,
                transform=t,
            )
        else:
            seg_type = "pipe"
            seg_left = mpatches.Rectangle(
                (1 / 4, seg_from), pipe_width, seg_length, facecolor="k", transform=t
            )
            seg_right = mpatches.Rectangle(
                (3 / 4 - pipe_width, seg_from),
                pipe_width,
                seg_length,
                facecolor="k",
                transform=t,
            )
        patches += [seg_left, seg_right]

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
    ax.set_ylim(
        max([s["bottom"] for s in segments]) + 1, min([s["top"] for s in segments]) - 1
    )
    if tight_layout:
        ax.figure.tight_layout()

    return patches
