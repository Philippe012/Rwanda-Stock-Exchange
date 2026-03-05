import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.linear_model import LinearRegression
import warnings

warnings.filterwarnings('ignore')

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Rwanda Stock Exchange.xlsx"

print(f"Loading data from: {DATA_PATH}")
print(f"File exists: {DATA_PATH.exists()}\n")

sheets = pd.read_excel(DATA_PATH, sheet_name=None)

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


# SHEET 1: Market Indicators
def analyze_indicators(df):
    print("Market Indicators Analysis")
    print("=" * 50)

    df_clean = df.dropna(subset=['Indicator']).copy()
    numeric_cols = ['Previous', 'Current', 'Change']
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    indicators = df_clean[df_clean['Indicator'].isin(['RSI', 'ALSI', 'EAESI'])]
    if not indicators.empty:
        print(indicators.to_string(index=False))

        avg_change = indicators['Change'].mean()
        print(f"\n Forecast: Average indicator change ≈ {avg_change:+.2f}")

    # Visualization
    if not indicators.empty:
        plt.figure(figsize=(8, 5))
        x_pos = np.arange(len(indicators))
        width = 0.35

        plt.bar(x_pos - width / 2, indicators['Previous'], width, label='Previous', alpha=0.8)
        plt.bar(x_pos + width / 2, indicators['Current'], width, label='Current', alpha=0.8)
        plt.xticks(x_pos, indicators['Indicator'])
        plt.ylabel('Value')
        plt.title('Market Indicators: Previous vs Current')
        plt.legend()
        plt.tight_layout()
        plt.savefig(BASE_DIR / "output" / "indicators_comparison.png", dpi=300)
        print(" Saved: indicators_comparison.png")
        plt.close()

    return indicators


# SHEET 2: Equity Markets
def analyze_equity(df):
    print("\n Equity Market Analysis")
    print("=" * 50)

    df_clean = df.copy()
    numeric_cols = ['Closing', 'Previous', 'Volume', 'Value']
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    df_clean['Change_pct'] = df_clean['Change (%)'].str.extract(r'([+\-]?[\d.]+)%').astype(float)

    active = df_clean[df_clean['Volume'] > 0]
    if not active.empty:
        print("Active Stocks:")
        print(active[['Security', 'Closing', 'Volume', 'Value', 'Change_pct']].to_string(index=False))

        active = active.copy()
        active['Predicted_Next'] = active['Closing'] * (1 + active['Change_pct'] / 100)
        print("\n Next Price Predictions (trend-based):")
        print(active[['Security', 'Closing', 'Predicted_Next']].to_string(index=False))

    plt.figure(figsize=(10, 6))

    if not active.empty:
        plt.subplot(1, 2, 1)
        plt.barh(active['Security'], active['Closing'], color='skyblue', edgecolor='navy')
        plt.xlabel('Closing Price (FRW)')
        plt.title('Active Stocks - Closing Prices')
        plt.gca().invert_yaxis()

    plt.subplot(1, 2, 2)
    plt.scatter(df_clean['Volume'], df_clean['Value'], alpha=0.7, c=df_clean['Change_pct'], cmap='RdYlGn')
    plt.xlabel('Volume')
    plt.ylabel('Value (FRW)')
    plt.title('Volume vs Value (Color = Change %)')
    plt.xscale('log')
    plt.yscale('log')
    plt.colorbar(label='Change %')

    plt.tight_layout()
    plt.savefig(BASE_DIR / "output" / "equity_analysis.png", dpi=300)
    print("Saved: equity_analysis.png")
    plt.close()

    # Stats
    print(f"\n Equity Stats:")
    print(f"   • Mean Closing Price: {df_clean['Closing'].mean():.2f} FRW")
    print(f"   • Total Volume: {df_clean['Volume'].sum():,.0f} shares")
    print(f"   • Total Value: {df_clean['Value'].sum():,.0f} FRW")

    return df_clean


# SHEET 3: Bond Market
def analyze_bonds(df):
    print("\n Bond Market Analysis")
    print("=" * 50)

    df_clean = df.copy()
    numeric_cols = ['Closing', 'Previous', 'Volume', 'Value']
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    df_clean['Change_pct'] = df_clean['Change (%)'].str.extract(r'([+\-]?[\d.]+)%').astype(float)

    print(df_clean[['Bond', 'Closing', 'Change_pct', 'Volume']].to_string(index=False))

    # Simple forecast: naive trend
    if len(df_clean) >= 2:
        avg_change = df_clean['Change_pct'].mean()
        avg_closing = df_clean['Closing'].mean()
        predicted = avg_closing * (1 + avg_change / 100)
        print(f"\n🔮 Avg Bond Price Forecast: {predicted:.2f} (based on avg trend)")

    # 📊 Visualization
    plt.figure(figsize=(10, 5))

    # Bond closing prices
    plt.subplot(1, 2, 1)
    bonds_short = df_clean['Bond'].str[:25] + '...'
    plt.plot(bonds_short, df_clean['Closing'], marker='o', linewidth=2)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Closing Price')
    plt.title('Bond Closing Prices')
    plt.grid(True, alpha=0.3)

    # Volume distribution
    plt.subplot(1, 2, 2)
    plt.barh(range(len(df_clean)), df_clean['Volume'] / 1e6, color='lightcoral')
    plt.yticks(range(len(df_clean)), df_clean['Bond'].str[:20])
    plt.xlabel('Volume (Millions)')
    plt.title('Bond Trading Volume')
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.savefig(BASE_DIR / "output" / "bond_analysis.png", dpi=300)
    print(" Saved: bond_analysis.png")
    plt.close()

    print(f"\n Bond Stats:")
    print(f"   • Avg Closing: {df_clean['Closing'].mean():.2f}")
    print(f"   • Total Volume: {df_clean['Volume'].sum():,.0f}")

    return df_clean


