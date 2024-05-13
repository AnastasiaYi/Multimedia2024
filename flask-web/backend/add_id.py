import pandas as pd
print(pd.__version__)
df = pd.read_csv('/Users/jeffreylu/Downloads/features_514.csv')
df['id'] = range(len(df))
column_values = df['id'].values
print(column_values)
df.to_csv('/Users/jeffreylu/Downloads/features_514_id.csv', index=False)