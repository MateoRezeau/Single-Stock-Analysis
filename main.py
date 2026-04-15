"""
╔══════════════════════════════════════════════════════════════════╗
║          COMPREHENSIVE FINANCIAL STATEMENT ANALYZER              ║
║                  Powered by yfinance                             ║
╚══════════════════════════════════════════════════════════════════╝

Usage:
    python financial_analysis.py
    python financial_analysis.py --ticker RMS.PA
    python financial_analysis.py --ticker AAPL --years 4

Requirements:
    pip install yfinance pandas numpy tabulate colorama
"""

import argparse
import sys
import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
import pandas as pd
import numpy as np
from tabulate import tabulate
from colorama import init, Fore, Back, Style

init(autoreset=True)

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────

DEFAULT_TICKER = "MC.PA"   # Hermès International
DEFAULT_YEARS  = 3
CURRENCY_SYMBOL = "€"       # Change to "$" for US stocks

# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

DIVIDER      = Fore.CYAN  + "─" * 90 + Style.RESET_ALL
THICK_DIV    = Fore.CYAN  + "═" * 90 + Style.RESET_ALL
SECTION_COL  = Fore.CYAN  + Style.BRIGHT
HEADER_COL   = Fore.WHITE + Style.BRIGHT
VALUE_COL    = Fore.WHITE
POS_COL      = Fore.GREEN
NEG_COL      = Fore.RED
LABEL_COL    = Fore.YELLOW
DIM_COL      = Fore.WHITE + Style.DIM
RESET        = Style.RESET_ALL


def fmt_num(value, unit="M", decimals=1):
    """Format a raw number into a human-readable financial figure."""
    if pd.isna(value) or value is None:
        return DIM_COL + "  N/A" + RESET
    divisor = {"M": 1e6, "B": 1e9, "K": 1e3}.get(unit, 1)
    formatted = f"{value / divisor:>{10}.{decimals}f}{CURRENCY_SYMBOL}{unit}"
    color = POS_COL if value >= 0 else NEG_COL
    return color + formatted + RESET


def fmt_pct(value, decimals=1):
    """Format a ratio as a percentage string."""
    if pd.isna(value) or value is None:
        return DIM_COL + "     N/A" + RESET
    color = POS_COL if value >= 0 else NEG_COL
    return color + f"{value * 100:>+8.{decimals}f}%" + RESET


def fmt_ratio(value, decimals=2):
    """Format a plain ratio."""
    if pd.isna(value) or value is None:
        return DIM_COL + "     N/A" + RESET
    return VALUE_COL + f"{value:>8.{decimals}f}x" + RESET


def safe_get(series, key, default=np.nan):
    """Safely retrieve a value from a pandas Series by partial key match."""
    if series is None or series.empty:
        return default
    matches = [k for k in series.index if key.lower() in str(k).lower()]
    if matches:
        val = series[matches[0]]
        return val if not (isinstance(val, float) and np.isnan(val)) else default
    return default


def section_header(title):
    print()
    print(THICK_DIV)
    print(SECTION_COL + f"  {'█'*3}  {title.upper()}  {'█'*3}" + RESET)
    print(THICK_DIV)


def sub_header(title):
    print()
    print(DIVIDER)
    print(HEADER_COL + f"  ▸  {title}" + RESET)
    print(DIVIDER)


def kv_row(label, value, width=40):
    """Print a key-value pair in a consistent layout."""
    print(f"  {LABEL_COL}{label:<{width}}{RESET}  {value}")


# ─────────────────────────────────────────────
#  DATA FETCHING
# ─────────────────────────────────────────────

def fetch_data(ticker_symbol: str):
    """Fetch all required data from yfinance."""
    print(f"\n{DIM_COL}  Fetching data for {ticker_symbol} …{RESET}")
    ticker = yf.Ticker(ticker_symbol)

    info           = ticker.info or {}
    income_stmt    = ticker.financials          # annual
    balance_sheet  = ticker.balance_sheet       # annual
    cash_flow      = ticker.cashflow            # annual
    quarterly_inc  = ticker.quarterly_financials

    # Limit columns to requested years
    def trim(df, years):
        if df is None or df.empty:
            return df
        return df.iloc[:, :years]

    return {
        "info":         info,
        "income":       trim(income_stmt,   DEFAULT_YEARS),
        "balance":      trim(balance_sheet, DEFAULT_YEARS),
        "cashflow":     trim(cash_flow,     DEFAULT_YEARS),
        "q_income":     quarterly_inc,
        "ticker_obj":   ticker,
    }


# ─────────────────────────────────────────────
#  SECTION 1 – TITLE
# ─────────────────────────────────────────────

