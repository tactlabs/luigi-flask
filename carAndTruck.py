# run: python carAndztruck.py Toronto-local-scheduler --fileName toronto.txt
# python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/cars-trucks/search/cta
# python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/computers/search/sya


import luigi
import requests
from bs4 import BeautifulSoup
from luigi.format import UTF8
import os


STR_OUTPUT1         = 'out1'
STR_OUTPUT2         = 'out2'
HREFCOUNT_OUT1_FILE = 'toronto.txt'
HREFCOUNT_OUT2_FILE = 'taskid.txt'
TORONTO_OUT1_FILE   = 'result.csv'
TORONTO_OUT2_FILE   = 'taskid1.txt'

class HrefCount(luigi.Task):
    urlpath = luigi.Parameter()
    def requires(self):
        return []

    def output(self):
        return { STR_OUTPUT1 : luigi.LocalTarget(HREFCOUNT_OUT1_FILE), STR_OUTPUT2 : luigi.LocalTarget(HREFCOUNT_OUT2_FILE) }

    def run(self):
        with open(self.output()['out1'].path ,'w') as fout, open(self.output()['out2'].path ,'w') as ftask:
            ftask.write('{}\n'.format(self.task_id))
            response = requests.get(self.urlpath)
            if(response.status_code == 200):
                fout.write('{}\n'.format(self.urlpath))
                soup = BeautifulSoup (response.text, features="lxml")
                nextButton = soup.find('link', attrs={'rel': 'next'})
                if nextButton is not None:
                    href = nextButton.get('href')
                    print(href)
                totalcount = soup.find('span', attrs={'class': 'totalcount'})
                rangeto = soup.find('span', attrs={'class': 'rangeTo'})
                print('totalcount={}'.format(totalcount))
                print('rangeto={}'.format(rangeto))
                while int(rangeto.text) < int(totalcount.text):
                    if href is not None:
                        response = requests.get(href)
                        if(response.status_code == 200):
                            fout.write('{}\n'.format(href))
                            soup = BeautifulSoup (response.text, features="lxml")
                            rangeto = soup.find('span', attrs={'class': 'rangeTo'})
                            nextButton = soup.find('link', attrs={'rel': 'next'})
                            if nextButton is not None:
                                href = nextButton.get('href')
                            else:
                                href = None
                    else:
                        print(response)
                        break
                    continue


class Toronto(luigi.Task):
    urlpath = luigi.Parameter()
    def requires(self):
        return { 'in1' :HrefCount(self.urlpath) }

    def output(self):
        return { STR_OUTPUT1 : luigi.LocalTarget(TORONTO_OUT1_FILE, format=UTF8), STR_OUTPUT2 : luigi.LocalTarget(TORONTO_OUT2_FILE) }
    
    def run(self):
        with open(self.input()['in1']['out1'].path) as fin, open(self.input()['in1']['out2'].path) as fintask, open(self.output()['out1'].path ,'w') as fout, open(self.output()['out2'].path ,'w') as ftask:
            for lin in fintask:
                taskId = lin.strip()
                ftask.write('{}\n'.format(taskId))
            ftask.write('{}\n'.format(self.task_id))
            fintask.close()
            os.remove(self.input()['in1']['out2'].path)
            for line in fin:
                url = line.strip()
                responseData = requests.get(url)
                if(responseData.status_code == 200):
                    bsoup = BeautifulSoup (responseData.text, features="lxml")
                    ul = bsoup.find('ul', attrs={'class': 'rows'})
                    li = ul.find_all('li')
                    for litag in li:
                        try:
                            ptag = litag.find('p')
                            atag = ptag.find('a')
                            link = atag.get('href')
                            title = str(atag.contents[0]).strip()
                            price = ptag.find("span", attrs={'class': 'result-price'})
                            if price is not None:
                                price = price.text.strip()
                            location = ptag.find("span", attrs={'class': 'result-hood'})
                            if location is not None:
                                location = location.text.strip()
                                location = location[1:-1]
                            fout.write('{} | {} | {} | {}\n'.format(link,title,price,location))
                        except Exception as e:
                            print (e)
            fin.close()
            os.remove(self.input()['in1']['out1'].path)


if __name__ == '__main__':
    luigi.run()
    


