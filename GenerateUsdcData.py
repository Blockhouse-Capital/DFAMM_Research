import requests
import json
import pandas as pd

# Uniswap V3 token data

token_usdc_id = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

url = 'https://api.thegraph.com/subgraphs/name/ianlapham/v3-minimal'
frames = []
query = """query {
tokenDayDatas (where : {token: "%s"}, orderBy: date, orderDirection: desc, skip:%d)
{
date
volumeUSD
totalValueLockedUSD
priceUSD
feesUSD
open
high
low
close
}
}"""
for i in range(0,500,10):
    tmp_query = query%(token_usdc_id,i)
    r = requests.post(url, json={'query': tmp_query})
    json_data = json.loads(r.text)
    try:
        df_data = json_data['data']["tokenDayDatas"]
        df = pd.DataFrame(df_data)
        frames.append(df)
    except KeyError:
        break

result = pd.concat(frames)
result['date'] = pd.to_datetime(result['date'], unit='s')
result[["volumeUSD","totalValueLockedUSD","feesUSD","priceUSD","open","high","low","close"]] = result[["volumeUSD","totalValueLockedUSD","feesUSD","priceUSD","open","high","low","close"]].apply(pd.to_numeric)
result['token_id'] = token_usdc_id
result.to_csv("USDC_Data.csv")

