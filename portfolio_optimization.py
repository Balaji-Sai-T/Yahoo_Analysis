"""
Portfolio Optimization using Markowitz Efficient Frontier
Demonstrates Modern Portfolio Theory (MPT) for tech stocks
"""

import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from datetime import datetime, timedelta


class PortfolioOptimizer:
    """Optimize portfolio using Markowitz Efficient Frontier"""
    
    def __init__(self, tickers, start_date=None, end_date=None):
        """
        Initialize with list of tickers
        
        Args:
            tickers: List of stock symbols
            start_date: Start date for historical data (default: 2 years ago)
            end_date: End date for historical data (default: today)
        """
        self.tickers = tickers
        
        # Set default dates if not provided
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=730)  # 2 years
            
        self.start_date = start_date
        self.end_date = end_date
        
        # Download historical data
        print(f"Downloading data for {tickers} from {start_date.date()} to {end_date.date()}...")
        self.data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
        
        # Calculate daily returns
        self.returns = self.data.pct_change().dropna()
        
        # Calculate covariance matrix and mean returns
        self.cov_matrix = self.returns.cov()
        self.mean_returns = self.returns.mean()
        
        print(f"\nData loaded successfully!")
        print(f"Number of trading days: {len(self.data)}")
        print(f"Average annual return per stock:")
        print((self.mean_returns * 252).to_string())
    
    def portfolio_stats(self, weights):
        """
        Calculate portfolio return, volatility, and Sharpe ratio
        
        Args:
            weights: Array of portfolio weights
            
        Returns:
            Tuple of (return, volatility, sharpe_ratio)
        """
        portfolio_return = np.sum(self.mean_returns * weights) * 252
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 252, weights)))
        sharpe_ratio = portfolio_return / portfolio_volatility
        
        return portfolio_return, portfolio_volatility, sharpe_ratio
    
    def negative_sharpe(self, weights):
        """Objective function: negative Sharpe ratio (for minimization)"""
        return -self.portfolio_stats(weights)[2]
    
    def portfolio_volatility_func(self, weights):
        """Objective function: portfolio volatility"""
        return self.portfolio_stats(weights)[1]
    
    def optimize_max_sharpe(self):
        """Find portfolio with maximum Sharpe ratio"""
        n_assets = len(self.tickers)
        
        # Constraints: weights sum to 1
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        
        # Bounds: weights between 0 and 1 (no short selling)
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        # Initial guess: equal weights
        init_guess = np.array([1/n_assets] * n_assets)
        
        # Optimize
        result = minimize(
            self.negative_sharpe,
            init_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def optimize_min_volatility(self):
        """Find portfolio with minimum volatility"""
        n_assets = len(self.tickers)
        
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(n_assets))
        init_guess = np.array([1/n_assets] * n_assets)
        
        result = minimize(
            self.portfolio_volatility_func,
            init_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        return result.x
    
    def generate_random_portfolios(self, n=10000):
        """Generate random portfolios for comparison"""
        results = np.zeros((3, n))
        
        np.random.seed(42)
        for i in range(n):
            weights = np.random.random(len(self.tickers))
            weights /= np.sum(weights)
            
            ret, vol, sharpe = self.portfolio_stats(weights)
            results[0,i] = ret
            results[1,i] = vol
            results[2,i] = sharpe
        
        return results
    
    def efficient_frontier(self, n_points=100):
        """Generate points along efficient frontier"""
        min_ret = self.mean_returns.min() * 252
        max_ret = self.mean_returns.max() * 252
        target_returns = np.linspace(min_ret, max_ret, n_points)
        
        efficient_vols = []
        efficient_weights = []
        
        for target_ret in target_returns:
            constraints = (
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: np.sum(self.mean_returns * x) * 252 - target_ret}
            )
            bounds = tuple((0, 1) for _ in range(len(self.tickers)))
            init_guess = np.array([1/len(self.tickers)] * len(self.tickers))
            
            result = minimize(
                self.portfolio_volatility_func,
                init_guess,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            if result.success:
                efficient_vols.append(result.fun)
                efficient_weights.append(result.x)
        
        return target_returns, np.array(efficient_vols)
    
    def print_results(self):
        """Print optimized portfolio results"""
        print("\n" + "="*70)
        print("PORTFOLIO OPTIMIZATION RESULTS")
        print("="*70)
        
        # Max Sharpe
        weights_sharpe = self.optimize_max_sharpe()
        ret_sharpe, vol_sharpe, sharpe_sharpe = self.portfolio_stats(weights_sharpe)
        
        print("\n1. MAXIMUM SHARPE RATIO PORTFOLIO")
        print("-" * 70)
        print(f"Return: {ret_sharpe*100:.2f}%")
        print(f"Volatility: {vol_sharpe*100:.2f}%")
        print(f"Sharpe Ratio: {sharpe_sharpe:.4f}")
        print("\nAllocations:")
        for ticker, weight in zip(self.tickers, weights_sharpe):
            print(f"  {ticker}: {weight*100:.2f}%")
        
        # Min Volatility
        weights_minvol = self.optimize_min_volatility()
        ret_minvol, vol_minvol, sharpe_minvol = self.portfolio_stats(weights_minvol)
        
        print("\n2. MINIMUM VOLATILITY PORTFOLIO")
        print("-" * 70)
        print(f"Return: {ret_minvol*100:.2f}%")
        print(f"Volatility: {vol_minvol*100:.2f}%")
        print(f"Sharpe Ratio: {sharpe_minvol:.4f}")
        print("\nAllocations:")
        for ticker, weight in zip(self.tickers, weights_minvol):
            print(f"  {ticker}: {weight*100:.2f}%")
        
        # Equal Weight
        weights_equal = np.array([1/len(self.tickers)] * len(self.tickers))
        ret_equal, vol_equal, sharpe_equal = self.portfolio_stats(weights_equal)
        
        print("\n3. EQUAL WEIGHT PORTFOLIO (Benchmark)")
        print("-" * 70)
        print(f"Return: {ret_equal*100:.2f}%")
        print(f"Volatility: {vol_equal*100:.2f}%")
        print(f"Sharpe Ratio: {sharpe_equal:.4f}")
        
        print("\n" + "="*70)
        
        return {
            'max_sharpe': (weights_sharpe, ret_sharpe, vol_sharpe, sharpe_sharpe),
            'min_vol': (weights_minvol, ret_minvol, vol_minvol, sharpe_minvol),
            'equal': (weights_equal, ret_equal, vol_equal, sharpe_equal)
        }
    
    def plot_efficient_frontier(self):
        """Plot efficient frontier and optimal portfolios"""
        # Generate random portfolios
        random_portfolios = self.generate_random_portfolios()
        
        # Generate efficient frontier
        target_returns, efficient_vols = self.efficient_frontier(n_points=50)
        
        # Calculate optimal portfolios
        weights_sharpe = self.optimize_max_sharpe()
        ret_sharpe, vol_sharpe, sharpe_sharpe = self.portfolio_stats(weights_sharpe)
        
        weights_minvol = self.optimize_min_volatility()
        ret_minvol, vol_minvol, sharpe_minvol = self.portfolio_stats(weights_minvol)
        
        # Create plot
        plt.figure(figsize=(12, 8))
        
        # Plot random portfolios
        plt.scatter(random_portfolios[1,:]*100, random_portfolios[0,:]*100, 
                   c=random_portfolios[2,:], cmap='viridis', alpha=0.3, s=10,
                   label='Random Portfolios')
        
        # Plot efficient frontier
        plt.plot(efficient_vols*100, target_returns*100, 'b-', linewidth=2, 
                label='Efficient Frontier')
        
        # Plot optimal portfolios
        plt.scatter(vol_sharpe*100, ret_sharpe*100, marker='*', color='red', 
                   s=500, edgecolors='black', linewidth=2, 
                   label=f'Max Sharpe ({sharpe_sharpe:.3f})', zorder=5)
        
        plt.scatter(vol_minvol*100, ret_minvol*100, marker='s', color='green', 
                   s=300, edgecolors='black', linewidth=2, 
                   label=f'Min Volatility ({vol_minvol*100:.2f}%)', zorder=5)
        
        plt.xlabel('Volatility (Annual %)', fontsize=12, fontweight='bold')
        plt.ylabel('Return (Annual %)', fontsize=12, fontweight='bold')
        plt.title('Markowitz Efficient Frontier - Tech Stocks Portfolio', 
                 fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        plt.savefig('efficient_frontier.png', dpi=300, bbox_inches='tight')
        print("\nPlot saved as 'efficient_frontier.png'")
        plt.show()


def main():
    """Main execution"""
    # Tech stocks for portfolio
    tickers = ["AAPL", "TSLA", "MSFT", "GOOG", "NVDA"]
    
    # Create optimizer
    optimizer = PortfolioOptimizer(tickers)
    
    # Print detailed results
    optimizer.print_results()
    
    # Plot efficient frontier
    optimizer.plot_efficient_frontier()
    
    # Display correlation matrix
    print("\n" + "="*70)
    print("CORRELATION MATRIX")
    print("="*70)
    correlation = optimizer.returns.corr()
    print(correlation.to_string())


if __name__ == "__main__":
    main()
