#run: python carAndztruck.py Toronto-local-scheduler --fileName toronto.txt
# python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/cars-trucks/search/cta
# python carAndTruck.py Toronto --local-scheduler --urlpath https://toronto.craigslist.org/d/computers/search/sya


import luigi
import requests
from bs4 import BeautifulSoup
from luigi.format import UTF8

class HrefCount(luigi.Task):
    urlpath = luigi.Parameter()
    def requires(self):
        return []

    def output(self):
        return luigi.LocalTarget("toronto1.txt")

    def run(self):
        with self.output().open('w') as fout:
            response = requests.get(self.urlpath)
            if(response.status_code == 200):
                fout.write('{}\n'.format(self.urlpath))
                soup = BeautifulSoup (response.text, features="lxml")
                nextButton = soup.find('link', attrs={'rel': 'next'})
                href = nextButton.get('href')
                totalcount = soup.find('span', attrs={'class': 'totalcount'})
                rangeto = soup.find('span', attrs={'class': 'rangeTo'})
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
                        break
                    continue


class Toronto(luigi.Task):
    urlpath = luigi.Parameter()
    def requires(self):
        return [HrefCount(self.urlpath)]

    def output(self):
        return luigi.LocalTarget("carandtruck1.csv", format=UTF8)
    
    def run(self):
        with self.input()[0].open() as fin, self.output().open('w') as fout:
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


if __name__ == '__main__':
    luigi.run()


