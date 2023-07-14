from collections import namedtuple

import numpy as np
import pandas as pd
from plotnine import (
    ggplot,
    aes,
    geom_point,
    geom_path,
    theme,
    theme_minimal,
    labs,
    xlim,
    ylim,
    facet_wrap,
    geom_hline,
    geom_vline,
    geom_segment,
    geom_text,
    scale_color_manual,
    element_blank,
)
from namedframes import PandasNamedFrame


# from plotnine import *

Point = namedtuple("Point", ("x", "y"))

ForceMultiplier = namedtuple("ForceMultiplier", ("x", "y"))
ExpandMultiplier = namedtuple("ExpandMultiplier", ("x", "y"))

# defaults: (1.05, 1.20)
k = 0.2
EXPAND_TEXT = ExpandMultiplier(1.05 * k, 1.2 * k)
EXPAND_POINTS = ExpandMultiplier(1.05, 1.2)
EXPAND_OBJECTS = ExpandMultiplier(1.05, 1.2)


# defaults are
# text: (0.1, 0.25)
# points: (0.2, 0.5)
# objects: (0.1, 0.25)
# see https://adjusttext.readthedocs.io/en/latest/
FORCE_TEXT = ForceMultiplier(0.1, 0.25)
FORCE_POINTS = ForceMultiplier(0.2, 0.5)
FORCE_OBJECTS = ForceMultiplier(0.1, 0.25)


adjust_text = {
    "expand_points": (EXPAND_POINTS.x, EXPAND_POINTS.y),
    "expand_text": (EXPAND_TEXT.x, EXPAND_TEXT.y),
    "expand_objects": (EXPAND_OBJECTS.x, EXPAND_OBJECTS.y),
    "force_text": (FORCE_TEXT.x, FORCE_TEXT.y),
    "force_points": (FORCE_POINTS.x, FORCE_POINTS.y),
    "force_objects": (FORCE_OBJECTS.x, FORCE_OBJECTS.y),
    "lim": 10000,
    "save_steps": False,
    "avoid_text": True,
    "avoid_points": False,
    "avoid_self": False,
    # "arrowprops": {"arrowstyle": "-", "color": "k", "lw": 0.25},
}


class StandingsDF(PandasNamedFrame):
    W: int
    L: int
    RS_G: float
    RA_G: float
    Team: str
    lg_div: str


class ArcDF(PandasNamedFrame):
    Team: str
    lg_div: str
    x: float
    y: float


def make_arc(start_point: Point, end_point: Point):
    """
    creates an arc from `start_point` to `end_point`. The arc
    is a portion of a circle centered at the origin.

    :param start_point:
    :param end_point:
    :return: numpy.array
    """
    vector_norm = np.sqrt(start_point.x**2 + start_point.y**2)
    initial_angle = np.arctan2(start_point.y, start_point.x)
    final_angle = np.arctan2(end_point.y, end_point.x)
    angle_step = (final_angle - initial_angle) / 100
    if angle_step == 0:
        angle_step = 1e-6
        final_angle += 1e-6
    angles = np.arange(initial_angle, final_angle + 0.5 * angle_step, angle_step)
    return vector_norm * np.array(list(zip(np.cos(angles), np.sin(angles))))


def make_arc_dataframe(sub_df: StandingsDF) -> ArcDF:
    """
    Makes a dataframe comprising the arc for this row and replicating the team
    and division-id.

    :param sub_df:
    :return:
    """
    if len(sub_df) > 1:
        raise ValueError

    row = sub_df.iloc[0]
    arc = make_arc(Point(row.RS_G, row.RA_G), Point(row.x_start, row.y_start))
    num_rows = arc.shape[0]
    return ArcDF(
        pd.DataFrame(
            {
                "Team": [row.Team] * num_rows,
                "lg_div": [row.lg_div] * num_rows,
                "x": arc[:, 0],
                "y": arc[:, 1],
            }
        )
    )


def get_winpct_contours(standings: StandingsDF, delta_runs: float):
    mean_runs = 0.5 * (standings.RS_G.mean() + standings.RA_G.mean())
    run_max = mean_runs + delta_runs
    run_min = mean_runs - delta_runs
    text_x_min = run_min + 2 * delta_runs * 0.12
    text_x_max = run_max - 2 * delta_runs * 0.12

    # 36 to 126 per 162 games in steps of 10
    winpct_seq = np.arange(81 - 45, 81 + 45 + 1e-6, 10) / 162
    slopes = np.sqrt((1 - winpct_seq) / winpct_seq)

    winpct_contours = pd.DataFrame({"slopes": slopes})
    winpct_contours = winpct_contours.assign(
        x=np.where(run_min * slopes < run_min, run_min / slopes, run_min),
        y=np.where(run_min * slopes < run_min, run_min, run_min * slopes),
        xend=np.where(run_max * slopes > run_max, run_max / slopes, run_max),
        yend=np.where(run_max * slopes > run_max, run_max, run_max * slopes),
    )

    win_labels = pd.DataFrame({"w": winpct_seq * 162})
    win_labels = win_labels.assign(
        x=np.where(text_x_min * slopes < run_min, text_x_max, text_x_min),
        y=np.where(
            text_x_min * slopes < run_min, text_x_max * slopes, text_x_min * slopes
        ),
    )

    return winpct_contours, win_labels


