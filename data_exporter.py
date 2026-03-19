import pandas as pd
import json
import os

def export_summary_data():
    cleaned_file = "data/events_oct_cleaned.csv"
    rfm_file = "data/rfm_data.csv"
    
    if not os.path.exists(cleaned_file):
        print("Error: Cleaned data not found. Run analysis first.")
        return

    # Use usecols to speed up loading and reduce memory usage
    cols_needed = ['event_type', 'price', 'user_id', 'user_session', 'category_code']
    df = pd.read_csv(cleaned_file, usecols=cols_needed)
    rfm = pd.read_csv(rfm_file) if os.path.exists(rfm_file) else None
    
    # Add 'day' for daily revenue (we can extract from event_time if we don't have it, 
    # but the cleaning script adds it. Let's make sure it's there or calculate it.)
    # The cleaning script added 'day', 'hour', 'day_of_week'.
    # Let's reload with 'day' if it's there.
    
    # Try to get 'day' if available
    try:
        df_times = pd.read_csv(cleaned_file, usecols=['day'])
        df['day'] = df_times['day']
    except:
        # If not there, we'd need event_time, but let's assume it's there based on my reading of data_cleaning.py
        pass
    
    # 1. Base KPIs
    total_revenue = df[df['event_type'] == 'purchase']['price'].sum()
    total_users = df['user_id'].nunique()
    # Note: user_session might have NaNs in raw, but cleaning handles it.
    total_sessions = df['user_session'].nunique()
    total_orders = df[df['event_type'] == 'purchase']['user_session'].nunique()
    aov = total_revenue / total_orders if total_orders > 0 else 0
    cr = (total_orders / total_sessions * 100) if total_sessions > 0 else 0
    
    # 2. Daily Revenue for Sparkline
    daily_revenue = df[df['event_type'] == 'purchase'].groupby('day')['price'].sum().to_dict()
    
    # 3. Top Categories
    top_categories = df[df['event_type'] == 'purchase']['category_code'].value_counts().head(5).to_dict()
    if 'unknown' in top_categories: del top_categories['unknown']
    
    # 4. RFM Segment counts
    segment_counts = {}
    if rfm is not None:
        segment_counts = rfm['Segment'].value_counts().to_dict()
        
    summary = {
        "kpis": {
            "total_revenue": round(total_revenue, 2),
            "total_users": total_users,
            "total_orders": total_orders,
            "aov": round(aov, 2),
            "conversion_rate": round(cr, 2)
        },
        "daily_revenue": daily_revenue,
        "top_categories": top_categories,
        "segments": segment_counts
    }
    
    # Save to data/dashboard_data.json
    output_path = "data/dashboard_data.json"
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=4)
    
    print(f"Summary data exported to {output_path}")

if __name__ == "__main__":
    export_summary_data()
