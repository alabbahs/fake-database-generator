import pandas as pd

def normalize_column(col):
    return col.astype(str).str.strip().str.lower()

def add_stats():
    df_data = pd.read_csv('data/database_csvs/data.csv', encoding='ISO-8859-1')
    df_stats = pd.read_csv('data/database_csvs/data_stats.csv')

    df_stats.rename(columns={"Column": "column_name", "TableName": "table_name"}, inplace=True)

    df_data["table_name"] = normalize_column(df_data["table_name"])
    df_data["column_name"] = normalize_column(df_data["column_name"])
    df_stats["table_name"] = normalize_column(df_stats["table_name"])
    df_stats["column_name"] = normalize_column(df_stats["column_name"])

    df_merged = df_data.merge(
        df_stats,
        on=["table_name", "column_name"],
        how="left"
    )

    df_merged.to_csv('data/database_csvs/data_with_stats.csv', index=False)
    print("✅ Data with stats written to data/database_csvs/data_with_stats.csv")

if __name__ == "__main__":
    add_stats()