def validate_transform_standings(standings: pd.DataFrame):
    """
    Validates the standings dataframe and transforms it to the
    necessary form if needed.

    :param standings:
    :return:
    """
    pl_df = standings.copy()
    necessary_columns = ["W", "L", "RS_G", "RA_G", "Team", "lg_div"]
    if (
        "lgID" in pl_df.columns
        and "divID" in pl_df.columns
        and "lg_div" not in pl_df.columns
    ):
        pl_df = pl_df.assign(lg_div=pl_df.lgID + "-" + pl_df.divID)

    if "R" in pl_df.columns and "G" in pl_df.columns and "RS_G" not in pl_df.columns:
        pl_df = pl_df.assign(RS_G=lambda row: row.R / row.G)
    if "RA" in pl_df.columns and "G" in pl_df.columns and "RA_G" not in pl_df.columns:
        pl_df = pl_df.assign(RA_G=lambda row: row.RA / row.G)

    column_aliases = {"teamID": "Team", "div_id": "lg_div"}

    for original_column, updated_column in column_aliases.items():
        if original_column in pl_df.columns:
            pl_df = pl_df.rename({original_column: updated_column}, axis=1)

    if not all(
        necessary_column in pl_df.columns for necessary_column in necessary_columns
    ):
        raise ValueError(f"missing columns from {pl_df.columns}")

    return pl_df.assign(
        winpct=lambda row: row.W / (row.W + row.L),
        wpythag=lambda row: row.RS_G**2 / (row.RS_G**2 + row.RA_G**2),
        x_start=lambda row: row.RS_G * np.sqrt(row.winpct / row.wpythag),
        y_start=lambda row: row.x_start * np.sqrt((1 - row.winpct) / row.winpct),
        was_lucky=lambda row: row.winpct > row.wpythag,
    )


def plot_graphical_standings(standings: StandingsDF, delta_runs=None):
    standings = validate_transform_standings(standings)

    mean_runs = 0.5 * (standings.RS_G.mean() + standings.RA_G.mean())
    if delta_runs is None:
        delta_runs = (
            max(
                (
                    standings.RS_G.max() - mean_runs,
                    mean_runs - standings.RS_G.min(),
                    standings.RA_G.max() - mean_runs,
                    mean_runs - standings.RA_G.max(),
                )
            )
            * 1.05
        )
    print(delta_runs)
    panel_min = mean_runs - delta_runs
    panel_max = mean_runs + delta_runs

    arcs = standings.groupby("Team").apply(make_arc_dataframe).reset_index(drop=True)
    winpct_contours, win_labels = get_winpct_contours(standings, delta_runs)

    graph = (
        ggplot(data=standings)
        + geom_point(mapping=aes(x="RS_G", y="RA_G"))
        + labs(x="RS / G", y="RA / G")
        + xlim(panel_min - 0.01, panel_max + 0.01)
        + ylim(panel_max + 0.01, panel_min - 0.01)
        + geom_path(data=arcs, mapping=aes(x="x", y="y", group="Team"))
        + theme_minimal()
        + facet_wrap("~lg_div")
        + geom_hline(yintercept=mean_runs)
        + geom_vline(xintercept=mean_runs)
        + theme(panel_grid=element_blank())
        + geom_segment(
            data=winpct_contours,
            mapping=aes(x="x", y="y", xend="xend", yend="yend"),
            alpha=0.25,
        )
    )
    graph += geom_text(
        data=standings,
        mapping=aes(x="RS_G", y="RA_G", label="Team", color="was_lucky"),
        size=8,
        adjust_text=adjust_text,
        show_legend=False,
    )
    graph += scale_color_manual(values=("steelblue", "red"))
    graph += geom_text(
        data=win_labels.assign(
            y_=lambda row: row.y - 0.1, w=lambda row: row.w.astype(int)
        ),
        mapping=aes(x="x", y="y_", label="w"),
        alpha=0.5,
        size=8,
    )
    return graph
