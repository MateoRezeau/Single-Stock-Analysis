# Single Stock Analysis

## Project Overview
This project implements an Automated Fundamental Analysis engine that transforms raw market data into structured, institutional-grade financial reports. Instead of manually parsing filings, the algorithm utilizes the yfinance API to extract and reformat Income Statements, Balance Sheets, and Cash Flow statements into a standardized terminal-based dashboard.

## Technical Features
- **Data Engine:** Integrated with `yfinance` to extract real-time and historical Income Statements, Balance Sheets, and Cash Flow data.
- **Analytical Framework:** Implement vertical common-size analysis and a comprehensive 30-point ratio suite (profitability, efficiency, liquidity, and solvency).
- **Mathematical Accuracy:** Utilizes rolling averages for Balance Sheet line items to properly calculate turnover and return metrics (e.g., ROE, ROA) against period-end flows).
- **UX & Reporting:** Features a color-coded terminal interface using `colorama` and `tabulate` for institutional-grade readability and standardized reporting.

## Analysis of LVMH as of 15/04/2026

                               FINANCIAL STATEMENT ANALYZER

══════════════════════════════════════════════════════════════════════════════════════════
  LVMH Moët Hennessy - Louis Vuitton, Société Européenne  (MC.PA)
  Consumer Cyclical  ·  Luxury Goods  ·  PAR  ·  EUR
══════════════════════════════════════════════════════════════════════════════════════════

══════════════════════════════════════════════════════════════════════════════════════════
  ███  2 · GENERAL INFORMATION & MARKET RATIOS  ███
══════════════════════════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Price & Valuation
──────────────────────────────────────────────────────────────────────────────────────────
  Current Price                                  481.90 €
  Market Capitalisation                          239.0€B
  Enterprise Value                               263.7€B
  Shares Outstanding                             494€M
  Float Shares                                   245€M
  Beta (5Y monthly)                              0.90

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Earnings Per Share
──────────────────────────────────────────────────────────────────────────────────────────
  EPS (TTM)                                      21.86 €
  EPS (Forward)                                  26.18 €

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Price Multiples (Comparable Ratios)
──────────────────────────────────────────────────────────────────────────────────────────
  P/E (TTM)                                      22.04x
  P/E (Forward)                                  18.41x
  P/B  (Price / Book)                            3.55x
  P/S  (Price / Sales)                           2.96x
  EV / Revenue                                   3.26x
  EV / EBITDA                                    12.81x
  PEG Ratio                                      N/A

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Dividends & Returns
──────────────────────────────────────────────────────────────────────────────────────────
  Dividend Yield                                +270.0%
  Dividend Rate (annual)                         13.00 €
  Payout Ratio                                  +59.5%
  Return on Equity (ROE)                        +16.2%
  Return on Assets (ROA)                        +7.6%

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Growth & Margins (trailing, from yfinance info)
──────────────────────────────────────────────────────────────────────────────────────────
  Revenue Growth (YoY)                          -4.7%
  Earnings Growth (YoY)                         -1.4%
  Gross Margin                                  +66.2%
  Operating Margin                              +21.2%
  Net Profit Margin                             +13.5%
  EBITDA Margin                                 +25.5%

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Liquidity & Leverage (from yfinance info)
──────────────────────────────────────────────────────────────────────────────────────────
  Current Ratio                                 1.58x
  Quick Ratio                                   0.69x
  Debt / Equity                                 0.53x
  Total Cash                                    13.5€B
  Total Debt                                    36.8€B

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Analyst Consensus
──────────────────────────────────────────────────────────────────────────────────────────
  Recommendation                                BUY
  # of Analyst Opinions                         27
  Target Price (Low)                            434.60 €
  Target Price (Mean)                           606.54 €
  Target Price (High)                           825.00 €

══════════════════════════════════════════════════════════════════════════════════════════
  ███  3 · FINANCIAL STATEMENTS  (LAST 3 YEARS)  ███
