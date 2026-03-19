import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_rfm_analysis(input_file):
    print(f"Loading data for RFM analysis from {input_file}...")
    df = pd.read_csv(input_file)
    df['event_time'] = pd.to_datetime(df['event_time'])
    
    # We only care about purchases for RFM
    purchases = df[df['event_type'] == 'purchase'].copy()
    
    # 1. Recency: Days since last purchase (relative to max date in dataset)
    snapshot_date = df['event_time'].max()
    
    rfm = purchases.groupby('user_id').agg({
        'event_time': lambda x: (snapshot_date - x.max()).days,
        'user_session': 'nunique',
        'price': 'sum'
    })
    
    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    
    # 2. Assign Scores (1-5, 5 being best)
    # Recency: lower is better (5 point for min recency)
    rfm['R_Score'] = pd.qcut(rfm['Recency'].rank(method='first'), 5, labels=[5, 4, 3, 2, 1])
    # Frequency: higher is better
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    # Monetary: higher is better
    rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    
    # Calculate Total Score
    rfm['RFM_Score'] = rfm['R_Score'].astype(int) + rfm['F_Score'].astype(int) + rfm['M_Score'].astype(int)
    
    # 3. Label Segments
    def segment_customer(row):
        score = row['RFM_Score']
        if score >= 13: return 'VIP / Champions'
        if score >= 10: return 'Loyal Customers'
        if score >= 7: return 'Potential Loyalists'
        if score >= 4: return 'At Risk / Hibernating'
        return 'Lost Customers'
    
    rfm['Segment'] = rfm.apply(segment_customer, axis=1)
    
    # 4. Save and Visualize
    print("Generating RFM visuals...")
    segment_counts = rfm['Segment'].value_counts()
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=segment_counts.values, y=segment_counts.index, palette='magma')
    plt.title('Customer Segments by RFM Score', fontsize=15)
    plt.xlabel('Number of Customers')
    plt.savefig('visuals/rfm_segments.png')
    plt.close()
    
    # Revenue Contribution by Segment
    segment_revenue = rfm.groupby('Segment')['Monetary'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x=segment_revenue.values, y=segment_revenue.index, palette='coolwarm')
    plt.title('Revenue Contribution by Customer Segment', fontsize=15)
    plt.xlabel('Total Revenue ($)')
    plt.savefig('visuals/revenue_by_segment.png')
    plt.close()
    
    print("RFM Analysis Complete. Visuals saved to 'visuals/'.")
    # Save RFM data for possible LTV calculation in report
    rfm.to_csv('data/rfm_data.csv')

if __name__ == "__main__":
    run_rfm_analysis("data/events_oct_cleaned.csv")
