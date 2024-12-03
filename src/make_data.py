import re

import numpy as np
import pandas as pd

from dotenv import find_dotenv, dotenv_values

config = dotenv_values(find_dotenv(".env"))

def clean_and_normalize_movie_title(title: str) -> str:
    """cleans the title string, normalizing it to make sure we are talking like for like
    returns a string itself, meant to be expanded and tested
    
    TODO: add robust testing for this, be specific
    """

    title = re.sub(r'[^a-zA-Z0-9\s.,!?&-]', '', title) # keep only letters, numbers, spaces, and common punctuation
    title = title.lower()
    title = title.strip() # Trim leading/trailing space
    title = re.sub(r'\s+', ' ', title) # Normalize multiple spaces to a single space
    return title


def clean_df(df:pd.DataFrame, save_local:bool = False) -> pd.DataFrame:
    """takes the raw data and does some essential cleaning on it. Deduplicates on 
    candidate key, cleans the string, and optionally returns the results to be called
    in later analysis.
    """
    
    df = df.assign(movie_title_clean = df["movie_title"].apply(lambda x: clean_and_normalize_movie_title(x)),
                   movie_franchise = df["movie_title"].apply(lambda x: x.split(":")[0] if ":" in x else np.nan))
    
    df = df.sort_values('num_users_voted', ascending=False)
    candidate_key_mask = df.duplicated(subset=['genres', 'movie_title_clean', 'movie_score']) # keep try of count
    df = df.drop_duplicates(subset=['genres', 'movie_title_clean', 'movie_score'], keep="first") # there can be multiple, want max user voted

    df = df.replace(0, np.nan) # zeros are really nulls here
    df = df.assign(content_rating = df["content_rating"].replace("Not Rated", np.nan))
    df = df.assign(movie_type = np.where(df["content_rating"].isin(['TV-MA', 'TV-14', 'TV-PG', 'TV-G', 'TV-Y7','TV-Y']), "tv", "movie"))

    # group by decades to get trend (2016 -> 2010s)
    def floor_to_decade(x):
        return np.floor(x / 10) * 10

    df = df.assign(decade = df.title_year.fillna(9999).apply(floor_to_decade).astype(int)) 

    if save_local:
        save_path = config["cleaned_data_path"]
        df.to_csv(save_path, index=False)
        print(f"saving at {save_path}")

    print("columns added - [movie_title_clean, movie_franchise, decade]")
    print(f"dropping the rows {candidate_key_mask.sum()} because they are duplicated - taking max audience score")
    
    return df


def build_metrics(df_grp:pd.DataFrame) -> pd.DataFrame:
    """builds out the metrics to use for a view,
    needs to be regenerated for different groupings and care should be had to 
    summarize budget and gross appropriately"""

    df = df_grp.copy(deep=True)
    df_raw_cols_ = list(df)
    
    ## TODO: make this dynamic and check for different groups
    #ROI gross - budget = profit => profit / budget = ROT
    df = df.assign(
                    budget_log = np.log(df["budget"]), # naturally logarithmic scale 
                    gross_log = np.log(df["gross"]),
                    lift = (df["gross"] / df["budget"]),
                    profit = (df["gross"] - df["budget"]),
                    ROI = ((df["gross"] - df["budget"])/ df["budget"]) * 100 # profit / budget
                )

    #TODO: add in CAGR separately and care needs to be made about the year
    cols_added_ = [col for col in list(df) if col not in df_raw_cols_]
    print(f"shape - {df.shape}, columns added - {cols_added_}")
    return df

def build_cagr(df_grp:pd.DataFrame, year_col:str, metric_col:str) -> float:
    """builds continuous annual growth rate from a pandas view.
    
    add in testing to make sure these are valid values, useful for broad forecasting."""
    
    df = df_grp.copy(deep=True)
    df = df.sort_values(by=year_col)

    start_value = df[metric_col].iloc[0]
    end_value = df[metric_col].iloc[-1]
    num_years = df[year_col].iloc[-1] - df[year_col].iloc[0]  # diff in years (end - start)

    cagr = ((end_value / start_value) ** (1 / num_years) - 1) * 100
    return cagr

def filter_tv_shows(df) ->pd.DataFrame:
    """filters out probable tv shows by lack of title and rating
    
    see 00_profiling_data.ipynb for more details"""
    
    assert "movie_type" in list(df), "run clean_data first"

    df = df.loc[df["movie_type"] == "movie"]
    df = df.loc[df["title_year"].notnull(), :]

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
