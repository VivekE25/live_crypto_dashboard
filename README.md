# 🚀 Live Crypto Market Intelligence Dashboard

![Dashboard Screenshot](Dashboard%20screenshot.png)

An automated end-to-end data pipeline that fetches live cryptocurrency market data, stores it in a PostgreSQL database, and visualizes it through a premium Power BI dashboard.

## 🏗️ Project Architecture
- **Data Extraction**: Python script utilizing the **CoinGecko API** to fetch real-time market data.
- **Processing**: **Pandas** for data cleaning and transformation (handling timestamps and metadata).
- **Storage**: **PostgreSQL** database for persistent time-series data storage.
- **Visualization**: **Power BI** dashboard connected via **DirectQuery** for real-time analytics.

## ✨ Key Features
- **Real-time Pipeline**: Automated updates every 60 seconds.
- **Market Analytics**: Track price changes, market cap, and volume for top cryptocurrencies.
- **Premium Design**: Dark-themed dashboard with neon accents, custom DAX measures for trend analysis, and dynamic icons.
- **Self-Maintaining**: Integrated SQL maintenance scripts to handle data cleanup.

## 🛠️ Technology Stack
- **Language**: Python 3.x
- **Database**: PostgreSQL
- **BI Tool**: Power BI Desktop
- **Libraries**: Pandas, SQLAlchemy, Requests

## 🚀 How to Run
1. **Database**: Execute `schema.sql` in your PostgreSQL instance.
2. **Environment**: Install dependencies using `pip install -r requirements.txt` and create a `.env` file with your `DATABASE_URL`.
3. **Pipeline**: Run `python main.py` to start the live data feed.
4. **Dashboard**: Open `Crypto_Dashboard.pbix` in Power BI and update the data source credentials.

---
*Created as part of a 4-month data engineering & analytics portfolio challenge.*
