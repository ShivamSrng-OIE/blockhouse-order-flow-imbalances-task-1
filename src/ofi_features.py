import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

def compute_best_level_ofi(
        df: pd.DataFrame
    ) -> pd.Series:
    """
    Compute the best-level order flow imbalance (OFI) for a given DataFrame. The OFI is calculated based on the bid and ask prices and sizes at the best level.
    
    Args:
        - df (pd.DataFrame): DataFrame containing the bid and ask prices and sizes.
    
    Returns:
        - pd.Series: A Series containing the best-level OFI values.
    """
    
    ofi_values = [0]
    for i in range(1, len(df)):
        prev_bid_px, prev_ask_px = df.loc[i-1, "bid_px_00"], df.loc[i-1, "ask_px_00"]
        prev_bid_sz, prev_ask_sz = df.loc[i-1, "bid_sz_00"], df.loc[i-1, "ask_sz_00"]
        curr_bid_px, curr_ask_px = df.loc[i, "bid_px_00"], df.loc[i, "ask_px_00"]
        curr_bid_sz, curr_ask_sz = df.loc[i, "bid_sz_00"], df.loc[i, "ask_sz_00"]

        bid_ofi = curr_bid_sz if curr_bid_px > prev_bid_px else (
            curr_bid_sz - prev_bid_sz if curr_bid_px == prev_bid_px else -prev_bid_sz)

        ask_ofi = -curr_ask_sz if curr_ask_px < prev_ask_px else (
            prev_ask_sz - curr_ask_sz if curr_ask_px == prev_ask_px else -prev_ask_sz)

        ofi_values.append(bid_ofi - ask_ofi)
    return pd.Series(ofi_values, index=df.index, name="best_level_ofi")


def compute_multi_level_ofi(
        df: pd.DataFrame, 
        levels: int = 10
    ) -> pd.Series:
    """
    Compute the multi-level order flow imbalance (OFI) for a given DataFrame. The OFI is calculated based on the bid and ask prices and sizes at multiple levels.
    
    Args:
        - df (pd.DataFrame): DataFrame containing the bid and ask prices and sizes.
        - levels (int): Number of levels to compute the OFI for.
    
    Returns:
        - pd.Series: A Series containing the multi-level OFI values.
    """
    
    ofi_matrix = []
    for lvl in range(levels):
        bid_px, ask_px = f"bid_px_0{lvl}", f"ask_px_0{lvl}"
        bid_sz, ask_sz = f"bid_sz_0{lvl}", f"ask_sz_0{lvl}"
        level_ofi = [0]
        for i in range(1, len(df)):
            prev_bid_px, prev_ask_px = df.loc[i-1, bid_px], df.loc[i-1, ask_px]
            prev_bid_sz, prev_ask_sz = df.loc[i-1, bid_sz], df.loc[i-1, ask_sz]
            curr_bid_px, curr_ask_px = df.loc[i, bid_px], df.loc[i, ask_px]
            curr_bid_sz, curr_ask_sz = df.loc[i, bid_sz], df.loc[i, ask_sz]

            bid_ofi = curr_bid_sz if curr_bid_px > prev_bid_px else (
                curr_bid_sz - prev_bid_sz if curr_bid_px == prev_bid_px else -prev_bid_sz)
            ask_ofi = -curr_ask_sz if curr_ask_px < prev_ask_px else (
                prev_ask_sz - curr_ask_sz if curr_ask_px == prev_ask_px else -prev_ask_sz)

            level_ofi.append(bid_ofi - ask_ofi)
        ofi_matrix.append(level_ofi)
    
    return pd.Series(np.sum(ofi_matrix, axis=0), index=df.index, name="multi_level_ofi")


def compute_integrated_ofi(
        df: pd.DataFrame, 
        levels: int = 10
    ) -> pd.Series:
    """
    Compute the integrated order flow imbalance (OFI) for a given DataFrame. The OFI is calculated based on the bid and ask prices and sizes at multiple levels, and then PCA is applied to integrate the levels.
    
    Args:
        - df (pd.DataFrame): DataFrame containing the bid and ask prices and sizes.
        - levels (int): Number of levels to compute the OFI for.
    
    Returns:
        - pd.Series: A Series containing the integrated OFI values.
    """
    
    ofi_matrix = []
    for lvl in range(levels):
        bid_px, ask_px = f"bid_px_0{lvl}", f"ask_px_0{lvl}"
        bid_sz, ask_sz = f"bid_sz_0{lvl}", f"ask_sz_0{lvl}"
        level_ofi = [0]
        for i in range(1, len(df)):
            prev_bid_px, prev_ask_px = df.loc[i-1, bid_px], df.loc[i-1, ask_px]
            prev_bid_sz, prev_ask_sz = df.loc[i-1, bid_sz], df.loc[i-1, ask_sz]
            curr_bid_px, curr_ask_px = df.loc[i, bid_px], df.loc[i, ask_px]
            curr_bid_sz, curr_ask_sz = df.loc[i, bid_sz], df.loc[i, ask_sz]

            bid_ofi = curr_bid_sz if curr_bid_px > prev_bid_px else (
                curr_bid_sz - prev_bid_sz if curr_bid_px == prev_bid_px else -prev_bid_sz)
            ask_ofi = -curr_ask_sz if curr_ask_px < prev_ask_px else (
                prev_ask_sz - curr_ask_sz if curr_ask_px == prev_ask_px else -prev_ask_sz)

            level_ofi.append(bid_ofi - ask_ofi)
        ofi_matrix.append(level_ofi)
    matrix = np.array(ofi_matrix).T
    pca = PCA(n_components=1)
    principal_component = pca.fit_transform(matrix).flatten()
    weights = pca.components_[0]
    integrated = principal_component / np.sum(np.abs(weights))
    most_important_level = np.argmax(np.abs(weights))
    print(f" -- Most important level for integrated OFI: {most_important_level + 1} (weight: {round(weights[most_important_level], 3)})")
    return pd.Series(integrated, index=df.index, name="integrated_ofi")