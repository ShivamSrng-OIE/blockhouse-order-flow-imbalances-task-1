import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from ofi_features import compute_best_level_ofi, compute_multi_level_ofi, compute_integrated_ofi


st.set_page_config(
    layout="wide",
    page_title="Order Flow Imbalance (OFI) Dashboard",
)
st.title("BlockHouse Task 1 - Interactive Order Flow Imbalance (OFI) Dashboard")

st.sidebar.header("Configuration")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

ofi_type = st.sidebar.radio(
    "Select OFI Type", 
    [
        "Best-Level", 
        "Multi-Level", 
        "Integrated"
    ]
)

if ofi_type in ["Multi-Level", "Integrated"]:
    window_size = st.sidebar.slider(
        "Rolling Window Size (h, in events)", 
        min_value=10, 
        max_value=200, 
        value=30
    )
    lob_depth = st.sidebar.slider(
        "Order Book Depth (Levels)", 
        min_value=1, 
        max_value=10, 
        value=10
    )
else:
    window_size = 30
    lob_depth = 1

if ofi_type == "Integrated":
    show_explain = st.sidebar.checkbox(
        "Show Explainability (PCA Weights)", 
        value=True
    )
    st.sidebar.caption(
        "I really like explainability, so I added PCA weights to the integrated OFI. This helps us understand how much each level contributes to the overall OFI."
    )
else:
    show_explain = False

def load_data():
    if uploaded_file:
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_csv("data/first_25000_rows.csv")

df = load_data()
st.success("Data loaded successfully.")

if ofi_type == "Best-Level":
    df["ofi"] = compute_best_level_ofi(df)
elif ofi_type == "Multi-Level":
    df["ofi"] = compute_multi_level_ofi(df, levels=lob_depth)
elif ofi_type == "Integrated":
    df["ofi"] = compute_integrated_ofi(df, levels=lob_depth)

df["ts_event"] = pd.to_datetime(df["ts_event"])
df["smoothed_ofi"] = df["ofi"].rolling(window=window_size, min_periods=1).mean()

st.subheader(f"Smoothed {ofi_type} OFI Time Series")
fig, ax = plt.subplots(figsize=(16, 6))
ax.plot(df["ts_event"], df["smoothed_ofi"], label=f"{ofi_type} OFI", color="navy")
ax.fill_between(df["ts_event"], df["smoothed_ofi"], 0, where=df["smoothed_ofi"] > 0, color='green', alpha=0.1)
ax.fill_between(df["ts_event"], df["smoothed_ofi"], 0, where=df["smoothed_ofi"] < 0, color='red', alpha=0.1)
ax.set_xlabel("Timestamp")
ax.set_ylabel("OFI Value")
ax.set_title(f"Smoothed {ofi_type} Order Flow Imbalance")
ax.legend()
ax.grid(True)
st.pyplot(fig)

if ofi_type == "Integrated" and show_explain:
    st.subheader("PCA Component Weights for Integrated OFI")
    ofi_matrix = []
    for lvl in range(lob_depth):
        bid_sz = df[f"bid_sz_0{lvl}"]
        ask_sz = df[f"ask_sz_0{lvl}"]
        bid_px = df[f"bid_px_0{lvl}"]
        ask_px = df[f"ask_px_0{lvl}"]
        level_ofi = []
        for i in range(1, len(df)):
            prev_bid_px, prev_ask_px = bid_px.iloc[i-1], ask_px.iloc[i-1]
            prev_bid_sz, prev_ask_sz = bid_sz.iloc[i-1], ask_sz.iloc[i-1]
            curr_bid_px, curr_ask_px = bid_px.iloc[i], ask_px.iloc[i]
            curr_bid_sz, curr_ask_sz = bid_sz.iloc[i], ask_sz.iloc[i]

            bid_ofi = curr_bid_sz if curr_bid_px > prev_bid_px else (
                curr_bid_sz - prev_bid_sz if curr_bid_px == prev_bid_px else -prev_bid_sz)
            ask_ofi = -curr_ask_sz if curr_ask_px < prev_ask_px else (
                prev_ask_sz - curr_ask_sz if curr_ask_px == prev_ask_px else -prev_ask_sz)
            level_ofi.append(bid_ofi - ask_ofi)
        ofi_matrix.append(level_ofi)

    matrix = np.array(ofi_matrix).T
    pca = PCA(n_components=1)
    pca.fit(matrix)
    weights = pca.components_[0]

    st.bar_chart(pd.Series(weights, index=[f"Level {i+1}" for i in range(len(weights))], name="PCA Weight"))
    st.caption("These weights indicate the relative importance of each depth level in constructing the Integrated OFI via PCA.")