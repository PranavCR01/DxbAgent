from roi_calculator.bayut_fetcher import get_dubai_data
import os
if os.path.exists("data/bayut_cache.parquet"):
    os.remove("data/bayut_cache.parquet")


df = get_dubai_data()
print(df.head())
