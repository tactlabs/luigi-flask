# luigi-flask

Simple Application to collect the data using luigi and parser will be beautifulsoup

To run:
pip install -r requirements.txt

open the seperate terminal and run the command : luigid

python app.py

to view: http://127.0.0.1:4000/

luigid -- Need to run in the seperate terminal
this will start the luigi scheduler globally and can view the UI part in : http://localhost:8082/

to run luigi seperately in local
python Module TaskName --local-scheduler --parameterName parameterValue

Example:
#python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/computers/search/sya

# Luigi Config
Local scheduler is used for development purpose, but for production we need the central scheduler
[core]
#default-scheduler can be an IP central scheduler
default-scheduler-host:localhost

if tasks needed to be store in DB

[scheduler]
#this was store the record of past task details, else it is discard either
#after the frequent luigi task refresh or when luigi daemon is shutdown
record_task_history = True

[task_history]
#if we want to store the history in a DB
db_connection = sqlite:////home/baskaran/baskaran/teamtact/workspace/postclick/luigi-flask/database.db

db-connection property should be updated with ypur path, here luigi will craete the table automatically and store the task history
