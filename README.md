# Order Flow Imbalance (OFI) Feature Construction - Blockhouse Task 1

This project implements Order Flow Imbalance (OFI) feature engineering across Best-Level, Multi-Level, and Integrated (PCA-based) definitions, inspired by the research paper *\"Cross-Impact of Order Flow Imbalance in Equity Markets\"*. The solution includes both a CLI-based feature pipeline and an interactive Streamlit dashboard with explainability.

---

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Usage

You can run the project in two modes:

### CLI Mode

Processes the dataset and saves OFI features and plots to the `output/` folder.

```bash
python main.py --mode cli
```

### Streamlit Dashboard

Launches an interactive dashboard with sliders to explore OFI types, depth, and smoothing. Includes PCA-based explainability for Integrated OFI.

```bash
python main.py --mode streamlit
```

---

## Folder Structure

```
.
├── data/                    # Contains the task proviided CSV file (first_25000_rows.csv)
├── output/                  # Generated plots and CSVs (CLI mode)
├── src/
│   ├── ofi_features.py      # OFI computation logic
│   ├── utils.py             # Plotting utilities
│   └── streamlit_app.py     # Streamlit app logic
├── main.py                  # Entry point (CLI / dashboard)
└── requirements.txt
```

---

## Notes

- The dataset contains only a single instrument, so cross-asset OFI estimation (as in the original paper) is not feasible here. However, if provided with other ticker's data, it will be possible to have cross-asset OFI estimation

---

Contact: sarangshivam99@gmail.com
