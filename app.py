#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, url_for, request
import math
import requests
import sqlite3
import random
from sqlite3 import Error
import os.path
import luigiLib 
import subprocess
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")
database = "database"

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/', methods=['POST','GET'])
def index():

    req_json = request.get_json()
    # url = request.values.get('url')
    # if len(url) <= 0:
    #     return error_result({"msg":"Unable to find URL param"})

    return render_template('table_single.html')

@app.route('/trigger')
def trigger():
    taskId = luigiLib.tasks('https://toronto.craigslist.org/d/computers/search/sya')
    conn = sqlite3.connect(database)
    select_sql = ''' SELECT * FROM tasks WHERE task_id IN (%s) '''
    cur = conn.cursor()
    cur.execute(select_sql, taskId)
    return 'taskId'
    # return luigiLib.tasks('https://toronto.craigslist.org/d/computers/search/sya')



def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)  

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    #app.debug = True;
    app.run('127.0.0.1', '4000', True)
