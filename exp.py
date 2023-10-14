import pandas as pd
from Spread import compute_spread

df = pd.read_csv('Datasets/Positions.csv')

column_names= ["adjusted_current_price", "current_tick", "tick_lower", "tick_upper", "adjusted_amount0", "token0", "adjusted_amount1", "token1"]
spread_df = pd.DataFrame(columns=column_names)


for id in df["id"]:
    adjusted_current_price, current_tick, tick_lower, tick_upper, adjusted_amount0, token0, adjusted_amount1, token1 = compute_spread(id)
    spread_df.loc[id,"adjusted_current_price"] = adjusted_current_price
    spread_df.loc[id,"current_tick"] = current_tick
    spread_df.loc[id,"tick_lower"] = tick_lower
    spread_df.loc[id,"tick_upper"] = tick_upper
    spread_df.loc[id,"adjusted_amount0"] = adjusted_amount0
    spread_df.loc[id,"token0"] = token0
    spread_df.loc[id,"adjusted_amount1"] = adjusted_amount1
    spread_df.loc[id,"token1"] = token1


spread_df.to_csv("Spread_Data.csv")