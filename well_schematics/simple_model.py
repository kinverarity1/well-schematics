import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches as mpatches

def parse_items(items, schema_type="drilled_hole_casing"):
    """Parse a well construction definition following a schema like::

        items = [
            {"type": "drilled_hole", "from": 0, "to": 12, "diam": 438, "drilling_order": 0, "label": ""},
            {"type": "drilled_hole", "from": 186, "to": 998.8, "diam": 222, "drilling_order": 2, "label": "main hole"},
            {"type": "drilled_hole", "from": 12, "to": 186, "diam": 311, "drilling_order": 1},
            {"type": "cement_plug", "from": 867, "to": 998.8, "drilling_order": 3},
            {"type": "drilled_hole", "from": 867, "to": 1100, "diam": 149, "drilling_order": 4 },
            {"type": "casing", "from": 0, "to": 12, "inner_diam": 326, "label": "conductor"},
            {"type": "cemented_annulus", "from": 0, "to": 12, "inner_annulus_diam": 326},
            {"type": "casing", "from": 0, "to": 996.5, "inner_diam": 162, "label": "7\" API casing"},
            {"type": "cemented_annulus", "from": 53, "to": 996.5, "inner_annulus_diam": 162},
            {"type": "casing", "from": 0, "to": 184, "inner_diam": 227, "label": "artesian control"},
            {"type": "cemented_annulus", "from": 0, "to": 184, "inner_annulus_diam": 227},
            {"type": "casing", "from": 0, "to": 320, "inner_diam": 104, "label": "fictional reline"},
            {"type": "cemented_annulus", "from": 0, "to": 50, "inner_annulus_diam": 104},
        ]

    """
    if schema_type == "drilled_hole_casing":
        return parse_items_for_drilled_hole_casing_schema(items)
    else:
        raise KeyError(
            f"schema_type {schema_type} is not recognised by well_schematics v{__version__}"
        )


def parse_items_for_drilled_hole_casing_schema(items):
    sorted_items = {}
    
    drilling_items = [x for x in items if x['type'] in ('drilled_hole', 'cement_plug')]
    dh_idxs = [x for x in range(len(drilling_items))]
    dh_order_diams = sorted(dh_idxs, key=lambda x: drilling_items[x].get('diam', 9999))
    sorted_items['drilling'] = [dict(i=i, order_diam=dh_order_diams.index(i), **drilling_items[i]) for i in dh_idxs]
    
    cs_items = [x for x in items if x['type'] in ( 'casing', 'cemented_annulus')]
    cs_idxs = [x for x in range(len(cs_items))]
    cs_order_diams = sorted(cs_idxs, key=lambda x: cs_items[x]['inner_diam'])
    sorted_items['casing'] = [dict(i=i, order_diam=cs_order_diams.index(i), **cs_items[i]) for i in cs_idxs]
    
    return sorted_items
    


def parsed_items_to_dataframe(sitems):
    """Convert parsed items to a dataframe."""
    keys = [
        "type",
        "i",
        "order_diam",
        "drilling_order",
        "from",
        "to",
        "diam",
        "inner_diam",
        "label",
    ]
    df = pd.concat([pd.DataFrame(t) for t in sitems.values()])
    for key in keys:
        if not key in df:
            df[key] = None
    return df[keys]


def get_intervals(df):
    depths = sorted(set(list(df["from"].unique()) + list(df["to"].unique())))
    return [(depths[i], depths[i + 1]) for i in range(len(depths) - 1)]

def subset_construction_by_intervals(df):
    intervals = get_intervals(df)
    for interval in intervals:
        subset = df[(df['from'] < interval[1]) & (df['to'] > interval[0])]
#         logger.debug(f'interval {interval}\n{str(subset)}\n')
        yield interval, subset


def plot_simple_model_dataframe(df, fig=None, ax=None):
    if ax is None:
        if fig is None:
            fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

    dh_cols = ["order_diam", "drilling_order", "from", "to", "diam"]

    for ivl, sdf in subset_construction_by_intervals(df):
        ax.axhline(ivl[0], ls=':', color='grey', lw=0.5)
        ax.axhline(ivl[1], ls=':', color='grey', lw=0.5)
        ax.text(500, ivl[1] - (ivl[1] - ivl[0]) / 2, str(ivl), fontsize='xx-small', color='grey', ha='left', va='center')
        print(f"{ivl}")
        dholes = sdf[sdf.type == "drilled_hole"].sort_values("order_diam")
        print(f' > dhole {dholes[dh_cols]}')
        for dh_idx, dhole in dholes.iterrows():
            later_dholes = df[df.drilling_order > dhole.drilling_order]
            later_max_dhole_diam = later_dholes.diam.max()
            if ivl[1] == dhole.to:    
                ax.plot(
                    [-1 * dhole.diam, -1 * later_max_dhole_diam],
                    [ivl[1], ivl[1]],
                    color="red",
                    lw=0.5,
                )
                ax.plot(
                    [dhole.diam, later_max_dhole_diam],
                    [ivl[1], ivl[1]],
                    color="red",
                    lw=0.5,
                )
            ax.plot(
                [-1 * dhole.diam, -1 * dhole.diam], [ivl[0], ivl[1]], color="brown", lw=0.5
            )
            ax.plot([dhole.diam, dhole.diam], [ivl[0], ivl[1]], color="brown", lw=0.5)
            
            
        casings = sdf[sdf.type == "casing"].sort_values("order_diam")
        for cs_idx, casing in casings.iterrows():
            ax.plot(
                [-1 * casing.inner_diam, -1 * casing.inner_diam],
                [ivl[0], ivl[1]],
                color="black",
                lw=1,
            )
            ax.plot(
                [casing.inner_diam, casing.inner_diam],
                [ivl[0], ivl[1]],
                color="black",
                lw=1,
            )
        inner_casing_diam = casings.inner_diam.min()
            
        plugs = sdf[sdf.type == 'cement_plug']
        print(f'{len(plugs)} plug(s)')
        for plug_ix, plug in plugs.iterrows():
            print(plug)
            earlier_dholes_than_plug = dholes[dholes.drilling_order <= plug.drilling_order]
            later_dholes_than_plug = dholes[dholes.drilling_order > plug.drilling_order]
            plug_outer_diam = min(casings.inner_diam.min(), earlier_dholes_than_plug.diam.min())
            plug_inner_diam = later_dholes_than_plug.diam.max()
            print(f'plug outer diam: {plug_outer_diam}')
            print(f'plug inner diam: {plug_inner_diam}')
            patch1 = mpatches.Rectangle((-1 * plug_outer_diam, ivl[0]), plug_outer_diam - plug_inner_diam, ivl[1] - ivl[0], facecolor='grey', alpha=0.25, lw=0)
            patch2 = mpatches.Rectangle((plug_inner_diam, ivl[0]), plug_outer_diam - plug_inner_diam, ivl[1] - ivl[0], facecolor='grey', alpha=0.25, lw=0)
            ax.add_artist(patch1)
            ax.add_artist(patch2)

        print()

    ax.invert_yaxis()
    ax.set_xticks(np.arange(0, 500, 100))
    ax.set_xlim(500, -500)
    ax.set_xlabel("Diameter (mm)")
    ax.set_ylabel('Depth (m)')
    return ax