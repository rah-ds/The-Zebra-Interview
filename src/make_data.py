import pandas as pd

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