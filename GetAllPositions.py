
import requests
import json
import pandas as pd

# spread = tickupper - ticklower 

# pools = ["0x07a72f8f6a29cf501e7226ca82264f9ee79380e7", "0x11c990d06df093fb7361356b16985051a65ebe2e", 
# "0x5630ab57ee56ea296833d90cc7d96b6cb5bd2585", "0x657979310186d5e48d6f2df2be8ca4259d178554", 
# "0x7bea39867e4169dbe237d55c8242a8f2fcdcc387", "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640", 
# "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8", "0xe0554a476a092703abdb3ef35c80e0d76d32939f"]

query = """{
  positions(where: {token0_: {symbol: "USDC"}, token1_: {symbol: "WETH"}}, skip: %d) {
    id
  }
}"""

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
result.to_csv("Positions.csv")
