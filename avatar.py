import luigi
import requests
import os
import random, string
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")


class FetchUrl(luigi.Task):
    urlDefault = 'https://avatars2.githubusercontent.com/u/'
    limit = luigi.IntParameter(default=25)
    def requires(self):
        return[]

    def output(self):
        return luigi.LocalTarget('urls.txt')

    def run(self):
        with self.output().open('w') as fout:
            isBreak = False
            conn = sqlite3.connect(db_path)
            task_select_sql = ''' SELECT url FROM imagetasks '''
            cur = conn.cursor()
            cur.execute(task_select_sql)
            rows = cur.fetchall()
            print(len(rows))
            for x in range(1, self.limit+1):
                num = random.randint(1, 64186191)
                url=self.urlDefault+str(num)
                if(len(rows)>0):
                    for row in rows:
                        if(str(url)==str(row[0])):
                            self.limit = self.limit + 1
                            print(self.limit)
                            isBreak = True
                            break
                if(isBreak):
                    print('Already existing url')
                    print(url)
                    isBreak = False
                    continue
                else:
                    rows.append(url)
                    print(len(rows))
                print(url)
                fout.write('{}\n'.format(url))
            

    class ImageContent(luigi.Task):
        limit = luigi.IntParameter(default=25)
        imagepath = luigi.Parameter()
        def requires(self):
            return[FetchUrl(self.limit)]

        def output(self):
            return luigi.LocalTarget('imagespath.csv')

        def run(self):
            with self.input()[0].open() as fin, self.output().open('w') as fout:
                print(self.imagepath)
                for line in fin:
                    url = line.strip()
                    response = requests.get(url)
                    letters = string.ascii_lowercase
                    fileName = ''.join(random.choice(letters) for i in range(12))
                    filePath = self.imagepath+fileName+'.png'
                    if(os.path.exists(filePath)):
                        fileName = ''.join(random.choice(letters) for i in range(14))
                        filePath = self.imagepath+fileName+'.png'
                        print(filePath)
                        file = open(filePath, "wb")
                        file.write(response.content)
                        file.close()
                        fout.write('{} | {}\n'.format(url, filePath))
                    else:
                        print(filePath)
                        file = open(filePath, "wb")
                        file.write(response.content)
                        file.close()
                        fout.write('{} | {}\n'.format(url, filePath))


if __name__ == '__main__':
    luigi.run()
    
