import pandas as pd

df = pd.read_csv('Datasets/Pool_Data.csv')

print(df["createdAtTimestamp"])

dfToken0WETH = df[df['token0'].str.contains('WETH')]
dfToken0USDC = df[df['token0'].str.contains('USDC')]

dfToken0 = pd.concat([dfToken0WETH, dfToken0USDC]).reset_index(drop=True)

dfToken1WETH = df[df['token1'].str.contains('WETH')]
dfToken1USDC = df[df['token1'].str.contains('USDC')]

dfToken1 = pd.concat([dfToken1WETH, dfToken1USDC]).reset_index(drop=True)

dfTokens = pd.concat([dfToken0, dfToken1]).reset_index(drop=True)
