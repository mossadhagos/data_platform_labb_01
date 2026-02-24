import pandas as pd



# read_csv file
df = pd.read_csv(
"/Users/lillmossi/Documents/github/data_platform_labb_01/data/lab 1 - csv.csv", )

dirty_df = pd.read_json("products.json")

print(dirty_df.head())
print(dirty_df.info())
print(dirty_df.describe())