# SHEET 4: Exchange Rates
def analyze_forex(df):
    print("\n Exchange Rate Analysis")
    print("=" * 50)

    df_clean = df.copy()
    numeric_cols = ['Buying Value', 'Average Value', 'Selling Value']
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    print(df_clean[['Country', 'Code/CCY', 'Average Value']].to_string(index=False))

    df_clean = df_clean.copy()
    df_clean['Spread'] = df_clean['Selling Value'] - df_clean['Buying Value']
    df_clean['Predicted_Low'] = df_clean['Average Value'] - df_clean['Spread'] * 0.5
    df_clean['Predicted_High'] = df_clean['Average Value'] + df_clean['Spread'] * 0.5

    print("\n Next Day Forecast Range (Average +- 50% spread):")
    print(df_clean[['Code/CCY', 'Predicted_Low', 'Predicted_High']].to_string(index=False))

    plt.figure(figsize=(10, 6))

    x_pos = np.arange(len(df_clean))
    width = 0.25

    plt.bar(x_pos - width, df_clean['Buying Value'], width, label='Buying', alpha=0.8)
    plt.bar(x_pos, df_clean['Average Value'], width, label='Average', alpha=0.9)
    plt.bar(x_pos + width, df_clean['Selling Value'], width, label='Selling', alpha=0.8)

    plt.xticks(x_pos, df_clean['Code/CCY'])
    plt.ylabel('Value vs FRW')
    plt.title('Exchange Rates: Buy/Average/Sell')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(BASE_DIR / "output" / "forex_analysis.png", dpi=300)
    print("Saved: forex_analysis.png")
    plt.close()

    usd = df_clean[df_clean['Code/CCY'] == 'USD']
    if not usd.empty:
        print(f"\n🇺🇸 USD Focus:")
        print(f"   • Current Avg: {usd['Average Value'].values[0]:.2f} FRW")
        print(f"   • Forecast Range: {usd['Predicted_Low'].values[0]:.2f} - {usd['Predicted_High'].values[0]:.2f} FRW")

    return df_clean


def main():
    output_dir = BASE_DIR / "output"
    output_dir.mkdir(exist_ok=True)

    print("Rwanda Stock Exchange Prediction Framework")
    print("=" * 60 + "\n")

    indicators_df = analyze_indicators(sheets['Sheet1'])
    equity_df = analyze_equity(sheets['Sheet2'])
    bond_df = analyze_bonds(sheets['Sheet3'])
    forex_df = analyze_forex(sheets['Sheet4'])

    plt.figure(figsize=(12, 8))
    plt.suptitle('RSE Market Summary Dashboard', fontsize=16, fontweight='bold')

    # 1. Key Metrics
    plt.subplot(2, 2, 1)
    metrics = ['Equity\nVolume', 'Bond\nVolume', 'Market Cap\n(Trillions FRW)', 'USD\nRate']
    values = [107.45, 475.34, 4.78, 1458.11]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    bars = plt.bar(metrics, values, color=colors, edgecolor='black')
    plt.ylabel('Value')
    plt.title('Key Market Metrics')
    for bar, val in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{val:.2f}',
                 ha='center', va='bottom', fontsize=9)

    # 2. Active Stocks
    plt.subplot(2, 2, 2)
    active = equity_df[equity_df['Volume'] > 0]
    if not active.empty:
        plt.pie(active['Value'], labels=active['Security'], autopct='%1.1f%%', startangle=90)
        plt.title('Active Stocks: Value Distribution')

    # 3. Bond Performance
    plt.subplot(2, 2, 3)
    plt.plot(bond_df['Bond'].str[:15], bond_df['Closing'], marker='s', linewidth=2)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Closing Price')
    plt.title('Bond Price Trends')
    plt.grid(True, alpha=0.3)

    # 4. Forex Heatmap
    plt.subplot(2, 2, 4)
    forex_data = forex_df[['Code/CCY', 'Buying Value', 'Average Value', 'Selling Value']].set_index('Code/CCY')
    sns.heatmap(forex_data.T, annot=True, fmt='.2f', cmap='YlOrRd', cbar_kws={'label': 'Rate vs FRW'})
    plt.title('Exchange Rates Heatmap')
    plt.xlabel('Currency')

    plt.tight_layout()
    plt.savefig(output_dir / "rse_dashboard.png", dpi=300, bbox_inches='tight')
    print("\nSaved: rse_dashboard.png (Summary Dashboard)")
    plt.show()

    print("\n" + "=" * 60)
    print("All analyses complete! Check the 'output/' folder for visualizations.")
    print("Note: Predictions are simplified trend projections for educational purposes.")
    print("=" * 60)


if __name__ == "__main__":
    main()