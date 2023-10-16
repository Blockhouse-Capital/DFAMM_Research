import pandas as pd
from Spread import compute_spread

df = pd.read_csv('Datasets/Positions.csv')

column_names= ["pool_block", "pool_timestamp", "adjusted_current_price", "tick_lower", "tick_upper", "adjusted_amount0", "token0", "adjusted_amount1", "token1"]
spread_df = pd.DataFrame(columns=column_names)

pools = ["0x07a72f8f6a29cf501e7226ca82264f9ee79380e7", "0x11c990d06df093fb7361356b16985051a65ebe2e", 
"0x5630ab57ee56ea296833d90cc7d96b6cb5bd2585", "0x657979310186d5e48d6f2df2be8ca4259d178554", 
"0x7bea39867e4169dbe237d55c8242a8f2fcdcc387", "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640", 
"0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8", "0xe0554a476a092703abdb3ef35c80e0d76d32939f"]

for id in pools:
    alpha, pool_block, pool_timestamp, adjusted_current_price, tick_lower, tick_upper, adjusted_amount0, token0, adjusted_amount1, token1 = compute_spread(id)
    spread_df.loc[id,"pool_block"] = pool_block
    spread_df.loc[id,"pool_timestamp"] = pool_timestamp
    spread_df.loc[id,"adjusted_current_price"] = adjusted_current_price
    for tick in tick_lower:
        spread_df.loc[id,"tick_lower"] = tick
    
    for tick in tick_upper:
        spread_df.loc[id,"tick_upper"] = tick
    spread_df.loc[id,"adjusted_amount0"] = adjusted_amount0
    spread_df.loc[id,"token0"] = token0
    spread_df.loc[id,"adjusted_amount1"] = adjusted_amount1
    spread_df.loc[id,"token1"] = token1
    spread_df.loc[id,"alpha"] = alpha

spread_df.to_csv("Spread_Data.csv")