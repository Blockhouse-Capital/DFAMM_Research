import numpy as np

# alpha_0 = alpha_t(k, bond_prices[0, 0], simulated_spreads[i, 0] / 2, simulated_spreads[i, 0] / 2)

# Define a function to calculate opportunity cost
def calculate_opportunity_cost(alpha_0, alpha_d, risk_free_rate_data, dt_values):
    opportunity_cost = 0.0
    
    for alpha, r, dt in zip(alpha_d, risk_free_rate_data, dt_values):
        opportunity_cost += (alpha_0 - alpha) * r * dt
    
    return opportunity_cost

# Example usage of the calculate_opportunity_cost function:
# opportunity_cost_i = calculate_opportunity_cost(alpha_0, alpha_d, r, dt)

# Converting lists to NumPy arrays (as in your existing code)...

print("Complete")

"""
In the code above, the calculate_opportunity_cost function is defined to calculate the opportunity cost using the inputs alpha_0, alpha_d, r (risk-free rate), and dt (time interval). You can call this function within your loop to calculate the daily opportunity cost as you did in your existing code.
