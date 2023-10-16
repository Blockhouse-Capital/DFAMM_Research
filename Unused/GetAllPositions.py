import requests
import json
import pandas as pd
from GenerateSpread import compute_spread

# spread = tickupper - ticklower 

query = """{
  positions(where: {token0_: {symbol: "USDC"}, token1_: {symbol: "WETH"}}, skip: %d) {
    id
  }
}"""

url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'

frames = []
for i in range(0, 150000,200):
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
result.to_csv("Positions.csv")
