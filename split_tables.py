import pandas as pd


def split_tables():
    df = pd.read_csv('data/database_csvs/data.csv', encoding='ISO-8859-1')

    for table, group_df in  df.groupby("TableName"):
        print(f"Table: {table}")
        group_df.to_csv(f"data/split_tables/{table}.csv", index=False)