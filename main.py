import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables (from .env file if it exists)
load_dotenv()

# --- 1. Database Configuration ---
# Use the DATABASE_URL environment variable, or fallback to the provided string
# In a real environment, you should use .env for security.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Vivek%40123@localhost:5432/crypto_project")
engine = create_engine(DATABASE_URL)

# --- 2. Data Extraction Function ---
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[{time.strftime('%H:%M:%S')}] API Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Connection Error: {e}")
        return None

# --- 3. Database Maintenance (Schema & Cleanup) ---
def run_maintenance():
    try:
        with engine.connect() as conn:
            # 1. Ensure 'image' column exists for logos if it doesn't already
            conn.execute(text("ALTER TABLE live_crypto_data ADD COLUMN IF NOT EXISTS image VARCHAR(255);"))
            # 2. Delete data older than 30 days to keep database fast
            conn.execute(text("DELETE FROM live_crypto_data WHERE last_updated < NOW() - INTERVAL '30 days'"))
            conn.commit()
    except Exception as e:
        print(f"Maintenance Error: {e}")

# --- 4. ETL Process ---
def run_pipeline():
    print(f"[{time.strftime('%H:%M:%S')}] Fetching market data...")
    raw_data = fetch_crypto_data()
    
    if raw_data:
        # Convert to DataFrame
        df = pd.DataFrame(raw_data)
        
        # 1. Select relevant columns (excluding API's last_updated)
        columns_to_keep = ['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume', 'image']
        df_cleaned = df[columns_to_keep].copy()
        
        # 2. Rename 'id' to 'coin_id' to match SQL table
        df_cleaned = df_cleaned.rename(columns={'id': 'coin_id'})

        # 3. SET LOCAL TIMESTAMP (Laptop Time)
        # We manually set this to capture exactly when the data was saved on your machine.
        df_cleaned['last_updated'] = pd.Timestamp.now().replace(microsecond=0)

        # 4. Push to PostgreSQL
        try:
            df_cleaned.to_sql('live_crypto_data', engine, if_exists='append', index=False)
            local_time = df_cleaned['last_updated'].iloc[0].strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{time.strftime('%H:%M:%S')}] SUCCESS: Data saved at {local_time} (Laptop Time)")
            
            # Run maintenance cleanup after successful update
            run_pipeline_maintenance = True # Just to keep a reference to it
            run_maintenance()
            
        except Exception as e:
            print(f"Database Error: {e}")

# --- 5. Main Loop (Runs every minute) ---
if __name__ == "__main__":
    print("-" * 50)
    print(f"🚀 CRYPTO PIPELINE STARTING (Local Time: {time.strftime('%Y-%m-%d %H:%M:%S')})")
    print("-" * 50)
    
    # Run maintenance once at startup
    run_maintenance()
    
    while True:
        try:
            run_pipeline()
        except Exception as e:
            print(f"General Error: {e}")
            
        print("Waiting 60 seconds (1 minute) for next update...")
        time.sleep(60)