def print_title(info: dict, ticker_symbol: str):
    name    = info.get("longName") or info.get("shortName") or ticker_symbol
    sector  = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    exchange = info.get("exchange", "N/A")
    currency = info.get("currency", "N/A")

    print()
    print(Back.CYAN + Fore.BLACK + Style.BRIGHT +
          f"{'':^10}{'FINANCIAL STATEMENT ANALYZER':^70}{'':^10}" + RESET)
    print()
    print(THICK_DIV)
    print(HEADER_COL + f"  {name}  ({ticker_symbol})" + RESET)
    print(DIM_COL   + f"  {sector}  ·  {industry}  ·  {exchange}  ·  {currency}" + RESET)
    print(THICK_DIV)


# ─────────────────────────────────────────────
#  SECTION 2 – GENERAL INFO & MARKET RATIOS
# ─────────────────────────────────────────────

def print_general_info(info: dict):
    section_header("2 · General Information & Market Ratios")

    def g(key, default=np.nan):
        return info.get(key, default)

    # ── Price & Valuation ──
    sub_header("Price & Valuation")

    price        = g("currentPrice") or g("regularMarketPrice")
    mkt_cap      = g("marketCap")
    ev           = g("enterpriseValue")
    shares       = g("sharesOutstanding")
    float_shares = g("floatShares")
    beta         = g("beta")

    kv_row("Current Price",           VALUE_COL + f"{price:>10.2f} {CURRENCY_SYMBOL}" + RESET if not pd.isna(price) else DIM_COL + "N/A" + RESET)
    kv_row("Market Capitalisation",   fmt_num(mkt_cap, "B"))
    kv_row("Enterprise Value",        fmt_num(ev, "B"))
    kv_row("Shares Outstanding",      fmt_num(shares, "M", 0))
    kv_row("Float Shares",            fmt_num(float_shares, "M", 0))
    kv_row("Beta (5Y monthly)",       VALUE_COL + f"{beta:>8.2f}" + RESET if not pd.isna(beta) else DIM_COL + "N/A" + RESET)

    # ── Earnings Per Share ──
    sub_header("Earnings Per Share")

    eps_ttm   = g("trailingEps")
    eps_fwd   = g("forwardEps")

    kv_row("EPS (TTM)",               VALUE_COL + f"{eps_ttm:>10.2f} {CURRENCY_SYMBOL}" + RESET if not pd.isna(eps_ttm) else DIM_COL + "N/A" + RESET)
    kv_row("EPS (Forward)",           VALUE_COL + f"{eps_fwd:>10.2f} {CURRENCY_SYMBOL}" + RESET if not pd.isna(eps_fwd) else DIM_COL + "N/A" + RESET)

    # ── Price Multiples ──
    sub_header("Price Multiples (Comparable Ratios)")

    pe_ttm  = g("trailingPE")
    pe_fwd  = g("forwardPE")
    pb      = g("priceToBook")
    ps      = g("priceToSalesTrailing12Months")
    ev_rev  = g("enterpriseToRevenue")
    ev_ebit = g("enterpriseToEbitda")
    peg     = g("pegRatio")

    rows = [
        ("P/E (TTM)",              fmt_ratio(pe_ttm)),
        ("P/E (Forward)",          fmt_ratio(pe_fwd)),
        ("P/B  (Price / Book)",    fmt_ratio(pb)),
        ("P/S  (Price / Sales)",   fmt_ratio(ps)),
        ("EV / Revenue",           fmt_ratio(ev_rev)),
        ("EV / EBITDA",            fmt_ratio(ev_ebit)),
        ("PEG Ratio",              fmt_ratio(peg)),
    ]
    for label, val in rows:
        kv_row(label, val)

    # ── Dividends & Returns ──
    sub_header("Dividends & Returns")

    div_yield  = g("dividendYield")
    div_rate   = g("dividendRate")
    payout     = g("payoutRatio")
    roe        = g("returnOnEquity")
    roa        = g("returnOnAssets")

    kv_row("Dividend Yield",          fmt_pct(div_yield))
    kv_row("Dividend Rate (annual)",  VALUE_COL + f"{div_rate:>10.2f} {CURRENCY_SYMBOL}" + RESET if not pd.isna(div_rate) else DIM_COL + "N/A" + RESET)
    kv_row("Payout Ratio",            fmt_pct(payout))
    kv_row("Return on Equity (ROE)",  fmt_pct(roe))
    kv_row("Return on Assets (ROA)",  fmt_pct(roa))

    # ── Growth & Margins (from yfinance info) ──
    sub_header("Growth & Margins (trailing, from yfinance info)")

    rev_growth    = g("revenueGrowth")
    earn_growth   = g("earningsGrowth")
    gross_margin  = g("grossMargins")
    oper_margin   = g("operatingMargins")
    profit_margin = g("profitMargins")
    ebitda_margin = g("ebitdaMargins")

    kv_row("Revenue Growth (YoY)",    fmt_pct(rev_growth))
    kv_row("Earnings Growth (YoY)",   fmt_pct(earn_growth))
    kv_row("Gross Margin",            fmt_pct(gross_margin))
    kv_row("Operating Margin",        fmt_pct(oper_margin))
    kv_row("Net Profit Margin",       fmt_pct(profit_margin))
    kv_row("EBITDA Margin",           fmt_pct(ebitda_margin))

    # ── Liquidity & Leverage (from yfinance info) ──
    sub_header("Liquidity & Leverage (from yfinance info)")

    current_ratio  = g("currentRatio")
    quick_ratio    = g("quickRatio")
    debt_to_equity = g("debtToEquity")
    total_cash     = g("totalCash")
    total_debt     = g("totalDebt")

    kv_row("Current Ratio",           fmt_ratio(current_ratio))
    kv_row("Quick Ratio",             fmt_ratio(quick_ratio))
    kv_row("Debt / Equity",           fmt_ratio(debt_to_equity / 100 if not pd.isna(debt_to_equity) else np.nan))
    kv_row("Total Cash",              fmt_num(total_cash, "B"))
    kv_row("Total Debt",              fmt_num(total_debt, "B"))

    # ── Analyst Targets ──
    sub_header("Analyst Consensus")

    target_high = g("targetHighPrice")
    target_low  = g("targetLowPrice")
    target_mean = g("targetMeanPrice")
    recommend   = g("recommendationKey", "N/A")
    nb_analysts = g("numberOfAnalystOpinions", "N/A")

    kv_row("Recommendation",          VALUE_COL + str(recommend).upper() + RESET)
    kv_row("# of Analyst Opinions",   VALUE_COL + str(nb_analysts) + RESET)
    kv_row("Target Price (Low)",      VALUE_COL + f"{target_low:>10.2f} {CURRENCY_SYMBOL}" + RESET if not pd.isna(target_low) else DIM_COL + "N/A" + RESET)
    kv_row("Target Price (Mean)",     VALUE_COL + f"{target_mean:>10.2f} {CURRENCY_SYMBOL}" + RESET if not pd.isna(target_mean) else DIM_COL + "N/A" + RESET)
    kv_row("Target Price (High)",     VALUE_COL + f"{target_high:>10.2f} {CURRENCY_SYMBOL}" + RESET if not pd.isna(target_high) else DIM_COL + "N/A" + RESET)


