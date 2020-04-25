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
import os
import random, string
from flask import send_file


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")
image_path = os.path.join(BASE_DIR, "static\\images\\")
file_path = os.path.join(BASE_DIR, "result.csv")
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

@app.route('/trigger', methods=['POST','GET'])
def trigger():
    if request.method == 'POST':
        data = request.form.get("url")
        taskId = luigiLib.tasks(data)
        status = 'FAILURE'
        result_file_path = ''
        task_status = 'FAILURE'
        fileName = 'result.csv'
        if(len(taskId)>0):
            try:
                conn = sqlite3.connect(db_path)
                task_select_sql = ''' SELECT * FROM tasks WHERE task_id  = :taskId '''
                events_select_sql = ''' SELECT * FROM task_events WHERE task_id  = :taskId '''
                task_select_obj = {
                            'taskId' : taskId
                        }
                cur = conn.cursor()
                cur.execute(task_select_sql, task_select_obj)
                rows = cur.fetchall()
                print(len(rows))
                for row in rows:
                    filterId = row[0]
                    events_select_obj = {
                            'taskId' : int(filterId)
                        }
                    cur.execute(events_select_sql, events_select_obj)
                    eventrows = cur.fetchall()
                    print(len(eventrows))
                    for eventrow in eventrows:
                        status = eventrow[2]
                        if (status == 'DONE'):
                            task_status = 'SUCCESS'
                            if(len(taskId)>0):
                                tasks = taskId.split('__')
                            if(os.path.exists(file_path)):
                                result_file_path = os.path.join(BASE_DIR, 'result_{}.csv'.format(tasks[2]))
                                destFile = tasks[2]
                                if(os.path.exists(result_file_path)):
                                    destFile = randomword(12)
                                print(destFile)
                                os.rename('result.csv', 'result_{}.csv'.format(destFile))
                            else:
                                print('error')
            except Exception as e:
                print(e)
                if(os.path.exists(file_path)):
                    destFile = randomword(12)
                    print(destFile)
                    os.rename('result.csv', 'result_{}.csv'.format(destFile))
                    status = 'DONE'
                    task_status='SUCCESS'
                else:
                    print('failure of tasks')
        else:
            if(os.path.exists(file_path)):
                destFile = randomword(12)
                os.rename('result.csv', 'result_{}.csv'.format(destFile))
                result_file_path = os.path.join(BASE_DIR, 'result_{}.csv'.format(destFile))
                fileName = 'result_{}.csv'.format(destFile)
                status = 'DONE'
                task_status='SUCCESS'
        return render_template('table_single.html', url=data, status=status, task_status=task_status, file_path=fileName)

# @app.route('/download/<fileName>')
# def getcsvfile():
#     try:
#         with open('{}'.format(fileName)) as f:
#             return send_file(f, mimetype='text/csv')
#     except OSError:
#         print('404')

@app.route('/triggerImage')
def getImage():
    try:
        fileName = 'imagespath.csv'
        newfileName = ''
        records = luigiLib.imageTask(0, image_path, db_path)
        try:
            conn = create_connection(db_path)
            print('Query')
            cur = conn.cursor()
            cur.executemany('INSERT INTO imagetasks(url) VALUES (?)',records)
            conn.commit()
            print(cur.rowcount)
            print('commited')
            task_select_sql = ''' SELECT * FROM imagetasks '''
            cur.execute(task_select_sql)
            rows = cur.fetchall()
            print(len(rows))
            for row in rows:
                print(row)
            if(os.path.exists(fileName)):
                fileNameExt = randomword(10)
                newfileName = 'imagespath_{}.csv'.format(fileNameExt)
                os.rename(fileName, newfileName)
        except Exception as e:
            print(e)
        finally:
            conn.close()
    except Exception as e:
        print(e)
    
    return fileName

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

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
    #app.debug = True;1
    app.run('127.0.0.1', 4000, True)
