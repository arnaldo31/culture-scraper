import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging
import traceback
import asyncio
import time
import aiohttp
import html
import re
import json
import codecs

today = datetime.today()
date_save = today.strftime("%Y-%m-%d")
logging.basicConfig(filename='scraper.log',level=logging.INFO,
                    encoding='utf-8',
                    format='%(asctime)s : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

save = []

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
}

def saving(savefile:list,filename:str):
    seen = []
    unique_list = []
    for item in savefile:
        text = '{}-{}-{}'.format(item['title'],item['address'],item['url'])
        if text not in seen:
            seen.append(text)
            unique_list.append(item)

    filename = filename
    with codecs.open(f'.\\savefiles\\{filename}.json', 'w', encoding='utf-8') as f:
        json.dump({'posts': unique_list}, f, ensure_ascii=False, indent=4)

    
async def get_page(session,url):

    if Proy_activate == True:
        proxy_url = f"http://{PROXY['username']}:{PROXY['password']}@{PROXY['IP']}"
        async with session.get(url,proxy=proxy_url) as r:
            r.encoding = 'utf-8'
            return await r.text()
    else:
        async with session.get(url) as r:
            r.encoding = 'utf-8'
            return await r.text()
        
async def get_all(session,urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session,url))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return results

async def main(urls):

    while True:
        try:
            timeout = aiohttp.ClientTimeout(total=50)
            async with aiohttp.ClientSession(timeout=timeout,headers=headers) as session:
                data = await get_all(session,urls)
                return data
        except asyncio.TimeoutError:
            error_msg = 'Request timed out'
            print(error_msg)
            time.sleep(5)
            continue
        except aiohttp.client.ClientConnectionError:
            error_msg = 'ClientConnectionError'
            print(error_msg)
            time.sleep(5)
            continue

month_mapping = {
    "Jan": "01", "Feb": "02", "Mar": "03",
    "Apr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Aug": "08", "Sep": "09",
    "Oct": "10", "Nov": "11", "Dec": "12",
    'June':'06','July':'07','Sept':'09',
    'January':'01',
    'February':'02',
    'March':'03',
    'April':'04',
    'May':'05',
    'August':'08',
    'September':'09',
    'October':'10',
    'November':'11',
    'December':'12'
}

def crawl():
    

    current_date = datetime.now()
    day_minus = (11 - current_date.month ) * 30

    final_date = current_date + timedelta(days=day_minus)
    
    username = PROXY['username']
    password = PROXY['password']
    proxy = PROXY['IP']
    proxies = {
    'http': f'http://{username}:{password}@{proxy}',
    'https': f'http://{username}:{password}@{proxy}'
    }
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    }
    
    
    session = requests.Session()
    if Proy_activate == True:
        session.proxies.update(proxies)
        
    session.headers.update(headers)
    current_day = str(current_date.day)
    current_month = str(current_date.month)
    current_year = str(current_date.year)
    
    final_day = str(final_date.day)
    final_month = str(final_date.month)
    final_year  = str(final_date.year)
    
    
    data = {
        "startnr": 0,
        "Area": "nearme",
        "nearmeradius": 2000,
        "ArrStartdato": f"{current_day}/{current_month} {current_year}",
        "ArrSlutdato": f"{final_day}/{final_month} {final_year}",
        "Genre": "Gastronomi",
        "periode": None,
        "callback": "naut.call.nautnext[1]"
    }
    

    response = session.get(
        'https://www.kultunaut.dk/perl/arrlist2/type-nynaut',
        params=data
    )
    
    if 'nautnext[0]' in response.text:
        pattern = r'\.nautnext\[0\]\((\{[\s\S]*?\})\);'
    if 'nautnext[1]' in response.text:
        pattern = r'\.nautnext\[1\]\((\{[\s\S]*?\})\);'
    
    match = re.search(pattern, response.text)
    match_data = json.loads(match.group(1))
    #pprint.pprint(match_data)

    total_pages = match_data['maxantal']    
    print(total_pages)
    for i in range(1,9999,12):
        data['startnr'] = i
        while True:
            try:
                response = session.get('https://www.kultunaut.dk/perl/arrlist2/type-nynaut',params=data,timeout=10)
            except requests.exceptions.Timeout:
                continue
            except requests.exceptions.ConnectionError:
                continue
            pattern = None
            if 'nautnext[0]' in response.text:
                pattern = r'\.nautnext\[0\]\((\{[\s\S]*?\})\);'
            if 'nautnext[1]' in response.text:
                pattern = r'\.nautnext\[1\]\((\{[\s\S]*?\})\);'
                
            response.encoding = 'utf-8'
            match = re.search(pattern, response.text)

            if match == None:
                print(response.url)
                continue
            
            break
        
        match_data = json.loads(match.group(1))
        soup = BeautifulSoup(match_data['html'],'lxml')
        cards = soup.select('a.product-content')

        if cards == []:
            break
        
        links = []
        for card in cards:
            links.append(card['href'])

        parse_page(links=links)