══════════════════════════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Income Statement  (in €M)
──────────────────────────────────────────────────────────────────────────────────────────
  LINE ITEM                                  2025-12-31        2024-12-31        2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────
    REVENUE                                    80807.0€M     84682.0€M     86153.0€M
        Cost of Goods Sold                     27279.0€M     27918.0€M     26876.0€M
    GROSS PROFIT                               53528.0€M     56764.0€M     59277.0€M
        R&D Expenses                           N/A           N/A           N/A
        SG&A Expenses                          N/A           N/A           N/A
        Other Operating Exp.                   12.0€M        N/A           14.0€M
        Total Operating Expense                35860.0€M     37187.0€M     36496.0€M
    EBIT (Operating Income)                    25965.0€M     27593.0€M     30139.0€M
        D&A                                    8001.0€M      7796.0€M      7177.0€M
    EBITDA                                     25965.0€M     27593.0€M     30139.0€M
        Interest Expense                       1151.0€M      1186.0€M      973.0€M
        Interest Income                       -951.0€M      -1003.0€M     -804.0€M
        Other Income/Expense                   N/A           N/A           N/A
    PRE-TAX INCOME                             16698.0€M     18112.0€M     21626.0€M
        Tax Provision                          5476.0€M      5157.0€M      5673.0€M
    NET INCOME                                 10878.0€M     12550.0€M     15174.0€M

  ─── Per Share ───
        EPS (Basic)                            N/A           0.0€M         0.0€M
        EPS (Diluted)                          N/A           0.0€M         0.0€M
        Shares Outstanding (M)                 N/A           499.4€M       500.1€M
        Diluted Shares (M)                     N/A           499.7€M       500.3€M

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Balance Sheet  (in €M)
──────────────────────────────────────────────────────────────────────────────────────────
  LINE ITEM                                    2025-12-31    2024-12-31    2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────

  ── ASSETS ──────────────────

  CURRENT ASSETS
        Cash & Equivalents                     8794.0€M      9631.0€M      7774.0€M
        Short-Term Investments                 4708.0€M      3956.0€M      3490.0€M
        Receivables                            745.0€M       1031.0€M      850.0€M
        Inventory                              22659.0€M     23669.0€M     22952.0€M
        Other Current Assets                  -1.0€M        -1.0€M         N/A
    TOTAL CURRENT ASSETS                       93858.0€M     101719.0€M    99984.0€M

  NON-CURRENT ASSETS
        Net PP&E                               44018.0€M     46506.0€M     42695.0€M
        Goodwill                               41702.0€M     46587.0€M     49610.0€M
        Intangible Assets                      41702.0€M     46587.0€M     49610.0€M
        Long-Term Investments                  1214.0€M      1343.0€M      991.0€M
        Other Non-Current Assets               128.0€M       128.0€M       99.0€M
    TOTAL ASSETS                               142037.0€M    149190.0€M    143694.0€M

  ── LIABILITIES ────────────

  CURRENT LIABILITIES
        Accounts Payable                       8223.0€M      8630.0€M      9049.0€M
        Short-Term Debt                        10928.0€M     14252.0€M     13839.0€M
        Other Current Liabilities              1910.0€M      1978.0€M      1880.0€M
    TOTAL CURRENT LIABILITIES                  42672.0€M     46207.0€M     47848.0€M

  NON-CURRENT LIABILITIES
        Long-Term Debt                         25803.0€M     26951.0€M     25037.0€M
        Deferred Tax Liabilities               N/A           N/A           N/A
        Other Non-Current Liab.                6852.0€M      8698.0€M      12570.0€M
    TOTAL LIABILITIES                          73088.0€M     79903.0€M     80993.0€M

  ── EQUITY ─────────────────
        Common Stock                           67472.0€M     67517.0€M     61017.0€M
        Retained Earnings                      10878.0€M     12550.0€M     15174.0€M
        Other Equity Adj.                      N/A           N/A           N/A
    SHAREHOLDERS' EQUITY                       67472.0€M     67517.0€M     61017.0€M
        Minority Interest                      68949.0€M     69287.0€M     62701.0€M
    TOTAL LIABILITIES + EQUITY                 68949.0€M     69287.0€M     62701.0€M

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Statement of Cash Flows  (in €M)
──────────────────────────────────────────────────────────────────────────────────────────
  LINE ITEM                                    2025-12-31    2024-12-31    2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────

  ── OPERATING ACTIVITIES ────────
        Net Income                             17099.0€M     18907.0€M     22560.0€M
        D&A                                    N/A           N/A           N/A
        Stock-Based Compensation               N/A           N/A           N/A
        Changes in Working Capital             N/A           N/A           N/A
        Other Operating Items                -172.0€M        488.0€M      -259.0€M
    CASH FROM OPERATIONS (CFO)                 18875.0€M     18925.0€M     18403.0€M

  ── INVESTING ACTIVITIES ────────
        Capital Expenditures (CapEx)          -4670.0€M     -5552.0€M     -7807.0€M
        Acquisitions                           149.0€M      -438.0€M      -721.0€M
        Purchase of Investments                N/A           N/A           N/A
        Sale of Investments                    N/A           N/A           N/A
        Other Investing Activities             N/A           N/A           N/A
    CASH FROM INVESTING (CFI)                 -4640.0€M     -6539.0€M     -8310.0€M

  ── FINANCING ACTIVITIES ────────
        Debt / Stock Issuance                 -1640.0€M     -259.0€M      -1584.0€M
        Debt Repayment                        -4228.0€M     -3676.0€M     -3968.0€M
        Dividends Paid                        -6465.0€M     -6492.0€M     -6251.0€M
        Share Buybacks                        -1640.0€M     -312.0€M      -1584.0€M
        Other Financing Activities             N/A           N/A           N/A
    CASH FROM FINANCING (CFF)                 -14896.0€M    -10716.0€M    -9397.0€M

  ── NET CHANGE ──────────────────
        FX Effect on Cash                     -248.0€M       80.0€M       -273.0€M
    NET CHANGE IN CASH                        -661.0€M       1670.0€M      696.0€M
        Beginning Cash                         9269.0€M      7520.0€M      7100.0€M
        Ending Cash                            8359.0€M      9269.0€M      7520.0€M
    FREE CASH FLOW (FCF)                       14205.0€M     13373.0€M     10596.0€M

