#run: python carAndztruck.py Toronto-local-scheduler --fileName toronto.txt
# python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/cars-trucks/search/cta
# python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/computers/search/sya


import subprocess
import os
import sqlite3

def tasks(url):
    # subprocess.run([ 'python', '-m', 'luigi', '--module', 'carAndTruck', 'Toronto', '--urlpath', url ])
    taskId = ''
    subprocess.run(['python','carAndTruck.py','Toronto','--urlpath',url])
    with open('taskid1.txt', 'r') as fin:
        for line in fin:
            taskId = line.strip()
    return taskId

def imageTask(limit, imagePath, database):
    if(os.path.exists('urls.txt')):
        os.remove('urls.txt')
    if (limit>25):
        subprocess.run(['python', 'avatar.py', 'ImageContent', '--limit',str(limit), '--imagepath',imagePath])
    else:
        subprocess.run(['python', 'avatar.py', 'ImageContent', '--imagepath',imagePath])
    if(os.path.isfile('urls.txt')):
        records = []
        with open('urls.txt', 'r') as fin:
            for line in fin:
                tup = (line.strip(),)
                records.append(tup)
        print(records)
    return records
        


