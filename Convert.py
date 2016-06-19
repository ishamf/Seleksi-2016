import sys
import pandas as pd

print("reading data...")
dfs = pd.read_csv(sys.argv[1], index_col=0, chunksize=100)

print("writing up...")
with open(sys.argv[2], 'w') as f:
    for df in dfs:
        pol = df.POLYLINE
        cpl = pol[~(pol == '[]')]
        sdf = pd.to_numeric(cpl.str.split(',', expand=True)
                               .stack()
                               .str.replace('\[|\]', ''))
        odds = sdf[1::2]
        evens = sdf[::2]
        odds.index = pd.MultiIndex.from_tuples(odds.index.map(lambda x: (x[0], (x[1]-1)//2)))
        evens.index = pd.MultiIndex.from_tuples(evens.index.map(lambda x: (x[0], x[1]//2)))
        fdf = pd.concat([odds, evens], axis=1)
        fdf.to_csv(f, header=False)