══════════════════════════════════════════════════════════════════════════════════════════
  ███  4 · COMMON-SIZE FINANCIAL STATEMENTS  (% OF BASE)  ███
══════════════════════════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Income Statement  (all items as % of Total Revenue)
──────────────────────────────────────────────────────────────────────────────────────────
  LINE ITEM                                    2025-12-31    2024-12-31    2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────
  Total Revenue                               +100.0%       +100.0%       +100.0%
  Cost Of Revenue                             +33.8%        +33.0%        +31.2%
  Gross Profit                                +66.2%        +67.0%        +68.8%
  EBIT                                        +32.1%        +32.6%        +35.0%
  EBITDA                                      +32.1%        +32.6%        +35.0%
  Pretax Income                               +20.7%        +21.4%        +25.1%
  Tax Provision                               +6.8%         +6.1%         +6.6%
  Net Income                                  +13.5%        +14.8%        +17.6%

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Balance Sheet  (all items as % of Total Assets)
──────────────────────────────────────────────────────────────────────────────────────────
  LINE ITEM                                    2025-12-31    2024-12-31    2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────
  Cash And Cash Equivalents                    +6.2%        +6.5%         +5.4%
  Receivables                                  +0.5%        +0.7%         +0.6%
  Inventory                                    +16.0%       +15.9%        +16.0%
  Current Assets                               +66.1%       +68.2%        +69.6%
  Net PPE                                      +31.0%       +31.2%        +29.7%
  Goodwill                                     +29.4%       +31.2%        +34.5%
  Total Assets                                 +100.0%      +100.0%       +100.0%
  Current Liabilities                          +30.0%       +31.0%        +33.3%
  Long Term Debt                               +18.2%       +18.1%        +17.4%
  Total Liabilities Net Minority Interest      +51.5%       +53.6%        +56.4%
  Stockholders Equity                          +47.5%       +45.3%        +42.5%

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Cash Flow Statement  (items as % of Operating Cash Flow)
──────────────────────────────────────────────────────────────────────────────────────────
  LINE ITEM                                     2025-12-31   2024-12-31    2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────
  Net Income                                   +90.6%       +99.9%        +122.6%
  Operating Cash Flow                          +100.0%      +100.0%       +100.0%
  Capital Expenditure                          -24.7%       -29.3%        -42.4%
  Investing Cash Flow                          -24.6%       -34.6%        -45.2%
  Financing Cash Flow                          -78.9%       -56.6%        -51.1%
  Free Cash Flow                               +75.3%       +70.7%        +57.6%

