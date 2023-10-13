import requests
import json
import pandas as pd

query = """
{
  pools(
    orderBy: createdAtTimestamp,
    orderDirection: desc,
    where: {token0_: {symbol: "USDC"}, token1_: {symbol: "WETH"}},
    skip: %d
  ) {
    id
    totalValueLockedUSD
    token0 {
      symbol
    }
    token1 {
      symbol
    }
    feeTier
    volumeUSD
    liquidity
    token0Price
    token1Price
    volumeToken0
    volumeToken1
    feesUSD
    createdAtTimestamp
    createdAtBlockNumber
    totalValueLockedToken0
    totalValueLockedToken1
    tick
  }
}
"""

url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'


frames = []
for i in range(0,500,10):
    tmp_query = query%(i)
    r = requests.post(url, json={'query': tmp_query})
    json_data = json.loads(r.text)
    try:
        df_data = json_data['data']['pools']
        df = pd.DataFrame(df_data)
        frames.append(df)
    except KeyError:
        break

result = pd.concat(frames)
result.to_csv("Pool_Data.csv")