# ─────────────────────────────────────────────
#  HELPERS: Statement Builders
# ─────────────────────────────────────────────

def build_income_statement(df: pd.DataFrame):
    """Extract and rebuild a structured income statement from raw yfinance financials."""
    if df is None or df.empty:
        return None

    def g(key):
        return safe_get(df.iloc[:, 0], key)  # just to test existence

    def row(key):
        matches = [k for k in df.index if key.lower() in str(k).lower()]
        if matches:
            return df.loc[matches[0]]
        return pd.Series([np.nan] * len(df.columns), index=df.columns)

    revenue          = row("Total Revenue")
    cogs             = row("Cost Of Revenue")
    gross_profit     = row("Gross Profit")
    op_expense       = row("Operating Expense")
    rd               = row("Research And Development")
    sga              = row("Selling General Administrative")
    other_op_exp     = row("Other Operating Expenses")
    ebit             = row("EBIT")
    da               = row("Reconciled Depreciation")
    ebitda           = row("EBITDA")
    interest_exp     = row("Interest Expense")
    interest_inc     = row("Interest Income")
    other_income     = row("Other Income Expense")
    pretax_income    = row("Pretax Income")
    tax_provision    = row("Tax Provision")
    net_income       = row("Net Income")
    basic_eps        = row("Basic EPS")
    diluted_eps      = row("Diluted EPS")
    shares_basic     = row("Basic Average Shares")
    shares_diluted   = row("Diluted Average Shares")

    structure = [
        ("REVENUE",                   revenue,        False),
        ("  Cost of Goods Sold",      cogs,           True),
        ("GROSS PROFIT",              gross_profit,   False),
        ("  R&D Expenses",            rd,             True),
        ("  SG&A Expenses",           sga,            True),
        ("  Other Operating Exp.",    other_op_exp,   True),
        ("  Total Operating Expense", op_expense,     True),
        ("EBIT (Operating Income)",   ebit,           False),
        ("  D&A",                     da,             True),
        ("EBITDA",                    ebitda,         False),
        ("  Interest Expense",        interest_exp,   True),
        ("  Interest Income",         interest_inc,   True),
        ("  Other Income/Expense",    other_income,   True),
        ("PRE-TAX INCOME",            pretax_income,  False),
        ("  Tax Provision",           tax_provision,  True),
        ("NET INCOME",                net_income,     False),
        ("─── Per Share ───",         None,           False),
        ("  EPS (Basic)",             basic_eps,      True),
        ("  EPS (Diluted)",           diluted_eps,    True),
        ("  Shares Outstanding (M)",  shares_basic,   True),
        ("  Diluted Shares (M)",      shares_diluted, True),
    ]
    return structure, df.columns.tolist()


