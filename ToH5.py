import sys
import pandas as pd

df = pd.read_csv(sys.argv[1], index_col=(0, 1), names=['lat', 'lon'])

df = df.reset_index()
df = df.drop_duplicates(subset=['level_0', 'level_1'])
df = df.set_index(['level_0', 'level_1'])

df.to_hdf(sys.argv[2], 'data')