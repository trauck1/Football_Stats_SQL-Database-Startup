import mysql.connector
from bs4 import BeautifulSoup
import requests

#finds they type of stats being recorded to name the table
def tableHeaderFunc(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tableHeaderLine = soup.find('h2', {'class', 'nfl-c-content-header__roofline' })
    return (tableHeaderLine.text)

#finds all the statistical categories being recorded 
def categoryListFunc(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    categoriesHead = soup.find("thead")
    categoriesHead = categoriesHead.find('tr')
    categories = categoriesHead.find_all('th', {'class', 'header'})
    #list of all the categories
    categoriesList =[]
    for category in categories:
        categoriesList.append(category.text)
    return categoriesList

def createTable(tableName):
    tableCreation = f"CREATE TABLE {tableHeader} (  `Player` varchar(255))"
    cursor.execute(tableCreation)

def grabnAddData(url, categories, title):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", {'class', 'd3-o-table d3-o-table--detailed d3-o-player-stats--detailed d3-o-table--sortable'})
    table = table.find('tbody')
    rows = table.find_all('tr')
    for row in rows:
        statList = []
        individualStats = row.find_all('td')
        addRowStatement = f"INSERT INTO {title} ("
        valueStatement = f"VALUES ("
        for i in range(len(categories)):
            addRowStatement = addRowStatement + categories[i]
            if(i == 0):
                individualStats[i] = removeComma(individualStats[i].text)
                valueStatement = valueStatement + "'" + remove_spaces(str(individualStats[i])) + "'"
            else:    
                valueStatement = valueStatement + remove_spaces(str(individualStats[i].text))
            if((i+1) != len(categories)):
                addRowStatement = addRowStatement + ','
                valueStatement = valueStatement + ','
            else:
                addRowStatement = addRowStatement + ')'
                valueStatement = valueStatement + ')'
        totalStatement = addRowStatement + valueStatement
        totalStatement = removeLine(totalStatement)
        print(totalStatement)
        cursor.execute(totalStatement)
def remove_spaces(s):
    return s.replace(" ", "")

def removeComma(s):
    return s.replace("'", "")
def removeLine(s):
    return s.replace("\n", " ")
def categoryCleaner(n):
    n = n.replace('/','per')
    n = n.replace('%','Percent')
    n = n.replace('+','plus')
    n = n.replace('INT', 'interceptions')
    n = n.replace('Lng', "Longest")
    n = n.replace('-','_')
    n = n.replace('>A_M', '')
    return n

if __name__ == "__main__":
    urls = ["https://www.nfl.com/stats/player-stats/category/passing/2025/REG/all/passingyards/DESC",
    "https://www.nfl.com/stats/player-stats/category/rushing/2025/reg/all/rushingyards/desc",
    "https://www.nfl.com/stats/player-stats/category/receiving/2025/reg/all/receivingreceptions/desc",
    "https://www.nfl.com/stats/player-stats/category/fumbles/2025/REG/all/defensiveforcedfumble/DESC",
    "https://www.nfl.com/stats/player-stats/category/tackles/2025/reg/all/defensivecombinetackles/desc",
    "https://www.nfl.com/stats/player-stats/category/interceptions/2025/reg/all/defensiveinterceptions/desc",
    "https://www.nfl.com/stats/player-stats/category/kickoffs/2025/reg/all/kickofftotal/desc",
    "https://www.nfl.com/stats/player-stats/category/kickoff-returns/2025/reg/all/kickreturnsaverageyards/desc",
    "https://www.nfl.com/stats/player-stats/category/punts/2025/reg/all/puntingaverageyards/desc",
    "https://www.nfl.com/stats/player-stats/category/punt-returns/2025/reg/all/puntreturnsaverageyards/desc"]
    #connect to create the new database
    mydb = mysql.connector.connect(host = "127.0.0.1", 
                                user = "USER", 
                                passwd="PASSWD")
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE Football_Data;")
    cursor.execute("USE Football_Data;")
    for url in urls:
        tableHeader = tableHeaderFunc(url)
        tableHeader = remove_spaces(tableHeader)
        categoriesList = categoryListFunc(url)
        createTable(tableHeader)
        updatedCategoriesList = []
        for category in categoriesList:
            category = remove_spaces(category)
            category = categoryCleaner(category)
            updatedCategoriesList.append(category)
            addColumnStatement = f"ALTER TABLE {tableHeader} ADD COLUMN {category} DECIMAL (10,2) DEFAULT 0;"
            if category != 'Player':
                cursor.execute(addColumnStatement)
        grabnAddData(url, updatedCategoriesList, tableHeader)
    mydb.commit()
    cursor.close()
    mydb.close()
    
    
