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




Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR.
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
                        bypassing hacks that are Tesseract-specific.
