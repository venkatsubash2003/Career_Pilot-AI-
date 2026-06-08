import pandas as pd 

def load_sponsorship_companies():
    df = pd.read_csv("data/sponsorship_companies_10yrs.csv")

    companies = (
        df["Company"]
        .dropna()
        .str.lower()
        .str.strip()
        .unique()
        .tolist()
    )

    return companies