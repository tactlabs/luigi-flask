#run: python carAndztruck.py Toronto-local-scheduler --fileName toronto.txt
# python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/cars-trucks/search/cta
# python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/computers/search/sya


import subprocess

def tasks(url):
    # subprocess.run([ 'python', '-m', 'luigi', '--module', 'carAndTruck', 'Toronto', '--urlpath', url ])
    taskId = [] 
    subprocess.run(['python','carAndTruck.py','Toronto','--urlpath',url])
    with open('taskid1.txt', 'r') as fin:
        for line in fin:
            taskId.append(line.strip())
    return taskId
