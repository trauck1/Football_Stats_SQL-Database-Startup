# Football_Stats_SQL-Database-Startup

NFL Stats Scraper & MySQL Loader

This project scrapes NFL player statistics from NFL.com
 using BeautifulSoup and loads the data into a structured MySQL database for further analysis.

It automatically:

-Creates a new database (Football_Data)

-Creates tables for different statistical categories (Passing, Rushing, Receiving, etc.)

-Cleans up column names and table headers

-Inserts player statistics directly into MySQL

Features

Scrapes NFL player stats from multiple categories (passing, rushing, receiving, fumbles, tackles, interceptions, kickoffs, kickoff returns, punting, punting returns).

Dynamically generates MySQL tables based on stat headers.

Cleans and normalizes column names (e.g., % → Percent, Lng → Longest).

Inserts all scraped data into MySQL for analysis or visualization.

Requirements

Python

MySQL Server (local or remote)

Python dependencies:

pip install mysql-connector-python beautifulsoup4 requests

Setup

Clone this repository:

git clone https://github.com/yourusername/nfl-stats-scraper.git
cd nfl-stats-scraper


Edit database credentials inside main.py:

mydb = mysql.connector.connect(
    host = "127.0.0.1", 
    user = "your_mysql_user", 
    passwd = "your_mysql_password"
)


Run the script:

python footballDatabaseStartup.py


The script will:

Create a database called Football_Data

Create a table for each stat category (Passing, Rushing, etc.)

Insert all player stats

 

Future Improvements

Add a table for field goal stats

Add all the stats, not just the first page 

Option to update existing tables instead of recreating.
