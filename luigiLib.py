#run: python carAndztruck.py Toronto-local-scheduler --fileName toronto.txt
# python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/cars-trucks/search/cta
# python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/computers/search/sya


import subprocess

def tasks(url):
    # subprocess.run([ 'python', '-m', 'luigi', '--module', 'carAndTruck', 'Toronto', '--urlpath', url ]) 
    subprocess.run(['python','carAndTruck.py','Toronto','--urlpath',url])
    return 'Hello'