def translate(word):
    
    while True:
        params = {
            'q':word,
            'key':'AIzaSyBbAo3SShaeAiBAzYUdHEMc_-Oc_uL-wAg',
            'target':'en'
        }
        url = 'https://translation.googleapis.com/language/translate/v2'

        res = requests.post(url,params=params)
        
        data = res.json()
        error = data.get('error')
        if error != None:
            print('errorrrr')
            continue
        else:
            return data['data']['translations'][0]['translatedText']

def parse_page(links:list):

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(links))

    for data in results:

        soup = BeautifulSoup(data,'lxml')
        title = soup.find('meta', attrs={'property': 'og:title'})['content']
        image = soup.find('meta', attrs={'property': 'og:image'})['content']
        url = soup.find('meta',attrs={'property':'og:url'})['content']
        try:
            address = soup.find(class_='event-place').get_text('\n',strip=True)
        except:
            continue
        event_date = soup.find(class_='event-date').p.get_text(' ')
        translated_date = html.unescape(translate(word=event_date))
        
        if ',' in translated_date:
            if len(translated_date.split(',')) > 1:
                date_split = ''.join(translated_date.split(',')[:-1])
                if 'to' in date_split:
                    date_split = date_split.split('to ')[1]
                if 'and' in date_split:
                    date_split = date_split.split('and ')[1]
                date = ''.join(date_split).split(' ')
            else:
                date = translated_date.split(',')[0]
                date = date.split(' ')

            
            try:
                day = date[1]
                month = date[2]
                try:
                    month = month_mapping[month]
                except KeyError:
                    month = month_mapping[date[1]]
                    day = date[2]
                year = date[3]
            except:
                #print('error ---- ',url)
                continue
            
            timesplit = translated_date.split(',')[1]
            time = '00:00'
            try:
                if '-' in timesplit and 'at' not in timesplit:
                    time = timesplit.split('-')[0].strip()
                if '&' in timesplit:
                    time = timesplit.split('&')[0].strip()
                    if '.' in time:
                        time = time.replace('.',':')
                        if len(time.split(':')[0]) == 1:
                            time = '0'+time
                    else:
                        if len(time) == 1:
                            time =  '0' + time + ':00'
                if 'at' in timesplit and '-' in timesplit:
                    time = timesplit.split('at ')[1][:5].replace('-',':').replace('.',':')
                    time = time.split(':')[0] + ':00'
                if 'from' in timesplit and 'to' in timesplit:
                    time = timesplit.split('from ')[1][:5].replace('-',':').replace('.',':')
                if 'from' in timesplit and 'PM' in timesplit and ':' in timesplit:
                    time = timesplit.split('from ')[1].split('PM')[0].strip()
                    if len(time.split(':')[0]) == 1:
                        time = '0' + time
                if 'at' in timesplit and 'PM' in timesplit and ':' in timesplit:
                    time = timesplit.split('at ')[1].split('PM')[0].strip()
                    if len(time.split(':')[0]) == 1:
                        time = '0' + time
            except:
                pass
            
            date_str = f'{year}-{month}-{day}T{time}:00.000Z'
            try:
                Date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                continue

            
        else:
            date = translated_date.strip().split(' ')
            try:
                day = date[1]
                month = date[2]
                try:
                    month = month_mapping[month]
                except KeyError:
                    month = month_mapping[date[1]]
                    day = date[2]
                year = date[3]
            except:
                #print('error ---- ',url)
                continue
            
            time = '00:00'
            date_str = f'{year}-{month}-{day}T{time}:00.000Z'
            try:
                Date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            except:
                continue
        
        startDate = date_str
        endDate = date_str
        doorOpen = Date.strftime("%H:%M")
        try:
            description = soup.find(class_='event-description').get_text('\n',strip=True)
        except:
            description = ''

        routeplan = soup.find(class_='routeplan')
        lat = 56.09537115
        long = 9.75162625 
        if routeplan != None:
            href = routeplan['href'].split('?')[1].replace('daddr=','').strip().split(',')
            lat = float(href[0])
            long = float(href[1])
            
        dic = {
            "postType": "CULTURE", 
            "genre": "Gastronomy",
            "url": url,
            "title": title,
            "address": address,
            "openingHours": doorOpen,
            "body": description,
            "monthlySchedule": {
                "startDate": startDate, 
                "endDate": endDate 
            },
            "photos": [
                {
                "provider": image
                }
            ],
            "channel": "@public",
            "parent": "ROOT",
            "locationLatitude": lat,
            "locationLongitude": long
        }

        text = 'www.kultunaut.dk | ' + dic['title']
        print(text)
        title = ' completed - ' + dic['title']
        logging.info(title)
        save.append(dic)

PROXY = requests.get('https://raw.githubusercontent.com/arnaldo31/concerts-scraper/main/scrapers/proxy.json')
PROXY = PROXY.json()
Proy_activate = False

def run():
    
    filename = __file__.split('\\')[-1]
    logging.info("-" * 113)
    logging.info(f" Starting  - ({filename}) scraper")

    try:
        crawl()
        logging.info(f" completed - total: {len(save)}")
    except Exception as e:
        error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        logging.info("-" * 113)
        logging.error(f"An error occurred: (scrapers\\{filename})\n%s", error_message)
        logging.error("-" * 113)

    saving(savefile=save,filename=filename.replace('.py',''))
    return save
