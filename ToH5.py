import sys
import pandas as pd

df = pd.read_csv(sys.argv[1], index_col=(0, 1), names=['lat', 'lon'])

df.to_hdf(sys.argv[2], 'data')