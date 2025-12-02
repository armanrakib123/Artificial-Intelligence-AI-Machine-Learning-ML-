import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_PATH = "sales.csv"
if not os.path.exists(CSV_PATH):
    raise SystemExit(f"ফাইল পাওয়া যায়নি: {CSV_PATH} -> sales.csv তৈরি করে এরকম কলাম রাখো: Date,Product,Price,Quantity")

df = pd.read_csv(CSV_PATH, parse_dates=["Date"])


df["Total"] = df["Price"] * df["Quantity"]

daily = df.groupby(df["Date"].dt.date)["Total"].sum().reset_index()
daily.columns = ["Date", "DailyTotal"]
print("\n=== দৈনিক মোট বিক্রয় ===")
print(daily.to_string(index=False))


product_summary = df.groupby("Product").agg(
    TotalQuantity = ("Quantity", "sum"),
    TotalRevenue = ("Total", "sum")
).sort_values("TotalRevenue", ascending=False).reset_index()
print("\n=== পণ্যের সারাংশ ===")
print(product_summary.to_string(index=False))


df["YearMonth"] = df["Date"].dt.to_period("M")
monthly = df.groupby("YearMonth")["Total"].sum().reset_index()
monthly["YearMonth"] = monthly["YearMonth"].astype(str)
monthly.columns = ["YearMonth", "MonthlyTotal"]
print("\n=== মাসিক মোট আয় ===")
print(monthly.to_string(index=False))


top_product = product_summary.iloc[0]
print(f"\nTop Product: {top_product['Product']}  |  Revenue: {top_product['TotalRevenue']}  |  Quantity: {top_product['TotalQuantity']}")


plt.figure(figsize=(8,4))
plt.plot(daily["Date"], daily["DailyTotal"], marker='o')
plt.title("Daily Sales")
plt.xlabel("Date")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("daily_sales.png")
print("\nDaily sales graph saved as daily_sales.png")

plt.figure(figsize=(8,4))
plt.bar(monthly["YearMonth"], monthly["MonthlyTotal"])
plt.title("Monthly Sales")
plt.xlabel("Year-Month")
plt.ylabel("Amount")
plt.tight_layout()
plt.savefig("monthly_sales.png")
print("Monthly sales graph saved as monthly_sales.png")
