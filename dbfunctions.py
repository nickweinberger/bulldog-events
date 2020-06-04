import os
import requests
import re
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import sqlite3
from sqlite3 import Error
from datetime import datetime
# importing datetime module
from datetime import *

#stores events.db into a variable for dynamic manipulation
database = "events.db"


#function that creates connection to database given a database file
def create_connection(p_db_file):
    conn = None
    try:
        conn = sqlite3.connect(p_db_file)
    #if no connection established, prints the error
    except Error:
        print(Error)
    return conn

#function for adding things into database
def insert_event(date, time, description, location, t_link, Image, conv, Event_name):
    #creates the connection between database and code
    conn =create_connection(database)
    #cursor method: creates cursor, whereby sql can be executed, committed, and closed
    cur = conn.cursor()
    cur.execute("INSERT INTO Sports(Date, Time, Description, Location, Ticket_link, Image, conv_Event_date, Event_name) VALUES (?,?,?,?,?,?,?,?)", (date, time, description, location, t_link, Image, conv, Event_name))
    cur.close()
    conn.commit()
    conn.close()

def search_sports_events(p_search_str,typesearch):
    json_data = [];
    conn = create_connection(database)
    # bob mens
    cur = conn.cursor()
    sql_common_like_statement = "LIKE '%" + p_search_str + "%'"
    sql_query_1 = "SELECT * FROM Sports WHERE Event_name " + sql_common_like_statement + "OR Date "+ sql_common_like_statement + "OR Description "+ sql_common_like_statement
    if typesearch=='current':
      sql_query_1 = "SELECT * FROM Sports WHERE Date = DATE() and (Event_name " + sql_common_like_statement + "OR Date "+ sql_common_like_statement + "OR Description "+ sql_common_like_statement+")"
      #print(sql_query_1)
    if typesearch=='later':
      today = datetime.now().strftime('%Y-%m-%d')
      #sql_query_1 = "DATE(substr(Date,7,4)||'-'||substr(Date,4,2)||'-'||substr(Date,1,2))"
      sql_query_1 = "SELECT * FROM Sports WHERE Date >= DATE() and (Event_name " + sql_common_like_statement + "OR Date "+ sql_common_like_statement + "OR Description "+ sql_common_like_statement+")"
      #print(sql_query_1)
    cur.execute(sql_query_1)
    #gets the row description:
    #x[0] of description attribute of cursor returns just column names
    columns = [x[0] for x in cur.description]
    #print(columns)
    data = cur.fetchall()

    for row in data:
        #print(row)
        #appends into json_Data dict with key value pair of row and row_headers
        json_data.append(dict(zip(columns, row)))
    cur.close()
    conn.commit()
    conn.close()

    #print(json_data)
    return json_data;

def search_acapella_events(p_search_str,typesearch):
    json_data = [];
    conn = create_connection(database)
    cur = conn.cursor()
    sql_common_like_statement = "LIKE '%" + p_search_str + "%'"
    #add in the remaining fields more than just Event_name
    sql_query_1 = "SELECT * FROM Acapella WHERE Event_name " + sql_common_like_statement
    if typesearch=='current':
        #'Date="+datetime.now().strftime('%m/%d/%Y')+ and"
        sql_query_1 = "SELECT * FROM Acapella WHERE  Date = DATE() and (Event_name " + sql_common_like_statement + "OR Date "+ sql_common_like_statement+")"
    if typesearch=='later':
    # today = datetime.now().strftime('%Y-%m-%d')
        sql_query_1 = "SELECT * FROM Acapella WHERE Date >= DATE() and (Event_name " + sql_common_like_statement + "OR Date "+ sql_common_like_statement+")"
    cur.execute(sql_query_1)
    #gets the row description:
    #x[0] of description attribute of cursor returns just column names
    columns = [x[0] for x in cur.description]
    #print(columns)
    data = cur.fetchall()

    for row in data:
        #print(row)
        #appends into json_Data dict with key value pair of row and row_headers
        json_data.append(dict(zip(columns, row)))
    cur.close()
    conn.commit()
    conn.close()

    #print(json_data)
    return json_data;

def today_events(current):
    json_data = [];
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Sports WHERE Date = ?", (current,))
    columns = [x[0] for x in cur.description]
    data = cur.fetchall()

    for row in data:
        json_data.append(dict(zip(columns, row)))
    cur.close()
    conn.commit()
    conn.close()
    return json_data;

def search_comedy_events(p_string,typesearch):
    json_data = [];
    conn = create_connection(database)
    cur = conn.cursor()
    sql_query_1 = "SELECT * FROM Comedy WHERE Event_name LIKE '%" + p_string + "%'"
    if typesearch=='current':
        #Date="+datetime.now().strftime('%m/%d/%Y')+"  and
      sql_query_1="SELECT * FROM Comedy WHERE  (Event_name LIKE '%" + p_string + "%')"
    cur.execute(sql_query_1)
    columns = [x[0] for x in cur.description]
    data = cur.fetchall()

    for row in data:
        json_data.append(dict(zip(columns, row)))
    cur.close()
    conn.commit()
    conn.close()
    return json_data;

def dateLessThan(date1,date2):
   datetime1 = datetime.strptime(date1, '%Y/%m/%d')
   datetime2 = datetime.strptime(date2, '%Y/%m/%d')
   return datetime1 < datetime2

def search_theater_events(stri,typesearch):
    json_data = [];
    conn = create_connection(database)
    cur = conn.cursor()
    sql_query_1="SELECT * FROM Theater WHERE Event_name LIKE '%" + stri + "%'"
    if typesearch=='current':
        #Date="+datetime.now().strftime('%m/%d/%Y')+"  and
      sql_query_1="SELECT * FROM Theater WHERE  (Event_name LIKE '%" + stri + "%')"

    cur.execute(sql_query_1)
    columns = [x[0] for x in cur.description]
    data = cur.fetchall()

    for row in data:
        json_data.append(dict(zip(columns, row)))
    cur.close()
    conn.commit()
    conn.close()
    return json_data;

def get_all_events():
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Sports")
    data = cur.fetchall()
    #for row in data:
        #print(row)
    cur.close()
    conn.commit()
    conn.close()

def convert_date(List):
    if List[1] == 1:
        string = "Jan " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 2:
        string = "Feb " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 3:
        string = "Mar " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 4:
        string = "Apr " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 5:
        string = "May " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 6:
        string = "Jun " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 7:
        string = "Jul " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 8:
        string = "Aug " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 9:
        string = "Sep " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 10:
        string = "Oct " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 11:
        string = "Nov " +  str(List[2]) + ", " + str(List[0])
        return string
    if List[1] == 12:
        string = "Dec " +  str(List[2]) + ", " + str(List[0])
        return string

