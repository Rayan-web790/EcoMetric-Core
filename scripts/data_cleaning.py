import pandas as pd
import numpy as np
import os

def clean_data(input_file, output_file):
    print(f"Loading data from {input_file}...")
    # Loading 1 million rows first for a quick prototype, then we can run on full if needed
    # The full file is ~460MB, manageable in memory (16GB RAM likely)
    df = pd.read_csv(input_file)
    
    print("Initial Data Shape:", df.shape)
    
    # 1. Clean Missing Values
    # category_code and brand have many NaNs. We'll mark them as 'unknown'
    df['category_code'] = df['category_code'].fillna('unknown')
    df['brand'] = df['brand'].fillna('unknown')
    
    # event_type mapping (optional but helps)
    # 2. Fix Data Types
    df['event_time'] = pd.to_datetime(df['event_time']).dt.tz_localize(None) # Remove UTC for easier handling
    
    # 3. Remove duplicates
    df = df.drop_duplicates()
    
    # 4. Feature Engineering
    print("Performing feature engineering...")
    
    # Sort by user and time
    df = df.sort_values(['user_id', 'event_time'])
    
    # session duration: max(time) - min(time) per user_session
    session_times = df.groupby('user_session')['event_time'].agg(['min', 'max'])
    session_times['session_duration'] = (session_times['max'] - session_times['min']).dt.total_seconds()
    
    # Join back to main dataframe
    df = df.merge(session_times[['session_duration']], on='user_session', how='left')
    
    # Join back or keep separate for session analysis
    # For now, let's keep the event-level data and add order_value where applicable
    
    # Order Value (Sum of price for 'purchase' events in a session)
    # In this dataset, often multiple items are purchased in one session
    purchases = df[df['event_type'] == 'purchase'].copy()
    order_values = purchases.groupby('user_session')['price'].sum().rename('order_value')
    
    # Merge order values back (optional, but good for session level)
    
    # New vs Returning Customer
    # We define 'returning' if user has events on different days or multiple sessions
    # (Simplified for this 1-month dataset)
    user_sessions_count = df.groupby('user_id')['user_session'].nunique().rename('session_count')
    df = df.merge(user_sessions_count, on='user_id', how='left')
    df['customer_type'] = np.where(df['session_count'] > 1, 'Returning', 'New')
    
    # Time Features
    df['hour'] = df['event_time'].dt.hour
    df['day_of_week'] = df['event_time'].dt.day_name()
    df['day'] = df['event_time'].dt.day
    
    print("Cleaned Data Shape:", df.shape)
    
    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

if __name__ == "__main__":
    input_path = "data/events_2019_oct.csv"
    output_path = "data/events_oct_cleaned.csv"
    
    if not os.path.exists("data"):
        os.makedirs("data")
        
    clean_data(input_path, output_path)
