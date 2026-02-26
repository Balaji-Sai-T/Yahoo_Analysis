# Financial Concepts Deep Dive

## 1. Modern Portfolio Theory (MPT)

### Historical Context
- **Introduced by Harry Markowitz** in 1952
- Won Nobel Prize in Economics (1990)
- Revolutionized investment management

### Core Principles
1. **Risk vs. Return Tradeoff**
   - More return requires more risk
   - Cannot achieve high return with low risk
   - Optimal portfolios balance this tradeoff

2. **Diversification Reduces Risk**
   - Combination of assets reduces overall volatility
   - Works best with low/negative correlation
   - Example: Stock + Bond portfolio is less risky than either alone

3. **Portfolio Risk ≠ Weighted Average of Individual Risks**
   - Correlation matters critically
   - 50% Stock A (σ=20%) + 50% Stock B (σ=20%) ≠ σ=20%
   - Actual portfolio volatility depends on correlation

### Mathematical Formula
```
Portfolio Return = Σ(w_i × R_i)

Portfolio Volatility = √[Σ Σ(w_i × w_j × Cov(i,j))]

Where:
- w_i = weight of asset i
- R_i = return of asset i
- Cov(i,j) = covariance between assets i and j
```

## 2. Volatility (Standard Deviation)

### What It Measures
- **Price fluctuation frequency and magnitude**
- Historical measure based on past returns
- Annualized from daily data (multiply by √252 trading days)

### Calculation
```python
Daily Return = (Price_today - Price_yesterday) / Price_yesterday
Volatility = std_dev(daily_returns) × √252
```

### Interpretation
- **Low volatility (< 15%)**: Stable, less risky
- **Medium volatility (15-25%)**: Moderate risk
- **High volatility (> 25%)**: Significant price swings

### Examples
- Tech stocks: 25-40% volatility
- Blue chips: 15-25% volatility
- Government bonds: 3-8% volatility

## 3. Correlation & Covariance

### Correlation Matrix (-1 to +1)
```
 +1 = Perfect positive correlation
  0 = No correlation
 -1 = Perfect negative correlation
```

### Tech Stock Example
```
        AAPL   TSLA   MSFT   GOOG   NVDA
AAPL   1.00   0.42   0.68   0.71   0.65
TSLA   0.42   1.00   0.38   0.42   0.52
MSFT   0.68   0.38   1.00   0.74   0.61
GOOG   0.71   0.42   0.74   1.00   0.63
NVDA   0.65   0.52   0.61   0.63   1.00
```

### Interpretation
- **0.71 between AAPL-GOOG**: High positive correlation (move together)
- **0.38 between TSLA-MSFT**: Low positive correlation (more diversification)

### Why Correlation Matters
- Low correlation = better diversification
- High correlation = redundant holdings
- Negative correlation = perfect hedge

## 4. Efficient Frontier

### Definition
- **Set of optimal portfolios** with highest return for each risk level
- Dominates all other portfolios below the curve
- Any portfolio below the frontier is suboptimal

### Key Points on Frontier
1. **Minimum Variance Portfolio (MVP)**
   - Lowest possible volatility
   - Usually boring stocks with stable returns
   - Least return

2. **Maximum Sharpe Ratio Portfolio**
   - Best risk-adjusted return
   - "Optimal" in most scenarios
   - Higher return than MVP

3. **Maximum Return Portfolio**
   - Highest return (often 100% in single stock)
   - Maximum volatility
   - Rightmost point on frontier

### Shape
- Curved (parabolic) shape
- Convex (bows outward)
- Achievable through diversification

## 5. Sharpe Ratio

### Formula
```
Sharpe Ratio = (Portfolio Return - Risk-Free Rate) / Portfolio Volatility

Example:
Portfolio Return = 15%
Risk-Free Rate = 5% (T-bills)
Volatility = 10%

Sharpe = (0.15 - 0.05) / 0.10 = 1.0
```

### Interpretation
- **Sharpe > 1.0**: Excellent risk-adjusted return
- **0.5 - 1.0**: Good return for risk taken
- **< 0.5**: Poor risk-adjusted return
- **Negative**: Portfolio underperforming risk-free asset

### Example Comparison
```
Portfolio A: 20% return, 15% volatility, Sharpe = 1.0
Portfolio B: 15% return, 10% volatility, Sharpe = 1.0
→ Same Sharpe ratio, but A takes more risk for higher return
```

## 6. Covariance Matrix

### What It Is
- **Measures joint movement of assets**
- More detailed than correlation
- Used directly in portfolio calculations

### Relationship
```
Correlation = Covariance / (σ_i × σ_j)
```

### Using in Optimization
```
Portfolio Variance = w^T × Cov_Matrix × w

Where:
- w = weight vector
- Cov_Matrix = covariance matrix of returns
- w^T = transpose of w

Larger covariance values → larger portfolio variance
Negative covariance → diversification benefit
```

## 7. Portfolio Optimization

### What We're Solving
```
Maximize: Portfolio Return
Subject to:
  - Minimize: Portfolio Volatility (or Maximize: Sharpe Ratio)
  - Constraint: All weights sum to 1
  - Constraint: 0 ≤ weight ≤ 1 (no short selling)
```

### Optimization Methods
1. **Lagrange Multipliers**: Traditional mathematical approach
2. **Quadratic Programming**: Efficient computational method
3. **Sequential Least Squares Programming (SLSQP)**: Used in scipy

### Output
- **Optimal weights**: How much to allocate to each stock
- **Expected return**: Annual portfolio return
- **Portfolio volatility**: Annual portfolio risk
- **Sharpe ratio**: Risk-adjusted performance metric

## 8. Real-World Application: Portfolio Rebalancing

### Scenario
You have $100,000 to invest in 5 tech stocks

**Optimal Weights (from our model):**
- AAPL: 25%
- TSLA: 15%
- MSFT: 30%
- GOOG: 20%
- NVDA: 10%

**Action Plan:**
- AAPL: $25,000
- TSLA: $15,000
- MSFT: $30,000
- GOOG: $20,000
- NVDA: $10,000

**Expected Performance:**
- Annual return: ~28%
- Annual volatility: ~18%
- Sharpe ratio: ~1.5

## 9. Common Mistakes to Avoid

### Mistake 1: Ignoring Correlation
❌ "I'll buy 5 tech stocks for diversification"
✓ Buy across sectors: Tech + Finance + Healthcare

### Mistake 2: Chasing Past Performance
❌ "This stock had 50% return last year, buy it!"
✓ Use forward-looking volatility and correlation estimates

### Mistake 3: Overconcentration
❌ 80% in one stock
✓ Maximum weight per stock: 20-30%

### Mistake 4: Ignoring Transaction Costs
❌ Rebalancing weekly
✓ Rebalance quarterly/annually

### Mistake 5: Assuming Normal Distribution
❌ Ignoring extreme events (black swan events)
✓ Use value-at-risk, stress testing

## 10. Extensions & Advanced Topics

### Value at Risk (VaR)
- **Probability of loss exceeding X** in time period
- Example: "95% VaR = $5,000" means 95% chance daily loss < $5,000

### Conditional Value at Risk (CVaR)
- Expected loss given worst 5% outcomes
- More robust than VaR

### Black-Litterman Model
- Combines market equilibrium with investor views
- Addresses instability in Markowitz optimization
- Better for real-world portfolios

### Factor Models
- Explains returns through factors (size, value, momentum)
- Reduces dimensionality
- Improves stability

### Machine Learning Approaches
- Neural networks for correlation prediction
- Ensemble methods for weight optimization
- Time series forecasting for expected returns
