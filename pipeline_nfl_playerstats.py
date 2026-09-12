# pipeline_nfl_playerstats.py
import pandas as pd
import nflreadpy as nfl
from db_utils import load_to_postgres

print("Step 1: Fetching NFL player stats via nflreadpy...")

# Pull player stats for the recent seasons
# Note: nflreadpy returns a data format easily handled by pandas
seasons = [2021,2022,2023,2024,2025]
df_player_stats = nfl.load_player_stats(seasons)

# Convert to pandas DataFrame if it isn't one already
df = df_player_stats.to_pandas()

print(f"Successfully fetched {len(df)} rows of data.")


print("\n Step 2: Saving local CSV backup...")
df.to_csv("~/de_lab/nfl_stats_pipeline/raw_backup.csv", index=False)



print("\n Step3: Offloading to Postgres utility...")
# Pass dataframe into DB script
load_to_postgres(df, table_name="weekly_player_stats",schema="raw")


print("Pipeline finished successfully")
