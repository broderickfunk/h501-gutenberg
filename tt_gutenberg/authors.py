import pandas as pd


def list_authors(by_languages: bool = True, alias: bool = True) -> list[str]:

    if not by_languages or not alias:
        print("error")
    url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/"
    authors = pd.read_csv(f"{url}gutenberg_authors.csv")
    languages = pd.read_csv(f"{url}gutenberg_languages.csv")
    metadata = pd.read_csv(f"{url}gutenberg_metadata.csv")
    meta = metadata[["gutenberg_id", "author_id"]].dropna()

    merged = (
        languages.merge(meta, on="gutenberg_id", how="inner")
                    .merge(authors[["author_id", "alias"]], on="author_id", how="inner")
    )

    s = merged["alias"].astype("string").str.strip()
    s_lower = s.str.lower()

    bad = {"", "nan", "none", "null", "na", "n/a"}
    merged = merged.assign(alias_clean=s.where(~s_lower.isin(bad)))

    counts = (
        merged.dropna(subset=["alias_clean"])
              .groupby("alias_clean")
              .size()
              .sort_values(ascending=False)
    )

    return counts.index.tolist()
