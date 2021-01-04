import sqlite3


__searchable__ = ['upload', 'sdgs', 'entered_by', 'department']
conn = sqlite3.connect('database.db')
print ("Opened database successfully")

#conn.execute('CREATE TABLE data_table (date DATE, title TEXT, about TEXT, sdgs TEXT, upload BOOLEAN, name TEXT,data BLOP)')
conn.execute('CREATE TABLE data_table_2 (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, entered_by TEXT, title TEXT, about TEXT, department TEXT,sdgs TEXT, upload BOOLEAN, name TEXT, new_string TEXT)')
print ("Table created successfully")
conn.close()