def build_balance_sheet(df: pd.DataFrame):
    """Extract and rebuild a structured balance sheet."""
    if df is None or df.empty:
        return None

    def row(key):
        matches = [k for k in df.index if key.lower() in str(k).lower()]
        if matches:
            return df.loc[matches[0]]
        return pd.Series([np.nan] * len(df.columns), index=df.columns)

    cash                    = row("Cash And Cash Equivalents")
    short_investments       = row("Other Short Term Investments")
    receivables             = row("Receivables")
    inventory               = row("Inventory")
    other_current           = row("Other Current Assets")
    current_assets          = row("Current Assets")
    ppe_net                 = row("Net PPE")
    goodwill                = row("Goodwill")
    intangibles             = row("Other Intangible Assets")
    long_investments        = row("Long Term Equity Investment")
    other_non_current       = row("Other Non Current Assets")
    total_assets            = row("Total Assets")

    accounts_payable        = row("Accounts Payable")
    short_debt              = row("Current Debt")
    other_current_liab      = row("Other Current Liabilities")
    current_liab            = row("Current Liabilities")
    long_debt               = row("Long Term Debt")
    deferred_tax            = row("Deferred Tax Liabilities Net")
    other_non_cur_liab      = row("Other Non Current Liabilities")
    total_liab              = row("Total Liabilities Net Minority Interest")

    common_stock            = row("Common Stock")
    retained_earnings       = row("Retained Earnings")
    other_equity            = row("Other Equity Adjustments")
    stockholder_equity      = row("Stockholders Equity")
    total_equity_liab       = row("Total Equity Gross Minority Interest")
    minority_interest       = row("Minority Interest")

    structure = [
        ("── ASSETS ──────────────────", None,               False),
        ("CURRENT ASSETS",              None,               False),
        ("  Cash & Equivalents",        cash,               True),
        ("  Short-Term Investments",    short_investments,  True),
        ("  Receivables",               receivables,        True),
        ("  Inventory",                 inventory,          True),
        ("  Other Current Assets",      other_current,      True),
        ("TOTAL CURRENT ASSETS",        current_assets,     False),
        ("NON-CURRENT ASSETS",          None,               False),
        ("  Net PP&E",                  ppe_net,            True),
        ("  Goodwill",                  goodwill,           True),
        ("  Intangible Assets",         intangibles,        True),
        ("  Long-Term Investments",     long_investments,   True),
        ("  Other Non-Current Assets",  other_non_current,  True),
        ("TOTAL ASSETS",                total_assets,       False),
        ("── LIABILITIES ────────────", None,               False),
        ("CURRENT LIABILITIES",         None,               False),
        ("  Accounts Payable",          accounts_payable,   True),
        ("  Short-Term Debt",           short_debt,         True),
        ("  Other Current Liabilities", other_current_liab, True),
        ("TOTAL CURRENT LIABILITIES",   current_liab,       False),
        ("NON-CURRENT LIABILITIES",     None,               False),
        ("  Long-Term Debt",            long_debt,          True),
        ("  Deferred Tax Liabilities",  deferred_tax,       True),
        ("  Other Non-Current Liab.",   other_non_cur_liab, True),
        ("TOTAL LIABILITIES",           total_liab,         False),
        ("── EQUITY ─────────────────", None,               False),
        ("  Common Stock",              common_stock,       True),
        ("  Retained Earnings",         retained_earnings,  True),
        ("  Other Equity Adj.",         other_equity,       True),
        ("SHAREHOLDERS' EQUITY",        stockholder_equity, False),
        ("  Minority Interest",         minority_interest,  True),
        ("TOTAL LIABILITIES + EQUITY",  total_equity_liab,  False),
    ]
    return structure, df.columns.tolist()


