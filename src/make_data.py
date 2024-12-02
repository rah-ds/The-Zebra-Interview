import numpy as np
import pandas as pd

def add_metrics(df:pd.DataFrame) -> pd.DataFrame:
    # this will add the main metrics used

    df_raw_cols_ = list(df)

    df = df.replace(0, np.nan) # zeros are really nulls

    df = df.assign(lift = (df["gross"] / df["budget"]),
                    budget_log = np.log(df["budget"]),
                    gross_log = np.log(df["gross"])
                )

    # group by decades to get trend (2016 -> 2010s)
    def floor_to_decade(x):
        return np.floor(x / 10) * 10

    # kept this way to track nulls in graph
    df = df.assign(decade = df.title_year.fillna(9999).apply(floor_to_decade).astype(int)) 

    cols_added_ = [col for col in list(df) if col not in df_raw_cols_]

    print(f"shape - {df.shape}, columns added - {cols_added_}")

    return df


def get_long_text_summary(df:pd.DataFrame, piped_kw:str = None) -> pd.DataFrame:
    """takes a | operator and explodes the raw movies DataFrame that is long and summarized
    by score, and number of users that voted.
    """

    df_explode = df.iloc[df[piped_kw].str.split("|").explode().index,:]
    df_explode = df_explode.assign(kw_clean = df[piped_kw].str.split("|").explode())

    df_explode = df_explode.groupby("kw_clean").agg(
        n = ("num_users_voted", 'count'),
        num_voted = ("num_users_voted", "mean"),
        movie_score = ("movie_score", "mean"),
        movie_score_median = ("movie_score", "median")
    ).sort_values("movie_score_median", ascending=False).round(2)       

    return df_explode
