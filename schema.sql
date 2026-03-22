/* 
🚀 CRYPTO DASHBOARD - DATABASE SCHEMA SETUP 
This script creates the table and adds necessary columns for 
Real-Time Market Data and Power BI integration.
*/

-- 1. Create the Main Table (Base Schema)
CREATE TABLE IF NOT EXISTS live_crypto_data (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50),
    symbol VARCHAR(10),
    name VARCHAR(50),
    current_price DECIMAL,
    market_cap BIGINT,
    total_volume BIGINT,
    last_updated TIMESTAMP
);

-- 2. Add 'image' Column (For Coin Logos in Power BI)
ALTER TABLE live_crypto_data ADD COLUMN IF NOT EXISTS image VARCHAR(255);

-- 3. Add 'minute' Column (For Hour-over-hour Trends)
ALTER TABLE live_crypto_data ADD COLUMN IF NOT EXISTS minute INT;

-- 4. Maintenance Script (Runs via Python)
-- DELETE FROM live_crypto_data WHERE last_updated < NOW() - INTERVAL '30 days';
