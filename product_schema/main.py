import pandas as pd

# read_csv file
df = pd.read_csv("/Users/lillmossi/Documents/github/data_platform_labb_01/data/lab 1 - csv.csv", sep=";")

df["name"] = df["name"].str.strip()
df["name"] = (
    df["name"]
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)
print(df.head())

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["missing_currency"] = df["currency"].isna()
df["missing_currency"] = df["currency"].isna() | (df["currency"] == "")
df["is_free"] = df["price"] == 0
df["extreme_price"] = df["price"] > 10000

Q1 = df["price"].quantile(0.25)
Q3 = df["price"].quantile(0.75)
IQR = Q3 - Q1

upper_bound = Q3 + 1.5 * IQR

df["extreme_price"] = df["price"] > upper_bound
print(df[["price", "missing_currency", "is_free", "extreme_price"]].head())
print("Missing currency:", df["missing_currency"].sum())
print("Free products:", df["is_free"].sum())
print("Extreme prices:", df["extreme_price"].sum())

rejected_df = df[
    (df["price"].isna()) |
    (df["price"] < 0)|
    (df["currency"].isna()) |
    (df["currency"] == "")
]

clean_df = df.drop(rejected_df.index)

print("Original:", len(df))
print("Rejected:", len(rejected_df))
print("Clean:", len(clean_df))

rejected_df.to_csv("rejected.csv", index=False)
clean_df.to_csv("clean.csv", index=False)


average_price = clean_df["price"].mean()
median_price = clean_df["price"].median()
total_product = len(clean_df)
missing_price_count = df["price"].isna().sum()

summary_df = pd.DataFrame({
    "snitt_pris": [average_price],
    "median_pris": [median_price],
    "antal_produkter": [total_product],
    "antal_produkter_med_saknat_pris": [missing_price_count]
})

summary_df.to_csv("summary.csv", index=False)

top_10_expensive = clean_df.sort_values(by="price", ascending=False).head(10)

median_price = clean_df["price"].median()

top_10_deviation = clean_df.sort_values(by="price", ascending=False).tail(10)

price_analysis_df = pd.concat([top_10_expensive, top_10_deviation])

price_analysis_df.to_csv("price_analysis.csv", index=False)