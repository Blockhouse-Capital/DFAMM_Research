
import requests
import json
import pandas as pd

# spread = tickupper - ticklower 

query = """
 query {
  positions (skip : %d ,orderBy: liquidity , orderDirection: desc)
  {
    id
    owner
    pool
    {
      id
    }
    token0
    {
      id
    }
    token1
    {
      id
    }
    tickLower
    {
      id
    }
    tickUpper
    {
      id
    }
    liquidity
    depositedToken0
    depositedToken1
    withdrawnToken0
    withdrawnToken1
    collectedFeesToken0
    collectedFeesToken1
    transaction
    {
      id
    }
    feeGrowthInside0LastX128
    feeGrowthInside1LastX128
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
        df_data = json_data['data']['positions']
        df = pd.DataFrame(df_data)
        frames.append(df)
    except KeyError:
        break

result = pd.concat(frames)
result.to_csv("LP_Data.csv")


