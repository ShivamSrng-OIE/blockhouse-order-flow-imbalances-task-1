import pandas as pd

def compute_best_level_ofi(
        df: pd.DataFrame
    ) -> pd.Series:
    """
    Compute Best-Level Order Flow Imbalance (OFI) using level 0 bid/ask price and size.
    OFI tells us whether there's more buying pressure or selling pressure.

    Args:
        - df (pd.DataFrame): DataFrame with order book data. Should contain bid_px_00, ask_px_00, bid_sz_00, ask_sz_00 columns.

    Returns:
        - pd.Series: A column of OFI values (one per row, same length as df)
    """

    ofi_values = [0]
    for i in range(1, len(df)):
        prev_bid_px = df.loc[i-1, "bid_px_00"]
        prev_ask_px = df.loc[i-1, "ask_px_00"]
        prev_bid_sz = df.loc[i-1, "bid_sz_00"]
        prev_ask_sz = df.loc[i-1, "ask_sz_00"]

        curr_bid_px = df.loc[i, "bid_px_00"]
        curr_ask_px = df.loc[i, "ask_px_00"]
        curr_bid_sz = df.loc[i, "bid_sz_00"]
        curr_ask_sz = df.loc[i, "ask_sz_00"]

        # ----------- Compute Bid-side OFI (buy orders) ------------
        if curr_bid_px > prev_bid_px:
            bid_ofi = curr_bid_sz
        elif curr_bid_px == prev_bid_px:
            bid_ofi = curr_bid_sz - prev_bid_sz
        else:
            bid_ofi = -prev_bid_sz

        # ----------- Compute Ask-side OFI (sell orders) ------------ 
        if curr_ask_px < prev_ask_px:
            ask_ofi = -curr_ask_sz  
        elif curr_ask_px == prev_ask_px:
            ask_ofi = prev_ask_sz - curr_ask_sz
        else:
            ask_ofi = -prev_ask_sz

        ofi_values.append(bid_ofi - ask_ofi)

    return pd.Series(
        ofi_values, 
        index=df.index, 
        name="best_level_ofi"
    )


def compute_multi_level_ofi(
        df: pd.DataFrame, 
        levels: int = 10
    ) -> pd.DataFrame:
    """
    Compute Multi-Level OFI for all levels from 0 to (levels-1).

    Args:
        - df (pd.DataFrame): DataFrame with order book data. Should contain bid_px_0{level}, ask_px_0{level}, bid_sz_0{level}, ask_sz_0{level} columns.
        - levels (int): Number of levels to compute OFI for. Default is 10.
    
    Returns:
        - pd.Series: A DataFrame with OFI values for each level (one per row, same length as df)
    """

    multi_level_ofi = {}
    for lvl in range(levels):
        bid_px_col = f"bid_px_0{lvl}"
        ask_px_col = f"ask_px_0{lvl}"
        bid_sz_col = f"bid_sz_0{lvl}"
        ask_sz_col = f"ask_sz_0{lvl}"

        ofi = [0]
        for i in range(1, len(df)):
            prev_bid_px = df.loc[i-1, bid_px_col]
            prev_ask_px = df.loc[i-1, ask_px_col]
            prev_bid_sz = df.loc[i-1, bid_sz_col]
            prev_ask_sz = df.loc[i-1, ask_sz_col]

            curr_bid_px = df.loc[i, bid_px_col]
            curr_ask_px = df.loc[i, ask_px_col]
            curr_bid_sz = df.loc[i, bid_sz_col]
            curr_ask_sz = df.loc[i, ask_sz_col]

            # ----------- Compute Bid-side OFI (buy orders) ------------
            if curr_bid_px > prev_bid_px:
                bid_ofi = curr_bid_sz
            elif curr_bid_px == prev_bid_px:
                bid_ofi = curr_bid_sz - prev_bid_sz
            else:
                bid_ofi = -prev_bid_sz

            # ----------- Compute Ask-side OFI (sell orders) ------------ 
            if curr_ask_px < prev_ask_px:
                ask_ofi = -curr_ask_sz
            elif curr_ask_px == prev_ask_px:
                ask_ofi = prev_ask_sz - curr_ask_sz
            else:
                ask_ofi = -prev_ask_sz

            ofi.append(bid_ofi - ask_ofi)
        
        multi_level_ofi[f"ofi_level_{lvl}"] = ofi

    return pd.DataFrame(multi_level_ofi, index=df.index)