══════════════════════════════════════════════════════════════════════════════════════════
  ███  5 · CALCULATED FINANCIAL RATIOS  ███
══════════════════════════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Profitability Ratios
──────────────────────────────────────────────────────────────────────────────────────────
  RATIO                                         2025-12-31   2024-12-31    2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────
  Gross Margin                                 +66.2%       +67.0%        +68.8%
  EBIT Margin                                  +32.1%       +32.6%        +35.0%
  EBITDA Margin                                +32.1%       +32.6%        +35.0%
  Net Profit Margin                            +13.5%       +14.8%        +17.6%
  Return on Assets (ROA)                       +7.7%        +8.4%         +10.6%
  Return on Equity (ROE)                       +16.1%       +18.6%        +23.6%
  Return on Capital Emp.                       +27.8%       +29.2%        +35.0%
  Effective Tax Rate                           +32.8%       +28.5%        +26.2%

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Efficiency / Activity Ratios
──────────────────────────────────────────────────────────────────────────────────────────
  RATIO                                         2025-12-31   2024-12-31    2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────
  Asset Turnover                                0.57x        0.58x         0.59x
  Receivables Turnover                          108.47x      95.36x        91.60x
  Days Sales Outstanding                        3.4d         3.8d          4.0d
  Inventory Turnover                            1.20x        1.21x         1.15x
  Days Inventory Outstanding                    303.2d       302.8d        316.6d

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Liquidity Ratios
──────────────────────────────────────────────────────────────────────────────────────────
  RATIO                                         2025-12-31   2024-12-31    2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────
  Current Ratio                                 2.20x        2.20x         2.09x
  Quick Ratio                                   1.67x        1.69x         1.61x
  Cash Ratio                                    0.21x        0.21x         0.16x

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Leverage / Solvency Ratios
──────────────────────────────────────────────────────────────────────────────────────────
  RATIO                                         2025-12-31   2024-12-31    2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────
  Debt / Equity                                 0.54x        0.61x         0.64x
  Debt / EBITDA                                 1.41x        1.49x         1.29x
  Net Debt / EBITDA                             1.08x        1.14x         1.03x
  Equity Multiplier                             2.11x        2.21x         2.35x
  Interest Coverage                             22.56x       23.27x        30.98x
  Debt Ratio                                    0.51x        0.54x         0.56x

──────────────────────────────────────────────────────────────────────────────────────────
  ▸  Cash Flow Quality Ratios
──────────────────────────────────────────────────────────────────────────────────────────
  RATIO                                         2025-12-31   2024-12-31    2023-12-31
──────────────────────────────────────────────────────────────────────────────────────────
  CFO / Net Income                              1.74x        1.51x         1.21x
  FCF / Net Income                              1.31x        1.07x         0.70x
  FCF / Revenue                                +17.6%       +15.8%        +12.3%
  CapEx / CFO                                  +24.7%       +29.3%        +42.4%
  CapEx / Revenue                              +5.8%        +6.6%         +9.1%

══════════════════════════════════════════════════════════════════════════════════════════

## Installation & Usage
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO`
2. Install dependencies: `pip install yfinance pandas numpy tabulate colorama`
3. Update ticker to analyze the company of your choice: `DEFAULT_TICKER = "TICKER OF YOUR CHOICE"` Script line 33
4. Run the analysis: `python main.py`