def build_cash_flow(df: pd.DataFrame):
    """Extract and rebuild a structured statement of cash flows."""
    if df is None or df.empty:
        return None

    def row(key):
        matches = [k for k in df.index if key.lower() in str(k).lower()]
        if matches:
            return df.loc[matches[0]]
        return pd.Series([np.nan] * len(df.columns), index=df.columns)

    net_income              = row("Net Income")
    da                      = row("Depreciation Amortization Depletion")
    sbc                     = row("Stock Based Compensation")
    wc_changes              = row("Changes In Working Capital")
    other_op                = row("Other Non Cash Items")
    cfo                     = row("Operating Cash Flow")

    capex                   = row("Capital Expenditure")
    acquisitions            = row("Net Business Purchase And Sale")
    investments_purchase    = row("Purchase Of Investment")
    investments_sale        = row("Sale Of Investment")
    other_inv               = row("Other Investing Activities")
    cfi                     = row("Investing Cash Flow")

    debt_issuance           = row("Common Stock Issuance")
    debt_repayment          = row("Repayment Of Debt")
    dividends               = row("Cash Dividends Paid")
    buybacks                = row("Repurchase Of Capital Stock")
    other_fin               = row("Other Financing Activities")
    cff                     = row("Financing Cash Flow")

    fx_effect               = row("Effect Of Exchange Rate Changes")
    net_change              = row("Changes In Cash")
    begin_cash              = row("Beginning Cash Position")
    end_cash                = row("End Cash Position")
    fcf                     = row("Free Cash Flow")

    structure = [
        ("── OPERATING ACTIVITIES ────────", None,               False),
        ("  Net Income",                    net_income,          True),
        ("  D&A",                           da,                  True),
        ("  Stock-Based Compensation",      sbc,                 True),
        ("  Changes in Working Capital",    wc_changes,          True),
        ("  Other Operating Items",         other_op,            True),
        ("CASH FROM OPERATIONS (CFO)",      cfo,                 False),
        ("── INVESTING ACTIVITIES ────────", None,               False),
        ("  Capital Expenditures (CapEx)",  capex,               True),
        ("  Acquisitions",                  acquisitions,        True),
        ("  Purchase of Investments",       investments_purchase,True),
        ("  Sale of Investments",           investments_sale,    True),
        ("  Other Investing Activities",    other_inv,           True),
        ("CASH FROM INVESTING (CFI)",       cfi,                 False),
        ("── FINANCING ACTIVITIES ────────", None,               False),
        ("  Debt / Stock Issuance",         debt_issuance,       True),
        ("  Debt Repayment",                debt_repayment,      True),
        ("  Dividends Paid",                dividends,           True),
        ("  Share Buybacks",                buybacks,            True),
        ("  Other Financing Activities",    other_fin,           True),
        ("CASH FROM FINANCING (CFF)",       cff,                 False),
        ("── NET CHANGE ──────────────────", None,               False),
        ("  FX Effect on Cash",             fx_effect,           True),
        ("NET CHANGE IN CASH",              net_change,          False),
        ("  Beginning Cash",                begin_cash,          True),
        ("  Ending Cash",                   end_cash,            True),
        ("FREE CASH FLOW (FCF)",            fcf,                 False),
    ]
    return structure, df.columns.tolist()


# ─────────────────────────────────────────────
#  GENERIC STATEMENT PRINTER
# ─────────────────────────────────────────────

def print_statement(structure, columns, title, unit="M", decimals=0):
    """Print a structured financial statement to the console."""
    sub_header(title + f"  (in {CURRENCY_SYMBOL}{unit})")

    col_width = 18
    header = f"  {'LINE ITEM':<42}" + "".join(
        HEADER_COL + f"{str(c.date() if hasattr(c,'date') else c):>{col_width}}" + RESET
        for c in columns
    )
    print(header)
    print(DIVIDER)

    for label, series, is_sub in structure:
        if series is None:
            # Section separator / title row
            print(f"\n  {LABEL_COL + Style.BRIGHT}{label}{RESET}")
            continue

        values_str = ""
        for col in columns:
            try:
                val = series[col]
                values_str += fmt_num(val, unit=unit, decimals=decimals).rjust(col_width + len(fmt_num(0, unit=unit, decimals=decimals)) - len(fmt_num(0, unit=unit, decimals=decimals).strip()))
                values_str += "  "
            except Exception:
                values_str += DIM_COL + f"{'N/A':>{col_width}}" + RESET + "  "

        # Color sub-items dimmer
        label_color = DIM_COL if is_sub else HEADER_COL + Style.BRIGHT
        indent      = "    " if is_sub else "  "
        print(f"  {label_color}{indent}{label:<40}{RESET}{values_str}")


# ─────────────────────────────────────────────
#  SECTION 3 – FINANCIAL STATEMENTS
# ─────────────────────────────────────────────

def print_financial_statements(data: dict):
    section_header("3 · Financial Statements  (last 3 years)")

    # Income Statement
    result = build_income_statement(data["income"])
    if result:
        structure, columns = result
        print_statement(structure, columns, "Income Statement", unit="M", decimals=1)
    else:
        print(f"\n  {NEG_COL}Income statement data not available.{RESET}")

    # Balance Sheet
    result = build_balance_sheet(data["balance"])
    if result:
        structure, columns = result
        print_statement(structure, columns, "Balance Sheet", unit="M", decimals=1)
    else:
        print(f"\n  {NEG_COL}Balance sheet data not available.{RESET}")

    # Cash Flow
    result = build_cash_flow(data["cashflow"])
    if result:
        structure, columns = result
        print_statement(structure, columns, "Statement of Cash Flows", unit="M", decimals=1)
    else:
        print(f"\n  {NEG_COL}Cash flow data not available.{RESET}")


# ─────────────────────────────────────────────
#  SECTION 4 – COMMON SIZE STATEMENTS
# ─────────────────────────────────────────────

