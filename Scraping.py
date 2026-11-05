import numpy as np
import pandas as pd
import yfinance
import csv
import math
from scipy.stats import norm
#Importing library used for the code and engine

#declaring Black-Scholes function and building the engine
def black_scholes(S, K, T, r, sigma, q:float=0.0, option_type:str="call"):
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if option_type == "call": #Implementing 2 options call and put
        return S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(-q * T) * norm.cdf(-d1)
    else: #error message if the user select something else than "Call" or "Put"
        raise ValueError("option_type must be 'call' or 'put'")

while True : #loop instructions while it pass the ticker test
    user_ticker = input("Ticker : ").upper() #create the ticker variable and format
    ticker =  yfinance.Ticker(user_ticker) #Script look for the users ticker and informations related
    info = ticker.info
    if info.get("symbol") : #pick the ticker
        break #break the loop if the ticker don't exist or miswritten
    print("Incorrect ticker") #error message in case of incorrect ticker

#Parameters of period to import from yahoo
while True :
    starting_period = input("start date (AAAA-MM-DD) : ") #format is displayed, we should respect it either it doesn't work
    ending_period = input("end date (AAAA-MM-DD) : ")
    if starting_period != "" and ending_period != "" and starting_period < ending_period: #implementing a logic to avoid errors in inputs
        historique = ticker.history(start = starting_period, end = ending_period)
        if not historique.empty:
            break #break the loop created if no match
        else:
            print("Data not available, please retry") #error message if the dates don't fit in the observations
    else :
        print("Data not available, please retry") #retry to tap the period required

#csv file creating and cleaning
with open(f"{user_ticker}.csv", "w", newline="",encoding="utf-8") as csvfile : #f"{} custom file name with the ticker
    writer = csv.writer(csvfile) #create the file in CSV format

#Indicators for the CSV file columns
    writer.writerow([
        "Date",
        "Close",
        "Dividends",
    ])
    for date, ligne in historique.iterrows() : #import from yahoo finance data format to match with the previous write.row function
        writer.writerow([
            date.strftime("%Y-%m-%d"),
            ligne["Close"],
            ligne["Dividends"],
        ])
print(f"{user_ticker}.csv created") #.csv file created with the name customized according to the ticker selected

choice = "" #wait for users choice between Black-Scholes pricing option or go for a new round
while choice not in ["yes", "no"] :
    choice = input("insert yes for BlackSholes pricing option or no to select another ticker : ").lower()
    if choice == "yes": #Black-Scholes computing

#reading the CSV file to extract infos and computing
        df = pd.read_csv(f"{user_ticker}.csv", parse_dates=["Date"]) #read, sort and format by the users input
        """
        Price of a european call option according to the Black-Scholes Merton method
        S : actual stock price
        K : strike
        T : maturity in year (ex: 0.5= 6mois)
        r : risk free rate (ex: 0.03 =3%)
        sigma : annual volatility (ex: 0.2 =20%)
        q : annual dividend yield
        option_type : "call" or "put
            """
# We use data from the CSV file to compute
        log_returns = np.log(df["Close"] / df["Close"].shift(1)).dropna() #computing log returns and "shift(1)).dropna()" to start from the next line
        S = df["Close"].iloc[-1] #iloc[-1] 
        sigma=log_returns.std()*math.sqrt(252) #252 is the number of days traded in a year
        annees = (df["Date"].max() - df["Date"].min()).days / 365 #number of day in a year
        q = (df["Dividends"].sum() / annees) / S #integrating dividends into our engine

# "float" accept decimal numbers, "input" ask user to write
        K = float(input("Strike :"))
        T = float(input("Duration (ex : 0.5 = 6 months) :"))
        r = float(input("Risque free rate (ex : 0.03 for 3%) : "))

#we show the Stock price and the result for the option selected previously
        print(f"S = {S:.2f}")
        print(f"print call : {black_scholes(S, K, T, r, sigma, q, 'call'):.2f}")
        print(f"print put: {black_scholes(S, K, T, r, sigma, q, 'put'):.2f}")

#2nd round if no Black-Scholes option pricing selected, select another ticker for CSV file
    elif choice == "no":
        print("Select another ticker")
    else:
        print("Please choose between BlackSholes pricing option or select another ticker")

#If we have a targeted price for a call option
def strike_for_call(targeted_price, S, T, r, sigma, q=0.0, tolerance=0.01):
    """
    Find the Strike K as the call price equal the targeted price defined by the user (bissection method).
    The call price decrease when K increase, we reduce the research interval at each round.
    """
    if not 0 < targeted_price < S:
        raise ValueError("The targeted price should be located between 0 and the stock price") #error message if the inputs are unreal

    K_low = 0.01   #very low Strike price, near 0
    K_high = 10 * S  #high Strike, call near 0

    while K_high - K_low > tolerance: #while the interval is higher than the tolerance we continue to cut it in half
        K_middle = (K_low + K_high) / 2
        middle_price = black_scholes(S, K_middle, T, r, sigma, q, "call")

        if middle_price > targeted_price:
            K_low = K_middle   #call price too high, we need a higher Strike
        else:
            K_high = K_middle  #call price too low, we need a lower Strike

    return (K_low + K_high) / 2
targeted_price = float(input("Targeted price of the Call : ")) #The user select its targeted price for the call
K_found = strike_for_call(targeted_price, S, T, r, sigma, q)
print(f"Strike : {K_found:.2f}")