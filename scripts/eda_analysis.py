import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda(input_file):
    print(f"Loading cleaned data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # Ensure visuals directory exists
    if not os.path.exists("visuals"):
        os.makedirs("visuals")
    
    print("--- Executive Summary ---")
    total_users = df['user_id'].nunique()
    total_revenue = df[df['event_type'] == 'purchase']['price'].sum()
    total_orders = df[df['event_type'] == 'purchase']['user_session'].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    print(f"Total Users: {total_users:,}")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Total Orders: {total_orders:,}")
    print(f"Average Order Value: ${avg_order_value:,.2f}")
    
    # 1. Sales Trends
    print("Generating sales trends...")
    daily_sales = df[df['event_type'] == 'purchase'].groupby('day')['price'].sum()
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=daily_sales.index, y=daily_sales.values, marker='o', color='#2ecc71')
    plt.title('Daily Revenue Trend - October 2019', fontsize=15)
    plt.xlabel('Day of Month')
    plt.ylabel('Revenue ($)')
    plt.grid(True, alpha=0.3)
    plt.savefig('visuals/revenue_trend.png')
    plt.close()
    
    # 2. Customer Type Distribution
    print("Generating customer insights...")
    customer_dist = df.drop_duplicates('user_id')['customer_type'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(customer_dist, labels=customer_dist.index, autopct='%1.1f%%', colors=['#3498db', '#e74c3c'], startangle=140)
    plt.title('Customer Type: New vs Returning', fontsize=15)
    plt.savefig('visuals/customer_type_dist.png')
    plt.close()
    
    # 3. Top Categories
    print("Generating product insights...")
    top_categories = df[df['event_type'] == 'purchase']['category_code'].value_counts().head(10)
    # Remove 'unknown' if it's there
    if 'unknown' in top_categories:
        top_categories = top_categories.drop('unknown')
        
    plt.figure(figsize=(12, 6))
    sns.barplot(x=top_categories.values, y=top_categories.index, palette='viridis')
    plt.title('Top 10 Product Categories by Sales Volume', fontsize=15)
    plt.xlabel('Number of Purchases')
    plt.savefig('visuals/top_categories.png')
    plt.close()
    
    print("EDA Complete. Visuals saved to 'visuals/' directory.")

if __name__ == "__main__":
    run_eda("data/events_oct_cleaned.csv")