def print_common_size(data: dict):
    section_header("4 · Common-Size Financial Statements  (% of base)")

    def pct_fmt(val, base_val):
        if pd.isna(val) or pd.isna(base_val) or base_val == 0:
            return DIM_COL + "     N/A" + RESET
        pct = val / abs(base_val) * 100
        color = POS_COL if pct >= 0 else NEG_COL
        return color + f"{pct:>+8.1f}%" + RESET

    col_width = 12

    # ── INCOME STATEMENT: % of Revenue ──
    sub_header("Income Statement  (all items as % of Total Revenue)")
    inc = data["income"]
    if inc is not None and not inc.empty:
        columns = inc.columns.tolist()
        rev_row = [k for k in inc.index if "total revenue" in str(k).lower()]
        if not rev_row:
            print(f"  {NEG_COL}Revenue row not found.{RESET}")
        else:
            revenue = inc.loc[rev_row[0]]
            header = f"  {'LINE ITEM':<42}" + "".join(
                HEADER_COL + f"{str(c.date() if hasattr(c,'date') else c):>{col_width}}" + RESET
                for c in columns
            )
            print(header)
            print(DIVIDER)
            items_to_show = [
                "Total Revenue",
                "Cost Of Revenue",
                "Gross Profit",
                "EBIT",
                "EBITDA",
                "Pretax Income",
                "Tax Provision",
                "Net Income",
            ]
            for item in items_to_show:
                matches = [k for k in inc.index if item.lower() in str(k).lower()]
                if not matches:
                    continue
                series = inc.loc[matches[0]]
                vals   = "".join(pct_fmt(series[c], revenue[c]).rjust(col_width + 4) for c in columns)
                print(f"  {LABEL_COL}{item:<42}{RESET}{vals}")

    # ── BALANCE SHEET: % of Total Assets ──
    sub_header("Balance Sheet  (all items as % of Total Assets)")
    bs = data["balance"]
    if bs is not None and not bs.empty:
        columns = bs.columns.tolist()
        ta_row  = [k for k in bs.index if "total assets" in str(k).lower()]
        if not ta_row:
            print(f"  {NEG_COL}Total Assets row not found.{RESET}")
        else:
            total_assets = bs.loc[ta_row[0]]
            header = f"  {'LINE ITEM':<42}" + "".join(
                HEADER_COL + f"{str(c.date() if hasattr(c,'date') else c):>{col_width}}" + RESET
                for c in columns
            )
            print(header)
            print(DIVIDER)
            items_to_show = [
                "Cash And Cash Equivalents",
                "Receivables",
                "Inventory",
                "Current Assets",
                "Net PPE",
                "Goodwill",
                "Total Assets",
                "Current Liabilities",
                "Long Term Debt",
                "Total Liabilities Net Minority Interest",
                "Stockholders Equity",
            ]
            for item in items_to_show:
                matches = [k for k in bs.index if item.lower() in str(k).lower()]
                if not matches:
                    continue
                series = bs.loc[matches[0]]
                vals   = "".join(pct_fmt(series[c], total_assets[c]).rjust(col_width + 4) for c in columns)
                print(f"  {LABEL_COL}{item[:42]:<42}{RESET}{vals}")

    # ── CASH FLOW: % of CFO ──
    sub_header("Cash Flow Statement  (items as % of Operating Cash Flow)")
    cf = data["cashflow"]
    if cf is not None and not cf.empty:
        columns = cf.columns.tolist()
        cfo_row = [k for k in cf.index if "operating cash flow" in str(k).lower()]
        if not cfo_row:
            print(f"  {NEG_COL}CFO row not found.{RESET}")
        else:
            cfo = cf.loc[cfo_row[0]]
            header = f"  {'LINE ITEM':<42}" + "".join(
                HEADER_COL + f"{str(c.date() if hasattr(c,'date') else c):>{col_width}}" + RESET
                for c in columns
            )
            print(header)
            print(DIVIDER)
            items_to_show = [
                "Net Income",
                "Depreciation Amortization Depletion",
                "Changes In Working Capital",
                "Operating Cash Flow",
                "Capital Expenditure",
                "Investing Cash Flow",
                "Financing Cash Flow",
                "Free Cash Flow",
            ]
            for item in items_to_show:
                matches = [k for k in cf.index if item.lower() in str(k).lower()]
                if not matches:
                    continue
                series = cf.loc[matches[0]]
                vals   = "".join(pct_fmt(series[c], cfo[c]).rjust(col_width + 4) for c in columns)
                print(f"  {LABEL_COL}{item[:42]:<42}{RESET}{vals}")


# ─────────────────────────────────────────────
#  SECTION 5 – CALCULATED FINANCIAL RATIOS
# ─────────────────────────────────────────────

