# Single Stock Analysis

## Project Overview
This project implements an Automated Fundamental Analysis engine that transforms raw market data into structured, institutional-grade financial reports. Instead of manually parsing filings, the algorithm utilizes the yfinance API to extract and reformat Income Statements, Balance Sheets, and Cash Flow statements into a standardized terminal-based dashboard.

## Technical Features
- **Data Engine:** Integrated with `yfinance` to extract real-time and historical Income Statements, Balance Sheets, and Cash Flow data.
- **Analytical Framework:** Implement vertical common-size analysis and a comprehensive 30-point ratio suite (profitability, efficiency, liquidity, and solvency).
- **Mathematical Accuracy:** Utilizes rolling averages for Balance Sheet line items to properly calculate turnover and return metrics (e.g., ROE, ROA) against period-end flows).
- **UX & Reporting:** Features a color-coded terminal interface using `colorama` and `tabulate` for institutional-grade readability and standardized reporting.

## Installation & Usage
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO`
2. Install dependencies: `pip install yfinance pandas numpy tabulate colorama`
3. Update ticker to analyze the company of your choice: `DEFAULT_TICKER = "TICKER OF YOUR CHOICE"` Script line 33
4. Run the analysis: `python main.py`
5. See `single_stock_analysis_output_RMS.PA.txt` for output example
