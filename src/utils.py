import pandas as pd
import matplotlib.pyplot as plt


def plot_best_level_ofi(df: pd.DataFrame):
    df["ts_event"] = pd.to_datetime(df["ts_event"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["ts_event"], df["best_level_ofi"], label="Best-Level OFI", color='blue')

    plt.title("Best-Level Order Flow Imbalance (OFI) Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("OFI Value")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("output/best_level_ofi_plot.png")
    plt.close()


def plot_multi_level_ofi_subplots(df, levels=10):
    """
    Plot each OFI level in its own subplot for clean visual comparison.
    """
    df["ts_event"] = pd.to_datetime(df["ts_event"])
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(16, 12), sharex=True)
    axes = axes.flatten()

    for lvl in range(levels):
        col = f"ofi_level_{lvl}"
        axes[lvl].plot(df["ts_event"], df[col], label=col, color='tab:blue', linewidth=1)
        axes[lvl].set_title(f"OFI Level {lvl}")
        axes[lvl].axhline(0, color='black', linestyle='--', linewidth=0.7)
        axes[lvl].grid(True)

    plt.suptitle("Multi-Level Order Flow Imbalance (Each Level Separate)", fontsize=16)
    plt.xlabel("Time")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("output/multi_level_ofi_subplots.png")
    plt.close()