def calculate_ratios(data: dict):
    inc = data["income"]
    bs  = data["balance"]
    cf  = data["cashflow"]
    info = data["info"]

    if inc is None or bs is None or cf is None:
        return {}

    def g(df, key):
        matches = [k for k in df.index if key.lower() in str(k).lower()]
        if matches:
            return df.loc[matches[0]]
        return pd.Series([np.nan] * len(df.columns), index=df.columns)

    cols = inc.columns.tolist()

    revenue        = g(inc, "Total Revenue")
    cogs           = g(inc, "Cost Of Revenue")
    gross_profit   = g(inc, "Gross Profit")
    ebit           = g(inc, "EBIT")
    ebitda         = g(inc, "EBITDA")
    net_income     = g(inc, "Net Income")
    interest_exp   = g(inc, "Interest Expense")
    tax_prov       = g(inc, "Tax Provision")
    pretax_income  = g(inc, "Pretax Income")

    current_assets = g(bs, "Current Assets")
    current_liab   = g(bs, "Current Liabilities")
    inventory      = g(bs, "Inventory")
    cash           = g(bs, "Cash And Cash Equivalents")
    receivables    = g(bs, "Receivables")
    total_assets   = g(bs, "Total Assets")
    total_liab     = g(bs, "Total Liabilities Net Minority Interest")
    equity         = g(bs, "Stockholders Equity")
    long_debt      = g(bs, "Long Term Debt")
    short_debt     = g(bs, "Current Debt")
    ppe            = g(bs, "Net PPE")

    cfo            = g(cf, "Operating Cash Flow")
    capex          = g(cf, "Capital Expenditure")
    fcf            = g(cf, "Free Cash Flow")

    ratios = {}

    # ── Profitability ──
    def safe_div(a, b):
        with np.errstate(divide='ignore', invalid='ignore'):
            return np.where(b != 0, a / b, np.nan)

    ratios["Gross Margin"]        = safe_div(gross_profit.values, revenue.values)
    ratios["EBIT Margin"]         = safe_div(ebit.values, revenue.values)
    ratios["EBITDA Margin"]       = safe_div(ebitda.values, revenue.values)
    ratios["Net Profit Margin"]   = safe_div(net_income.values, revenue.values)
    ratios["ROA"]                 = safe_div(net_income.values, total_assets.values)
    # ROE uses average equity
    avg_eq = (equity.values + np.roll(equity.values, 1)) / 2
    avg_eq[0] = equity.values[0]
    ratios["ROE"]                 = safe_div(net_income.values, avg_eq)
    total_capital = equity.values + long_debt.values
    ratios["ROCE"]                = safe_div(ebit.values, total_capital)

    # ── Efficiency / Activity ──
    avg_assets     = (total_assets.values + np.roll(total_assets.values, 1)) / 2; avg_assets[0] = total_assets.values[0]
    avg_rec        = (receivables.values  + np.roll(receivables.values, 1)) / 2;  avg_rec[0]    = receivables.values[0]
    avg_inv        = (inventory.values    + np.roll(inventory.values, 1)) / 2;    avg_inv[0]    = inventory.values[0]
    ratios["Asset Turnover"]      = safe_div(revenue.values, avg_assets)
    ratios["Receivables Turnover"]= safe_div(revenue.values, avg_rec)
    ratios["DSO (days)"]          = safe_div(avg_rec * 365, revenue.values)
    ratios["Inventory Turnover"]  = safe_div(cogs.values, avg_inv)
    ratios["DIO (days)"]          = safe_div(avg_inv * 365, cogs.values)
    ratios["Payables Turnover"]   = safe_div(cogs.values, safe_div(current_liab.values, 1))

    # ── Liquidity ──
    ratios["Current Ratio"]       = safe_div(current_assets.values, current_liab.values)
    quick_assets                  = current_assets.values - inventory.values
    ratios["Quick Ratio"]         = safe_div(quick_assets, current_liab.values)
    ratios["Cash Ratio"]          = safe_div(cash.values, current_liab.values)

    # ── Leverage / Solvency ──
    total_debt                    = long_debt.values + short_debt.values
    ratios["Debt / Equity"]       = safe_div(total_debt, equity.values)
    ratios["Debt / EBITDA"]       = safe_div(total_debt, ebitda.values)
    ratios["Net Debt / EBITDA"]   = safe_div(total_debt - cash.values, ebitda.values)
    ratios["Equity Multiplier"]   = safe_div(total_assets.values, equity.values)
    interest_abs                  = np.abs(interest_exp.values)
    ratios["Interest Coverage"]   = safe_div(ebit.values, interest_abs)
    ratios["Debt Ratio"]          = safe_div(total_liab.values, total_assets.values)

    # ── Cash Flow Quality ──
    ratios["CFO / Net Income"]    = safe_div(cfo.values, net_income.values)
    ratios["FCF / Net Income"]    = safe_div(fcf.values, net_income.values)
    ratios["FCF / Revenue"]       = safe_div(fcf.values, revenue.values)
    ratios["CapEx / CFO"]         = safe_div(np.abs(capex.values), cfo.values)
    ratios["CapEx / Revenue"]     = safe_div(np.abs(capex.values), revenue.values)

    # ── Tax Rate ──
    ratios["Effective Tax Rate"]  = safe_div(np.abs(tax_prov.values), pretax_income.values)

    return ratios, cols


