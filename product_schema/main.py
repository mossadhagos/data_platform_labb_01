import pandas as pd

# read_csv file
df = pd.read_csv( "/Users/lillmossi/Documents/github/data_platform_labb_01/data/lab 1 - csv.csv", sep=";")

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