import pandas as pd
import numpy as np

#from ipynb.fs.full.PLCode import calculate_conv_cost 

#See denominator or convexity cost
def LP_spread_conversion(Z, Zl, Zu):
    sigma_u = -2 * (Z**(1/2)) / (Zu**(1/2)) + 2
    sigma_l = -2 * (Z**(1/2)) / (Zl**(1/2)) + 2

    return sigma_u + sigma_l

#Quadratic Variation, needs multiple step ahead forecast, maybe generate 20 forecasts over the short block interval
def calc_QV(Z):
    log_returns = np.diff(np.log(Z))
    QV = []

    for i in range(1, len(log_returns)):
        QV.append(np.sum(np.diff(log_returns[i-1:i])**2))
    QV2 = pd.Series(QV)
    return QV2

def calculate_conv_cost(alpha_lu, Zl, Zu, Z, num_positions):
    integral = 0
    for i in range(len(Z)):
        alpha_curr_lu = alpha_lu[i]
        spread = LP_spread_conversion(Z[i], Zl[i], Zu[i])

        quad_var = calc_QV(Z[:i])

        quad_varl = quad_var.tolist()    

        integral += alpha_curr_lu / (2* spread * Z[i]**2) * sum(quad_varl)

    return integral

spread_df = pd.read_csv('Datasets/Spread_Data.csv') 

cols = ["Zl", "Z", "Zu", "alpha", "spread"]

vars_df = pd.DataFrame(columns=cols)

pos_weights = spread_df["num_positions"]/sum(spread_df["num_positions"])

vars_df["Zl"] = spread_df["tick_lower"]
vars_df["Z"] = spread_df["adjusted_current_price"]
vars_df["Zu"] = spread_df["tick_upper"]
vars_df["alpha"] = spread_df["alpha"]
vars_df["spread"] = vars_df['Zu'] - vars_df['Zl']


#vars_df.to_csv("ConvVars.csv")

integral = calculate_conv_cost(vars_df["alpha"], vars_df["Zl"], vars_df["Zu"], vars_df["Z"], spread_df["num_positions"])

print(integral)