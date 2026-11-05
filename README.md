# Black-Scholes Pricer

A small Python project that downloads a stock's price history from Yahoo Finance, saves it as a CSV file, and prices a European option with the Black-Scholes-Merton model.

## How it works

1. **Ticker input**: the script checks that the ticker exists on Yahoo Finance (`yfinance`).
2. **Download**: the price history between two dates is saved to `TICKER.csv` (columns `Date`, `Close`, `Dividends`).
3. **Parameters computed from the CSV**:
   - `S`: latest closing price,
   - `sigma`: historical volatility, the standard deviation of log returns × √252,
   - `q`: annualised dividend yield.
4. **User input**: strike `K`, duration `T` (in years) and risk-free rate `r`.
5. **Pricing**: the call and put prices are displayed.

## Installation

```bash
pip install yfinance pandas numpy scipy
```

## Usage

```bash
python Scraping.py
```

Example:

```
Ticker : AAPL
start date (AAAA-MM-DD) : 2022-01-01
end date (AAAA-MM-DD) : 2026-01-01
Strike : 355
Duration (ex : 0.5 = 6 months) : 0.5
Risque free rate (ex : 0.03 for 3%) : 0.03
```

## Formulas

Call: C = S·e^(−qT)·N(d₁) − K·e^(−rT)·N(d₂)

Put: P = K·e^(−rT)·N(−d₂) − S·e^(−qT)·N(−d₁)

where d₁ = [ln(S/K) + (r − q + σ²/2)·T] / (σ√T) and d₂ = d₁ − σ√T.

## Limitations

- The model is European, whereas US stock options are often American.
- Volatility is historical: it measures the past, not the market's expectations.
- Dividends are treated as a continuous yield, not as discrete payments.
- Yahoo data may have a slight delay.

## Possible improvements

- Find the strike matching a target call price (bisection).
- Compute implied volatility from a market price.
- Guard against `T = 0` and validate the dates entered.
