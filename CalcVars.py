import pandas as pd

spread_df = pd.read_csv('Datasets/Spread_Data.csv')  

cols = ["Zl", "Z", "Zu", "alpha", "spread"]

vars_df = pd.DataFrame(columns=cols)

vars_df["Zl"] = spread_df["tick_lower"]
vars_df["Z"] = spread_df["adjusted_current_price"]
vars_df["Zu"] = spread_df["tick_upper"]
vars_df["alpha"] = spread_df["alpha"]
vars_df["spread"] = vars_df['Zu'] - vars_df['Zl']

vars_df.to_csv("ConvVars.csv")

print(min(spread_df["pool_timestamp"]))
print(max(spread_df["pool_timestamp"]))
