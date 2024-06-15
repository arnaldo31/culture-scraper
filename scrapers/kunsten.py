import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import logging
import traceback
import pprint
import aiohttp
import asyncio
import time

today = datetime.today()
date_save = today.strftime("%Y-%m-%d")
logging.basicConfig(filename='scraper.log',level=logging.INFO,
                    encoding='utf-8',
                    format='%(asctime)s : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

save = []

month_mapping = {
    "Jan": "01", "Feb": "02", "Mar": "03",
    "Apr": "04", "May": "05", "Jun": "06",
    "Jul": "07", "Aug": "08", "Sep": "09",
    "Oct": "10", "Nov": "11", "Dec": "12",
    "jan": "01", "feb": "02", "mar": "03",
    "apr": "04", "may": "05", "jun": "06",
    "jul": "07", "aug": "08", "sep": "09",
    "oct": "10", "nov": "11", "dec": "12",
    'okt':'10'
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

async def get_page(session,url):

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

    
def crawl():
    
    response = requests.get('https://kunsten.nu/artguide/search/actual/month/all/', headers=headers,timeout=30)
    soup = BeautifulSoup(response.text,'lxml')
    cards = soup.find(id='results').find_all('article')
    links = []
    for item in cards:
        url = item.a.get('href')
        links.append(url)
        #res = requests.get(url,headers=headers)
        #parse(res.text)

    links2 = []
    x = 10
    for i in range(0,len(links),x):
        links2.append(links[i:i+x])
    
    for links3 in links2:
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(main(links3))
        
        for page in results:
            parse(page=page)
            
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

months = []
def parse(page:str):
    
    soup = BeautifulSoup(page,'lxml')
    url = soup.find(attrs={'property':'og:url'})['content']
    title = soup.find(attrs={'property':'og:title'})['content']
    try:
        desk = soup.find(attrs={'property':'og:description'})['content']
    except:
        desk = ''
    image = soup.find(attrs={'property':'og:image'})['content']
    genre = 'Visual Arts'

    main_div = soup.main
    if main_div == None:
        return None
    try:
        date = main_div.find(class_='date_from').text.strip().split(' ')
    except:
        return None
    #print(date)
    day = date[0]
    mon = date[1]
    if 'maj' in mon:
        mon = 'may'
    month = month_mapping[mon]
    year = date[2]
    time = '00:00'
    date_start = f'{year}-{month}-{day}T{time}:00.000Z'

    #---------------------------
    try:
        date = main_div.find(class_='date_to').text.strip().split(' ')
    except:
        return None
    #print(date)
    day = date[0]
    mon = date[1]
    if 'maj' in mon:
        mon = 'may'
    month = month_mapping[mon]
    year = date[2]
    time = '00:00'
    date_end = f'{year}-{month}-{day}T{time}:00.000Z'
    
    try:
        Date = datetime.strptime(date_start, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        return None
    
    try:
        Date = datetime.strptime(date_end, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        return None
    
    doorOpen = Date.strftime("%H:%M")
    
    try:
        address = soup.find(class_='address').get_text('\n',strip=True)
        map = soup.find(class_='map-wrap').a.get('href').split('loc:')[1]
        map = map.split('+')
        lat = float(map[0])
        long = float(map[1])
    except:
        address = 'Kunsten'
        lat = 56.09537115
        long = 9.75162625

    dic = {
        "postType": "CULTURE", 
        "genre": genre,
        "url": url,
        "title": title,
        "address": address,
        "openingHours": doorOpen,
        "body": desk,
        "monthlySchedule": {
            "startDate": date_start, 
            "endDate": date_end 
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
    
    text = 'www.kunsten.nu | ' + dic['title']
    print(text)
    title = ' completed - ' + dic['title']
    logging.info(title)
    save.append(dic)
    
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

    return save
