"""This is usually how I would set my plots but in the interest of time (trying to keep to the 6 hour window, not)"""


import sys

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.append("..//")
from src.make_data import build_metrics

colors_zebra_interview = {
    "Vibrant Purple": "#574cfa",
    "Dark Charcoal": "#070e15",
    "Pure White": "#ffffff",
    "Deep Blue": "#1b1d4e",
    "Royal Blue": "#2f2d87",
    "Light Gray": "#c7c7c7",
    "Light Silver": "#cfcfcf",
    "Medium Gray": "#c8c8c8",
    "Soft Gray": "#d0d0d0",
    "Warm Gray": "#cecece"
} # taken from attachments given in interview, used chatGPT to get hexidecimal 


def plot_median_movie_score_over_time(df:pd.DataFrame) -> matplotlib.figure.Figure:
    """gives the median movie score over time, returns the figure."""

    df_tmp = df.loc[df["movie_score"].notnull(), ].copy(deep=True)
    df_tmp.loc[df_tmp["decade"] < 1960, "decade"]= 1960
    df_tmp = df_tmp.assign(decade = df_tmp.decade.astype(str).str.replace("9990", "N/As")) # make sure nulls on right side of graph

    tbl = df_tmp.groupby("decade").agg(
        n = ("movie_title", "count"),
        median_score = ("movie_score", "median"),
        movie_score = ("movie_score", "sum"),
        gross = ("gross", "sum"),
        budget = ("budget", "sum"),
        avg_users_voted = ("num_users_voted", "mean"),
        num_users_voted = ("num_users_voted", "sum")
    ).round(2)

    tbl = tbl.reset_index()
    tbl = build_metrics(tbl)

    fig, ax = plt.subplots()

    sns.barplot(data = tbl, x = "decade", y = "n", ax = ax,
                 color=colors_zebra_interview["Deep Blue"]).set(title = "Median Movie Score by Decade", ylabel ="Count of Movies in Data")

    ax2 = ax.twinx()

    sns.pointplot(data = tbl, x="decade", y = "median_score", ax = ax2,
                   color=colors_zebra_interview["Vibrant Purple"],
                   label = "Median Movie Rating (1-10) by decade").set(ylabel = "Median Score (1-10)")
    
    ax2.set_ylim(1,10)
    plt.axhline(y=tbl["median_score"].median(), color=colors_zebra_interview["Light Gray"], linestyle='--', linewidth=1.5, label = "Median Overall") # doesn't make sense take from the raw

    plt.tight_layout()
    plt.savefig("..//plots/median_movie_score.png")

    return fig

def plot_median_movie_lift_over_time(df:pd.DataFrame) -> matplotlib.figure.Figure:
    """
    gives the median movie lift over time, saves out and gives  a figure to be rendered."""

    df_tmp = df.loc[df["movie_score"].notnull(), ].copy(deep=True)
    df_tmp.loc[df_tmp["decade"] < 1960, "decade"]= 1960
    df_tmp = df_tmp.assign(decade = df_tmp.decade.astype(str).str.replace("9990", "N/As")) # make sure nulls on right side of graph

    tbl = df_tmp.groupby("decade").agg(
        n = ("movie_title", "count"),
        median_score = ("movie_score", "median"),
        movie_score = ("movie_score", "sum"),
        gross = ("gross", "sum"),
        budget = ("budget", "sum"),
        avg_users_voted = ("num_users_voted", "mean"),
        num_users_voted = ("num_users_voted", "sum")
    ).round(2)

    tbl = tbl.reset_index()
    tbl = build_metrics(tbl)
    

    fig, ax = plt.subplots()
    tbl = tbl.assign(decade = tbl.decade.astype(str).str.replace("9990", "N/As")) # make sure nulls on right side of graph

    sns.barplot(data = tbl, x = "decade", y = "n", ax = ax,
                 color=colors_zebra_interview["Deep Blue"]).set(title = "Median Movie Profit (lift) by Decade", ylabel ="Count of Movies in Data")

    ax2 = ax.twinx()

    sns.pointplot(data = tbl, x="decade", y = "lift", ax = ax2,
                   color=colors_zebra_interview["Light Silver"],
                   label = "lift").set(ylabel = "lift = (Gross / Budget)")
    
    plt.axhline(y=tbl["lift"].median(), color=colors_zebra_interview["Warm Gray"], linestyle='--', linewidth=1.5, label = "Median Overall") # doesn't make sense take from the raw

    plt.tight_layout()
    plt.savefig("..//plots/median_lift_decade.png")

    return fig