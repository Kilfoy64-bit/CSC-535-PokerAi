import pandas as pd
import numpy as np
df = pd.read_csv("hands.csv")
cdf = df.copy()
cdf.columns
for col in cdf.columns:
    cdf['c'+col] = cdf[col].copy()
# Create computer index flag and merge
cdf = cdf[['cd1', 'cd1s', 'cd2', 'cd2s', 'cf1', 'cf1s', 'cf2',
           'cf2s', 'cf3', 'cf3s', 'ct1', 'ct1s', 'cr1', 'cr1s']]
# Randomize and reindex
cdf = cdf.sample(frac=1)
cdf.reset_index(drop=True)
df = df.join(cdf)
df.to_csv('randomgames.csv')
