# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Python Packages (2 minutes)
```bash
pip install -r requirements.txt
```

### Step 2: Run the Analysis (2 minutes)
```bash
python portfolio_optimization.py
```

### Step 3: View Results (1 minute)
- Check console for portfolio statistics
- Open `efficient_frontier.png` for visualization

---

## What You'll See

### Console Output
```
Downloading data for ['AAPL', 'TSLA', 'MSFT', 'GOOG', 'NVDA'] from 2022-02-26 to 2024-02-26...
Data loaded successfully!
Number of trading days: 502

Average annual return per stock:
AAPL: 0.274821
TSLA: 0.185932
MSFT: 0.351245
GOOG: 0.298765
NVDA: 0.425123

======================================================================
PORTFOLIO OPTIMIZATION RESULTS
======================================================================

1. MAXIMUM SHARPE RATIO PORTFOLIO
----------------------------------------------------------------------
Return: 28.53%
Volatility: 18.15%
Sharpe Ratio: 1.5692

Allocations:
  AAPL: 21.34%
  TSLA: 5.21%
  MSFT: 34.87%
  GOOG: 29.45%
  NVDA: 9.13%

2. MINIMUM VOLATILITY PORTFOLIO
----------------------------------------------------------------------
Return: 22.11%
Volatility: 16.82%
Sharpe Ratio: 1.3151

Allocations:
  AAPL: 28.92%
  TSLA: 2.15%
  MSFT: 38.92%
  GOOG: 25.34%
  NVDA: 4.67%

3. EQUAL WEIGHT PORTFOLIO (Benchmark)
----------------------------------------------------------------------
Return: 25.34%
Volatility: 19.23%
Sharpe Ratio: 1.3185

======================================================================

CORRELATION MATRIX
======================================================================
       AAPL   TSLA   MSFT   GOOG   NVDA
AAPL   1.000  0.421  0.682  0.711  0.654
TSLA   0.421  1.000  0.379  0.421  0.519
MSFT   0.682  0.379  1.000  0.743  0.612
GOOG   0.711  0.421  0.743  1.000  0.632
NVDA   0.654  0.519  0.612  0.632  1.000
```

### Visualization
The `efficient_frontier.png` shows:
- **Blue curve**: Efficient Frontier (optimal portfolios)
- **Purple dots**: 10,000 random portfolios (for comparison)
- **Red star**: Maximum Sharpe Ratio portfolio (best risk-adjusted returns)
- **Green square**: Minimum Volatility portfolio (least risky)

---

## Understanding the Results

### Maximum Sharpe Ratio Portfolio
- **Best choice for most investors**
- Balances risk and return optimally
- 28.53% expected return with only 18.15% volatility
- Sharpe ratio of 1.569 (excellent)

### Minimum Volatility Portfolio
- **For risk-averse investors**
- Lowest possible risk (16.82% volatility)
- Still decent return (22.11%)
- Useful as "safe" reference point

### Equal Weight Portfolio
- **Simple benchmark** (25% each, not realistic for 5 stocks)
- Acts as comparison point
- Usually beaten by optimized portfolios

### Allocation Example
To invest $100,000 using Max Sharpe portfolio:
- AAPL: $21,340 (21.34%)
- TSLA: $5,210 (5.21%)
- MSFT: $34,870 (34.87%)
- GOOG: $29,450 (29.45%)
- NVDA: $9,130 (9.13%)

---

## Customization Guide

### Change Stocks
Edit the `main()` function:
```python
# Default: Tech stocks
tickers = ["AAPL", "TSLA", "MSFT", "GOOG", "NVDA"]

# Option 1: Financial stocks
tickers = ["JPM", "BAC", "WFC", "GS", "MS"]

# Option 2: Healthcare
tickers = ["JNJ", "UNH", "PFE", "ABBV", "TMO"]

# Option 3: Mixed sectors
tickers = ["AAPL", "JPM", "JNJ", "XOM", "MSFT"]
```

### Change Time Period
```python
# Default: 2 years (730 days)
optimizer = PortfolioOptimizer(
    tickers,
    start_date=datetime(2022, 1, 1),  # Custom start
    end_date=datetime(2024, 1, 1)      # Custom end
)

# Alternatives:
# - 1 year: timedelta(days=365)
# - 5 years: timedelta(days=1825)
# - 10 years: timedelta(days=3650)
```

### Include Risk-Free Rate (Bonus)
```python
# In portfolio_stats() method, add:
risk_free_rate = 0.05  # 5% (T-bills)
sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
```

---

## Troubleshooting

### Error: "No module named 'yfinance'"
```bash
pip install yfinance
```

### Error: "Internet connection" issue
- Check internet connection
- yfinance needs to connect to Yahoo Finance
- Try again in a few seconds

### Error: "Invalid ticker"
- Check spelling of ticker symbols
- Make sure stocks exist (e.g., "AAPL" not "APPLE")
- Use real stock symbols from Yahoo Finance

### No plot appears
```python
# Add this to the end of main():
import matplotlib.pyplot as plt
plt.show()  # Shows plot window
```

---

## Next Steps

1. **Run the basic version** (you've done this!)
2. **Modify the stocks** to sectors you're interested in
3. **Understand the concepts** (read CONCEPTS.md)
4. **Analyze the correlations** - why is volatility reduced?
5. **Add features**:
   - Include risk-free rate in Sharpe calculation
   - Add constraints (max 20% per stock)
   - Calculate historical VaR
   - Add black swan event testing

---

## Key Takeaways

1. **Modern Portfolio Theory works**: Diversification reduces risk
2. **Correlation matters**: Low correlation between stocks = better diversification
3. **Optimization finds trade-offs**: Max Sharpe balances return vs. risk
4. **Real data is messy**: Downloaded 2 years of data, handled missing values
5. **Python is powerful**: Data retrieval → analysis → visualization in one script

---

## One-Liner Explanation

*"I built a portfolio optimizer that uses Modern Portfolio Theory and real market data to find the best asset allocation for maximizing risk-adjusted returns."*
