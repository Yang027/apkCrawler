'''
Project:自動化下載anzhi安卓手機商店中不同種類的top50 apk
Date:2022/11/20
Author:yang
'''
from clint.textui import progress
import requests
from bs4 import BeautifulSoup
import time
import requests
path="D:/apk" #path to save apk
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
# automatically download Top 50 apk from 10 category in anzhi.com
# without game apk
def anzhi_top50():   
    for ii in range(39,55):#39
        mainurl=f"http://www.anzhi.com"
        directurl=f'/sort_{ii}_1_hot.html'
        #print(appstore_map)
        response = requests.get(url=mainurl+directurl, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")         
        result = soup.find_all("div", class_="pagebars")
        hrefs=result[0].select("a")
        for href in hrefs:            
            response = requests.get(url=mainurl+href.get("href"), headers=headers)
            while response.status_code != 200:
                response = requests.get(url=mainurl+href.get("href"), headers=headers)
                time.sleep(2) #let it load  
            print(mainurl+href.get("href"))             
            #t = threading.Thread(target=download_page, args=(response,))
            download_page(response)
            #t.start() 
            #time.sleep(1)
        #download link:http://www.anzhi.com/ajaxdl_app.php?s={id}
def download(_url,name):
    try:       
        response = requests.get(_url,stream=True)        
        with open(f'{path}/{name}.apk', mode='wb') as f:
            total_length = int(response.headers.get('content-length'))
            for chunk in progress.bar(response.iter_content(chunk_size=1024), label="download:"+name,expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
        time.sleep(1)
    except Exception as e:
        print(e)
        pass

def download_page(_response):
    soup = BeautifulSoup(_response.text, "html.parser")
    result = soup.find_all("div", class_="app_list border_three")
    for jj in result:
        appname=[]
        for app in jj.select("div.app_info"):
            appname.append(app.select_one("span.app_name"))
        ii=0
        for links in jj.select("div.app_down"):
            ll=str(links.select_one('a'))
            link=ll.split("opendown(")[1].split(")")[0]
            download_link=f'http://www.anzhi.com/dl_app.php?s={link}&n=5'
            download(download_link,appname[ii].getText())
            ii+=1

if __name__=='__main__':
    anzhi_top50()