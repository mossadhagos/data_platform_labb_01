import pandas as pd
"""""
Laboration 1 – Data Pipeline med Pandas.

Programmet läser in produktdata från en CSV-fil, transformerar och rensar datan,
identifierar datakvalitetsproblem, separerar ogiltiga värden och skapar ett
curated dataset för analys.

Slutligen genereras sammanfattningsfiler med statistik såsom snittpris,
medianpris och antal produkter samt (bonus) prisanalys.
"""""

def load_data(filepath):
    """Läser in CSV-filen med korrekt separator."""
    return pd.read_csv(filepath, sep=";")


def transform_data(df):
    """Rensar och transformerar data."""

    # Rensa produktnamn
    df["name"] = (
        df["name"]
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    # Säkerställ numeriskt pris
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    return df


def flag_quality_issues(df):
    """Flaggar möjliga datakvalitetsproblem."""

    df["missing_currency"] = df["currency"].isna() | (df["currency"] == "")
    df["is_free"] = df["price"] == 0

    # IQR-metod för att hitta extrema priser
    Q1 = df["price"].quantile(0.25)
    Q3 = df["price"].quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + 1.5 * IQR

    df["extreme_price"] = df["price"] > upper_bound

    return df


def validate_data(df):
    """Separera ogiltig data från giltig data."""

    rejected_df = df[
        (df["price"].isna()) |
        (df["price"] < 0) |
        (df["currency"].isna()) |
        (df["currency"] == "")
        ]

    clean_df = df.drop(rejected_df.index)

    return rejected_df, clean_df


def create_summary(df, clean_df):
    """Skapar analytics summary."""

    average_price = clean_df["price"].mean()
    median_price = clean_df["price"].median()
    total_products = len(clean_df)
    missing_price_count = df["price"].isna().sum()

    summary_df = pd.DataFrame({
        "snitt_pris": [average_price],
        "median_pris": [median_price],
        "antal_produkter": [total_products],
        "antal_produkter_med_saknat_pris": [missing_price_count]
    })

    summary_df.to_csv("summary.csv", index=False)


def create_price_analysis(clean_df):
    """Bonus: skapar price analysis."""

    top_10_expensive = clean_df.sort_values(
        by="price", ascending=False
    ).head(10)

    median_price = clean_df["price"].median()

    clean_df["price_deviation"] = abs(
        clean_df["price"] - median_price
    )

    top_10_deviation = clean_df.sort_values(
        by="price_deviation", ascending=False
    ).head(10)

    price_analysis_df = pd.concat(
        [top_10_expensive, top_10_deviation]
    )

    price_analysis_df.to_csv("price_analysis.csv", index=False)


def main():
    """Kör hela data pipeline-processen."""

    df = load_data(
        "/Users/lillmossi/Documents/github/data_platform_labb_01/data/lab 1 - csv.csv"
    )

    df = transform_data(df)
    df = flag_quality_issues(df)

    rejected_df, clean_df = validate_data(df)

    rejected_df.to_csv("rejected.csv", index=False)
    clean_df.to_csv("clean.csv", index=False)

    create_summary(df, clean_df)
    create_price_analysis(clean_df)

    print("Pipeline körd klart.")


if __name__ == "__main__":
    main()