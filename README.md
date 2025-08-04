# 🧮 Real-Time Stock Trading Engine

This is a multithreaded, real-time **stock trading engine** written in Python. It simulates a simplified version of an exchange’s order matching engine and was developed as a response to a real-world systems challenge from Onymos.

The engine handles concurrent Buy and Sell orders across 1,024 tickers and matches them based on price-time priority. It avoids the use of dictionaries, maps, or external data structures and operates under lock-free multithreaded conditions.

## 🚀 Features

- ⚖️ **Price-Time Priority Matching**: Ensures that orders are matched based on price competitiveness and arrival time.
- 🧵 **Multithreaded Simulation**: Order producers and the matcher run in parallel to simulate real-world broker behavior.
- 🔐 **Lock-Free Design**: Avoids traditional locking mechanisms while maintaining data consistency across threads.
- 📊 **O(n) Matching Algorithm**: Matches orders efficiently in linear time with respect to the number of active orders per ticker.
- 📦 **No Built-in Data Structures**: Fulfills constraints by not using dictionaries, maps, or similar constructs.

## 🛠 Technologies

- Python (threading, time)
- Custom list-based data structures
- CLI-based simulation

## 🧪 How to Run

```bash
python trading_engine.py
