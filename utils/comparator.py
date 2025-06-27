def quick_dataframe_comparison(df1, df2):
    comparison = {
        "rows_a": df1.shape[0],
        "cols_a": df1.shape[1],
        "rows_b": df2.shape[0],
        "cols_b": df2.shape[1],
        "common_columns": list(set(df1.columns).intersection(set(df2.columns))),
        "unique_to_a": list(set(df1.columns) - set(df2.columns)),
        "unique_to_b": list(set(df2.columns) - set(df1.columns))
    }
    return comparison
