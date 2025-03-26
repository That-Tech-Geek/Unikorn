import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def simulate_scenario(initial_users=100, fee=999, churn=0.005, growth_rate=0.05, fixed_cost=3500, var_cost=1, months=36):
    users = [initial_users]
    revenue = []
    total_cost = []
    net_profit = []
    cumulative_cash_flow = []

    cumulative = 0

    for m in range(1, months + 1):
        if m > 1:
            new_users = users[-1] * growth_rate
            churn_users = users[-1] * churn
            current_users = users[-1] + new_users - churn_users
            users.append(current_users)
        else:
            current_users = users[-1]

        current_revenue = current_users * fee
        monthly_var_cost = current_users * var_cost
        current_total_cost = fixed_cost + monthly_var_cost
        current_net_profit = current_revenue - current_total_cost

        cumulative += current_net_profit

        revenue.append(current_revenue)
        total_cost.append(current_total_cost)
        net_profit.append(current_net_profit)
        cumulative_cash_flow.append(cumulative)

    df = pd.DataFrame({
        'Month': np.arange(1, months + 1),
        'Users': users,
        'Revenue': revenue,
        'Total Cost': total_cost,
        'Net Profit': net_profit,
        'Cumulative Cash Flow': cumulative_cash_flow
    })
    return df

# Streamlit Interface
st.title("Financial Simulation Model")

# Sidebar inputs
initial_users = st.sidebar.number_input("Initial Users", min_value=1, value=100)
fee = st.sidebar.number_input("Monthly Fee per User", min_value=1.0, value=999.0)
churn = st.sidebar.number_input("Monthly Churn Rate (%)", min_value=0.0, max_value=100.0, value=0.5) / 100
growth_rate = st.sidebar.number_input("Monthly Growth Rate (%)", min_value=0.0, max_value=100.0, value=5.0) / 100
fixed_cost = st.sidebar.number_input("Fixed Monthly Operating Cost", min_value=0.0, value=3500.0)
var_cost = st.sidebar.number_input("Variable Cost per User", min_value=0.0, value=1.0)
months = st.sidebar.number_input("Number of Months", min_value=1, value=36)

# Simulation Run
df_bootstrap = simulate_scenario(initial_users, fee, churn, growth_rate, fixed_cost, var_cost, months)

# Display Results
st.subheader("Simulation Results")
st.dataframe(df_bootstrap.tail(60))

# Plotting Results
st.subheader("Visual Analysis")
fig = px.line(df_bootstrap, x='Month', y=['Users', 'Revenue', 'Cumulative Cash Flow'],
              labels={'value': 'Amount', 'variable': 'Metrics'},
              title='Simulation Trends')
st.plotly_chart(fig)
