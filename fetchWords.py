# Fetch words from the dataset
import sqlite3 as SQL
import logging
import pandas as pd
logging.basicConfig(level=logging.DEBUG, filename='logs.log')

# SQL Connector
try:
    conn = SQL.connect(r'data\dictionary.db')
    db = conn.cursor()
    db.execute('SELECT * FROM entries')
except:
    logging.error("Error connecting to database")
    exit()
output = db.fetchall()
output = list(set(output))
db.close()

# Stash all words in a data pickle
try:
    df = pd.DataFrame(output, columns=['word', 'type', 'definition'])
    df.to_pickle('data\words.pkl')
except:
    logging.error("Error writing to pickle")
    exit()

logging.info("Words fetched")
logging.info(f"Found {len(output)} words")