def print_financial_ratios(data: dict):
    section_header("5 · Calculated Financial Ratios")

    result = calculate_ratios(data)
    if not result:
        print(f"\n  {NEG_COL}Insufficient data to compute ratios.{RESET}")
        return

    ratios, columns = result

    col_width = 14

    def header_line():
        return f"  {'RATIO':<42}" + "".join(
            HEADER_COL + f"{str(c.date() if hasattr(c,'date') else c):>{col_width}}" + RESET
            for c in columns
        )

    def ratio_row(label, key, fmt="pct"):
        vals = ratios.get(key)
        if vals is None:
            return
        line = ""
        for v in vals:
            if fmt == "pct":
                s = fmt_pct(v)
            elif fmt == "ratio":
                s = fmt_ratio(v)
            elif fmt == "days":
                color = VALUE_COL
                s     = color + f"{v:>8.1f}d" + RESET if not np.isnan(v) else DIM_COL + "     N/A" + RESET
            else:
                s = fmt_ratio(v)
            line += s.rjust(col_width + len(s) - len(s.strip()))
        print(f"  {LABEL_COL}{label:<42}{RESET}{line}")

    # ── Profitability ──
    sub_header("Profitability Ratios")
    print(header_line()); print(DIVIDER)
    ratio_row("Gross Margin",            "Gross Margin",      "pct")
    ratio_row("EBIT Margin",             "EBIT Margin",       "pct")
    ratio_row("EBITDA Margin",           "EBITDA Margin",     "pct")
    ratio_row("Net Profit Margin",       "Net Profit Margin", "pct")
    ratio_row("Return on Assets (ROA)",  "ROA",               "pct")
    ratio_row("Return on Equity (ROE)",  "ROE",               "pct")
    ratio_row("Return on Capital Emp.",  "ROCE",              "pct")
    ratio_row("Effective Tax Rate",      "Effective Tax Rate","pct")

    # ── Efficiency ──
    sub_header("Efficiency / Activity Ratios")
    print(header_line()); print(DIVIDER)
    ratio_row("Asset Turnover",           "Asset Turnover",       "ratio")
    ratio_row("Receivables Turnover",     "Receivables Turnover", "ratio")
    ratio_row("Days Sales Outstanding",   "DSO (days)",           "days")
    ratio_row("Inventory Turnover",       "Inventory Turnover",   "ratio")
    ratio_row("Days Inventory Outstanding","DIO (days)",          "days")

    # ── Liquidity ──
    sub_header("Liquidity Ratios")
    print(header_line()); print(DIVIDER)
    ratio_row("Current Ratio",  "Current Ratio", "ratio")
    ratio_row("Quick Ratio",    "Quick Ratio",   "ratio")
    ratio_row("Cash Ratio",     "Cash Ratio",    "ratio")

    # ── Leverage ──
    sub_header("Leverage / Solvency Ratios")
    print(header_line()); print(DIVIDER)
    ratio_row("Debt / Equity",     "Debt / Equity",     "ratio")
    ratio_row("Debt / EBITDA",     "Debt / EBITDA",     "ratio")
    ratio_row("Net Debt / EBITDA", "Net Debt / EBITDA", "ratio")
    ratio_row("Equity Multiplier", "Equity Multiplier", "ratio")
    ratio_row("Interest Coverage", "Interest Coverage", "ratio")
    ratio_row("Debt Ratio",        "Debt Ratio",        "ratio")

    # ── Cash Flow Quality ──
    sub_header("Cash Flow Quality Ratios")
    print(header_line()); print(DIVIDER)
    ratio_row("CFO / Net Income",  "CFO / Net Income",  "ratio")
    ratio_row("FCF / Net Income",  "FCF / Net Income",  "ratio")
    ratio_row("FCF / Revenue",     "FCF / Revenue",     "pct")
    ratio_row("CapEx / CFO",       "CapEx / CFO",       "pct")
    ratio_row("CapEx / Revenue",   "CapEx / Revenue",   "pct")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    # 1. Declare global at the very beginning of the scope
    global DEFAULT_YEARS 

    parser = argparse.ArgumentParser(
        description="Comprehensive Financial Statement Analyzer — powered by yfinance"
    )
    parser.add_argument(
        "--ticker", "-t",
        type=str,
        default=DEFAULT_TICKER,
        help=f"Ticker symbol (default: {DEFAULT_TICKER})"
    )
    parser.add_argument(
        "--years", "-y",
        type=int,
        default=DEFAULT_YEARS,
        help=f"Number of annual periods to show (default: {DEFAULT_YEARS})"
    )
    args = parser.parse_args()

    # 2. Now you can successfully update the global variable
    DEFAULT_YEARS = args.years

    # Fetch
    try:
        data = fetch_data(args.ticker)
    except Exception as e:
        print(f"\n{NEG_COL}  ERROR: Could not fetch data for '{args.ticker}': {e}{RESET}\n")
        sys.exit(1)

    # Print all sections
    print_title(data["info"], args.ticker)
    print_general_info(data["info"])
    print_financial_statements(data)
    print_common_size(data)
    print_financial_ratios(data)

    print()
    print(THICK_DIV)
    print(DIM_COL + "  End of report. Data sourced from Yahoo Finance via yfinance." + RESET)
    print(DIM_COL + "  This analysis is for informational purposes only — not financial advice." + RESET)
    print(THICK_DIV)
    print()

if __name__ == "__main__":
    main()
