import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def run_behavior_analysis(input_file):
    print(f"Loading data for behavior analysis from {input_file}...")
    df = pd.read_csv(input_file)
    
    # 1. Conversion Funnel: View -> Cart -> Purchase
    print("Building conversion funnel...")
    funnel_counts = df['event_type'].value_counts()
    
    # Define funnel steps explicitly
    steps = ['view', 'cart', 'purchase']
    # Filter only those that exist in our steps
    values = [funnel_counts.get(step, 0) for step in steps]
    
    funnel_df = pd.DataFrame({'step': steps, 'count': values})
    funnel_df['retention'] = funnel_df['count'] / funnel_df['count'].shift(1)
    funnel_df['drop_off'] = 1 - funnel_df['retention']
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='count', y='step', data=funnel_df, palette='Reds_r')
    for i, v in enumerate(funnel_df['count']):
        plt.text(v + 1000, i, f"{v:,}", color='black', va='center', fontweight='bold')
    plt.title('Conversion Funnel: View -> Cart -> Purchase', fontsize=15)
    plt.savefig('visuals/conversion_funnel.png')
    plt.close()
    
    # 2. Activity Heatmap (Hour vs Day of Week)
    print("Generating activity heatmap...")
    # Map back to day names for better visual
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = df.groupby(['day_of_week', 'hour']).size().unstack().reindex(day_order)
    
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False)
    plt.title('Activity Heatmap: Day vs Hour', fontsize=15)
    plt.savefig('visuals/activity_heatmap.png')
    plt.close()
    
    # 3. Session Duration vs Purchase Probability
    print("Analyzing session duration...")
    # We need session-level data
    sessions = df.groupby('user_session').agg({
        'session_duration': 'first',
        'event_type': lambda x: 'purchase' in x.values
    }).rename(columns={'event_type': 'is_purchaser'})
    
    # Binning duration
    sessions['duration_bin'] = pd.cut(sessions['session_duration'], bins=[0, 60, 300, 600, 1800, 3600, np.inf], 
                                      labels=['<1m', '1-5m', '5-10m', '10-30m', '30-60m', '1h+'])
    
    duration_purchase = sessions.groupby('duration_bin', observed=True)['is_purchaser'].mean()
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=duration_purchase.index.astype(str), y=duration_purchase.values, marker='o', color='#8e44ad')
    plt.title('Purchase Probability by Session Duration', fontsize=15)
    plt.ylabel('Conversion Rate')
    plt.xlabel('Session Duration')
    plt.savefig('visuals/duration_vs_conversion.png')
    plt.close()

    print("Behavior analysis complete. Visuals saved to 'visuals/'.")

if __name__ == "__main__":
    run_behavior_analysis("data/events_oct_cleaned.csv")
