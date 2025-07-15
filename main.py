import numpy as np
from scipy.stats import norm
import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("Black-Scholes Interactive Model")
st.divider()

#Calculate Black-Scholes option price for a call/put
def blackScholes(r, S, K, T, sigma, type="C"):
    d1 = (np.log(S/K) + (r+ sigma**2/2)*T)/(sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    try:
        if type == "C":
            price = S*norm.cdf(d1,0,1) - K*np.exp(-r*T)*norm.cdf(d2,0,1) # discounted strike price
        elif type == "P":
            price = K*np.exp(-r*T)*norm.cdf(-d2,0,1) - S*norm.cdf(-d1,0,1)
        return price
    except:
        print("Please Confirm all option parameters above")
    

# vars for Black-Scholes
st.sidebar.write("MADE BY DANIIL NEZHALSKYI")
r = st.sidebar.number_input("Risk-Free rate (%)", min_value=float(0), value = round(float(0.05),2)) # Risk-Free rate
S = st.sidebar.number_input("Underlying Price($)", min_value=float(0), value = round(float(100.00),2)) # underlying price
K = st.sidebar.number_input("Strike Price ($)", min_value=float(0), value = round(float(100.00),2)) # Strike price
T = st.sidebar.number_input("Time to Expiry (Years)", min_value=float(0), value = round(float(0.5),2)) # Time to Expiry
sigma = st.sidebar.number_input("Volatility (σ)", min_value=float(0), value = round(float(0.2),2))#sigma (volatility)
st.sidebar.divider()
st.sidebar.write("Heatmap Variables")
min_price = st.sidebar.number_input("Minimum Underlying Price", min_value=0.01,value=round(75.00,2))
max_price = st.sidebar.number_input("Maximum Underlying Price", min_value=0.02,value=round(125.00,2))
min_volatility = st.sidebar.slider("Minimum Volatility", float(0.01), float(1.00),0.10)
max_volatility = st.sidebar.slider("Maximum Volatility", float(0.02), float(1.00),0.30)

# Displaying the price
data = {"Risk-Free rate (%)": round(float(r),2),
        "Underlying Price($)": round(float(S),2),
        "Strike Price ($)": round(float(K),2),
        "Time to Expiry (Years)": round(float(T),2),
        "Volatility (σ)": round(float(sigma),2)}

df = pd.DataFrame(data, index=[0])
st.dataframe(df, width=1000)

col1, col2 = st.columns(2,gap="small")
bg_color1 = "#9dffc4"
bg_color2 = "#ff9ebd"
with col1:
    st.markdown(
        f"""
        <div style="background-color:{bg_color1};padding:8px;border-radius:1px;display:flex;flex-direction:column;
        align-items:center;gap:2px;">
            <p style="color:black;text-align:center;font-size:25px;">CALL</p>
            <p style="color:black;text-align:center;font-size:30px;font-weight:bold;">${round(blackScholes(r, S, K, T, sigma, type="C"),2)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"""
        <div style="background-color:{bg_color2};padding:8px;border-radius:1px;display:flex;flex-direction:column;
        align-items:center;gap:2px;">
            <p style="color:black;text-align:center;font-size:25px;">{"PUT"}</p>
            <p style="color:black;text-align:center;font-size:30px;font-weight:bold;">${round((blackScholes(r, S, K, T, sigma, type="P")),2)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Heatmap stuff
spot_prices = np.linspace(min_price, max_price, 10)         # 10 values from 80 to 120
volatilities = np.linspace(min_volatility, max_volatility, 10)      # 10 values from 0.01 to 0.8

call_matrix = []
for sigma in volatilities:
    row = []
    for S in spot_prices:
        call_price = blackScholes(r, S, K, T, sigma, type="C")
        row.append(call_price)
    call_matrix.append(row)


df2 = pd.DataFrame(call_matrix, index=np.round(volatilities, 2), columns=np.round(spot_prices, 2))
df.index.name = 'Volatility'
df.columns.name = 'Spot Price'



fig = plt.figure(figsize=(10,8))
sns.heatmap(df2,annot=True, fmt=".2f", cmap='YlOrBr')
st.divider()
col3, col4 = st.columns(2)
with col3:
    st.write("CALL Heatmap")
    st.pyplot(fig)


call_matrix2 = []
for sigma in volatilities:
    row = []
    for S in spot_prices:
        put_price = blackScholes(r, S, K, T, sigma, type="P")
        row.append(put_price)
    call_matrix2.append(row)


df2 = pd.DataFrame(call_matrix2, index=np.round(volatilities, 2), columns=np.round(spot_prices, 2))
df.index.name = 'Volatility'
df.columns.name = 'Spot Price'



fig2 = plt.figure(figsize=(10,8))
sns.heatmap(df2,annot=True, fmt=".2f", cmap='YlOrBr')
with col4:
    st.write("PUT Heatmap")
    st.pyplot(fig2)
