import os
import sqlite3
import pandas as pd
from flask import Flask, flash, redirect, render_template, \
     request, url_for
#def get_db_connection():
#    conn = sqlite3.connect('YTD.db')
#    conn.row_factory = sqlite3.Row
#    return conn

#conn = sqlite3.connect('YTD.db')
#conn.row_factory = sqlite3.Row

def sql_query(query):
    #conn = get_db_connection()
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    print(rows)
    conn.close()
    return rows

def sql_edit_insert(query,var):
    #conn = get_db_connection()
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query,var)
    conn.commit()
    conn.close()

def sql_delete(query,var):
    #conn = get_db_connection()
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query,var)
    
    conn.commit()
    conn.close()

def sql_query2(query,var):
   #conn = get_db_connection()
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query,var)
    rows = cur.fetchall()
    print(rows)
    conn.close()
    return rows

def sql_query_search(query, var):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, var)
    
    rows = cur.fetchall()
    print(rows)
    return rows
    #conn.commit()
def sql_download(query,var):
    #conn = get_db_connection()
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query,var)
    rows = cur.fetchall()
    print(rows)
    conn.close()
    return rows

