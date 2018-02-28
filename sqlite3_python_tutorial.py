import sqlite3
import time
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style

style.use('fivethirtyeight')


# Note: In SQLite3, there are only 5 date types: NULL, INTEGER, REAL, TEXT, BLOB


# If SQLite tries to connect to a DB that doesn't exist, it
# will just create that DB. Here 'tutorial' does not yet exist
connection = sqlite3.connect('tutorial.db')
cursor = connection.cursor()
add_rows = True


def create_table():
    """Create embedded database"""
    cursor.execute("CREATE TABLE IF NOT EXISTS dataToPlot(unix REAL, datestamp TEXT, keyword TEXT, value REAL)")


def static_data_entry():
    """Statically creates a row in the database"""
    cursor.execute("INSERT INTO dataToPlot VALUES (1234, '2018-02-2018', 'Python', 3)")
    connection.commit()


def dynamic_data_entry():
    """Dynamically creates a row in the database"""
    unix = time.time()
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
    keyword = 'Python'
    value = random.randrange(0,10)
    cursor.execute("INSERT INTO dataToPlot (unix, datestamp, keyword, value) VALUES (?, ?, ?, ?)", 
        (unix, date, keyword, value))
    connection.commit()


def read_from_db():
    """Reads rows from database"""
    cursor.execute("SELECT keyword, unix FROM dataToPlot WHERE value=3.0 AND keyword='Python'")
    data = cursor.fetchall()

    # Iterate through each row, where a row is a tuple, so can index (E.g. row[0]) 
    for row in data:
        print(row)


def graph_data():
    """Graphs queried rows of data"""

    # Query the database
    cursor.execute("SELECT unix, value FROM dataToPlot")
    data = cursor.fetchall()

    # Extract data
    dates = []
    values = []
    for row in data:
        dates.append(datetime.datetime.fromtimestamp(row[0]))
        values.append(row[1])

    # Plot the graph
    plt.plot_date(dates, values, '-')
    plt.show()




# Main program
if __name__ == "__main__":

    # Create the database
    create_table()

    # Add extra rows if wanted
    if add_rows:
        for _ in range(10):
            dynamic_data_entry()
            time.sleep(1)

    # Query and read rows from database
    read_from_db()

    # Plot a simple graph
    graph_data()

    # Close the connection
    cursor.close()
    connection.close()

