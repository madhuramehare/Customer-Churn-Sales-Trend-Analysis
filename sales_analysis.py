
import pandas as pd
import matplotlib.pyplot as plt
import os

url = "https://raw.githubusercontent.com/plotly/datasets/master/superstore.csv"

df = pd.read_csv(url)

print("\n========== DATASET LOADED SUCCESSFULLY ==========")

print("\nFirst 5 Records:")
print(df.head())

print("\nDataset Information:")
df.info()

print("\nDataset Statistics:")
print(df.describe())

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

df = df.drop_duplicates()

df = df.dropna(subset=[
    "Order Date", "Customer ID", "Sales", "Segment"
])

df["Order Date"] = pd.to_datetime(
    df["Order Date"], errors="coerce"
)

df = df.dropna(subset=["Order Date"])

df["Sales"] = df["Sales"].fillna(0)
df["Profit"] = df["Profit"].fillna(0)
df["Quantity"] = df["Quantity"].fillna(0)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nCleaned Dataset Shape:", df.shape)

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month

df["Month_Name"] = df["Order Date"].dt.strftime("%B")

df["Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)

df["Weekday"] = df["Order Date"].dt.day_name()
df["Year_Month"] = df["Order Date"].dt.to_period("M")
df["Profit_Margin"] = (
    df["Profit"] / df["Sales"].replace(0, float("nan"))
) * 100

print("\nFeature Engineering Completed!")

print(df[[
    "Order Date", "Year", "Month",
    "Quarter", "Weekday", "Year_Month"
]].head())

segment_analysis = df.groupby("Segment").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Orders=("Order ID", "nunique"),
    Total_Customers=("Customer ID", "nunique")
).round(2)

print("\n========== CUSTOMER SEGMENT ANALYSIS ==========")
print(segment_analysis)

top_customers = df.groupby("Customer Name").agg(
    Total_Spending=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Orders=("Order ID", "nunique")
).sort_values(
    by="Total_Spending", ascending=False
).head(10).round(2)

print("\n========== TOP 10 CUSTOMERS ==========")
print(top_customers)

category_analysis = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Total_Quantity=("Quantity", "sum")
).round(2)

print("\n========== CATEGORY ANALYSIS ==========")
print(category_analysis)

pivot_table = pd.pivot_table(
    df,
    values="Sales",
    index="Segment",
    columns="Category",
    aggfunc="sum",
    fill_value=0
).round(2)

print("\n========== SEGMENT VS CATEGORY PIVOT TABLE ==========")
print(pivot_table)

monthly_sales = df.groupby("Year_Month").agg(
    Monthly_Revenue=("Sales", "sum"),
    Monthly_Profit=("Profit", "sum"),
    Total_Orders=("Order ID", "nunique")
).sort_index()

print("\n========== MONTHLY SALES TREND ==========")
print(monthly_sales)

monthly_sales["Revenue_Growth_Percentage"] = (
    monthly_sales["Monthly_Revenue"].pct_change() * 100
).round(2)

print("\n========== MONTHLY REVENUE GROWTH ==========")
print(monthly_sales)

quarterly_sales = df.groupby("Quarter").agg(
    Revenue=("Sales", "sum"),
    Profit=("Profit", "sum")
).round(2)

print("\n========== QUARTERLY SALES ==========")
print(quarterly_sales)
reference_date = df["Order Date"].max()

customer_activity = df.groupby("Customer ID").agg(
    Last_Order=("Order Date", "max"),
    Total_Spending=("Sales", "sum"),
    Total_Orders=("Order ID", "nunique")
)

customer_activity["Days_Inactive"] = (
    reference_date - customer_activity["Last_Order"]
).dt.days

customer_activity["Activity_Status"] = (
    customer_activity["Days_Inactive"]
    .apply(lambda x: "At Risk" if x > 90 else "Active")
)

print("\n========== CUSTOMER ACTIVITY ==========")
print(customer_activity.head(10))

print("\nCustomer Activity Summary:")
print(customer_activity["Activity_Status"].value_counts())

best_segment = segment_analysis["Total_Sales"].idxmax()

best_category = category_analysis["Total_Sales"].idxmax()

most_profitable_category = category_analysis[
    "Total_Profit"
].idxmax()

top_customer = top_customers.index[0]

at_risk_count = (
    customer_activity["Activity_Status"] == "At Risk"
).sum()

total_revenue = df["Sales"].sum()
total_profit = df["Profit"].sum()

print("\n========== BUSINESS RECOMMENDATIONS ==========")

print("1. Best Customer Segment:", best_segment)

print("2. Best Selling Category:", best_category)

print("3. Most Profitable Category:", most_profitable_category)

print("4. Top Customer:", top_customer)

print("5. Customers At Risk:", at_risk_count)

print("6. Total Revenue: Rs.", round(total_revenue, 2))

print("7. Total Profit: Rs.", round(total_profit, 2))

print("\nRECOMMENDATIONS:")

print("- Focus marketing on the highest-revenue customer segment.")

print("- Promote products from the best-selling category.")

print("- Study the most profitable category to improve profit.")

print("- Provide loyalty rewards to valuable customers.")

print("- Contact inactive customers with suitable offers.")

print("- Monitor monthly revenue growth to identify sales trends.")
os.makedirs("output", exist_ok=True)
df.to_csv("output/cleaned_sales_data.csv", index=False)

segment_analysis.to_csv("output/segment_analysis.csv")

top_customers.to_csv("output/top_customers.csv")

pivot_table.to_csv("output/sales_pivot_table.csv")

monthly_sales.to_csv("output/monthly_sales_trend.csv")

quarterly_sales.to_csv("output/quarterly_sales.csv")

customer_activity.to_csv("output/customer_activity.csv")

plt.figure(figsize=(12, 6))

monthly_sales["Monthly_Revenue"].plot(
    marker="o",
    color="blue",
    linewidth=2
)

plt.title("Monthly E-commerce Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("output/monthly_sales_chart.png")
plt.show()

plt.figure(figsize=(8, 5))

segment_analysis["Total_Sales"].plot(
    kind="bar",
    color=["skyblue", "orange", "green"]
)

plt.title("Sales by Customer Segment")
plt.xlabel("Customer Segment")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("output/customer_segment_chart.png")
plt.show()

print("\n======================================")
print("CUSTOMER SALES ANALYSIS COMPLETED!")
print("All reports saved in output folder.")
print("======================================")
