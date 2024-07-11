import requests
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
import logging
import traceback
import codecs
import json
import urllib.parse


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

def crawl2():
    
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
    
    response = requests.get('https://www.scenen.dk/', headers=headers,timeout=30)
    app= response.text.split('app: "')[1].split('",')[0]
    key = response.text.split('key: "')[1].split('",')[0]
    
    headers2 = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.scenen.dk',
        'Referer': 'https://www.scenen.dk/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    current_datetime = datetime.utcnow()
    target_date = datetime(today.year+1, 3, 31)
    days_remaining = (target_date - current_datetime).days
    
    past_datetime = current_datetime + timedelta(days=days_remaining)
    current_timestamp = str(int(current_datetime.timestamp()))
    past_timestamp = str(int(past_datetime.timestamp()))
    
    for i in range(0,999):
        i = str(i)

        while True:
            try:
                data = '{"requests":[{"indexName":"scenensearchable_posts","params":"query=&maxValuesPerFacet=10&page='+i+'&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&filters=post_type%3A\'turne\'%20AND%20(acf_sort_name%3A\'B%C3%B8rneforestilling\'%20OR%20acf_sort_name%3A\'B%C3%B8rne%20og%20ungdomsforestilling\'%20OR%20acf_sort_name%3A\'Ungdomsforestilling\'%20OR%20acf_sort_name%3A\'Familieforestilling\')&facets=%5B%22acf_venue_regions_rep%22%2C%22acf_category_name%22%2C%22acf_age_groups%22%5D&tagFilters=&facetFilters=%5B%5B%22acf_venue_regions_rep%3ARegion%20Hovedstaden%22%5D%5D&numericFilters=%5B%22acf_plays_to_timestamp%3E%3D'+current_timestamp+'%22%2C%22acf_plays_from_timestamp%3C%3D'+past_timestamp+'%22%5D"},{"indexName":"scenensearchable_posts","params":"query=&maxValuesPerFacet=10&page=0&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&filters=post_type%3A\'turne\'%20AND%20(acf_sort_name%3A\'B%C3%B8rneforestilling\'%20OR%20acf_sort_name%3A\'B%C3%B8rne%20og%20ungdomsforestilling\'%20OR%20acf_sort_name%3A\'Ungdomsforestilling\'%20OR%20acf_sort_name%3A\'Familieforestilling\')&hitsPerPage=1&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=acf_venue_regions_rep&numericFilters=%5B%22acf_plays_to_timestamp%3E%3D'+current_timestamp+'%22%2C%22acf_plays_from_timestamp%3C%3D'+past_timestamp+'%22%5D"}]}'

                response = requests.post(
                    f'https://u5ulvmji6q-3.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.0.3)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(3.7.0)%3B%20Vue%20(2.6.11)%3B%20Vue%20InstantSearch%20(2.7.0)%3B%20JS%20Helper%20(2.28.1)&x-algolia-api-key={key}&x-algolia-application-id={app}',
                    headers=headers2,
                    data=data,
                )

                response.encoding = 'utf-8'
                cards = response.json()['results'][0]['hits']
                total = response.json()['results'][0]['nbHits']
                break
            
            except:
                continue
        
        if cards == []:
            break
        
        for data in cards:
            try:
                parse_page(data,total)
            except Exception as e:
                pass

def crawl():
    
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
    
    response = requests.get('https://www.scenen.dk/', headers=headers,timeout=30)
    app= response.text.split('app: "')[1].split('",')[0]
    key = response.text.split('key: "')[1].split('",')[0]
    
    headers2 = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.scenen.dk',
        'Referer': 'https://www.scenen.dk/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    current_datetime = datetime.utcnow()
    target_date = datetime(today.year+1, 3, 31)
    days_remaining = (target_date - current_datetime).days
    
    past_datetime = current_datetime + timedelta(days=days_remaining)
    current_timestamp = str(int(current_datetime.timestamp()))
    past_timestamp = str(int(past_datetime.timestamp()))
    
    for i in range(0,999):
        i = str(i)
        
        while True:
            
            try:
                data = '{"requests":[{"indexName":"scenensearchable_posts","params":"query=&hitsPerPage=10&maxValuesPerFacet=10&page='+i+'&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&filters=post_type%3Aturne&facets=%5B%22acf_venue_regions_rep%22%2C%22acf_category_name%22%5D&tagFilters=&facetFilters=%5B%5B%22acf_venue_regions_rep%3ARegion%20Hovedstaden%22%5D%5D&numericFilters=%5B%22acf_plays_to_timestamp%3E%3D'+current_timestamp+'%22%2C%22acf_plays_from_timestamp%3C%3D'+past_timestamp+'%22%5D"},{"indexName":"scenensearchable_posts","params":"query=&hitsPerPage=1&maxValuesPerFacet=10&page=0&highlightPreTag=__ais-highlight__&highlightPostTag=__%2Fais-highlight__&filters=post_type%3Aturne&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&clickAnalytics=false&facets=acf_venue_regions_rep&numericFilters=%5B%22acf_plays_to_timestamp%3E%3D'+current_timestamp+'%22%2C%22acf_plays_from_timestamp%3C%3D'+past_timestamp+'%22%5D"}]}'

                response = requests.post(
                    f'https://u5ulvmji6q-3.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.0.3)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(3.7.0)%3B%20Vue%20(2.6.11)%3B%20Vue%20InstantSearch%20(2.7.0)%3B%20JS%20Helper%20(2.28.1)&x-algolia-api-key={key}&x-algolia-application-id={app}',
                    headers=headers2,
                    data=data,
                )

                response.encoding = 'utf-8'
                cards = response.json()['results'][0]['hits']
                total = response.json()['results'][0]['nbHits']
                break
            
            except:
                continue

        if cards == []:
            break
        
        for data in cards:
            try:
                parse_page(data,total)
            except Exception as e:
                pass
            
def parse_page(data:dict,total:int):
    total = str(total)
    title = data['post_title']
    main_category = data.get('acf_category_name','')
    sub_category = data.get('acf_subcategory_name','')
    description = data.get('acf_event_description','')
    category = main_category
    if sub_category != '':
        category = f'{main_category}/{sub_category}'
    image = data['acf_image_large_url']
    url = data['permalink']
    while True:
        try:
            response = requests.get(url,headers=headers,timeout=10)
            break
        except requests.exceptions.Timeout:
            continue
        except requests.exceptions.ConnectionError:
            continue

    soup2 = BeautifulSoup(response.text,'lxml')
    tableData = soup2.find(class_='tableData').find(class_='venue-dates').parent
    date_month = tableData.h2.get_text('|',strip=True).replace('.','').split('|')
    day = date_month[0].strip()
    if len(day) == 1:
        day = '0'+day
    month = date_month[1].strip()
    try:
        month = month_mapping[month]
    except:
        return None
    year = tableData.find(class_='venue-year').text.strip()
    try:
        time = tableData.find(class_='venue-dayname').text.split(' ')[1].strip()
    except:
        time = '00:00'
    date_str = f'{year}-{month}-{day}T{time}:00.000Z'
    try:
        Date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        return None
    doorOpen = Date.strftime("%H:%M")
    try:
        ticket = tableData.find(class_='venue-ticket').get('href')
    except:
        ticket = url
    try:
        address = tableData.find(class_='venue-adress').text
        latlong = tableData.find(class_='google-info').find(class_='google-link')['href'].split('@')[1].split(',')
        locationLatitude = float(latlong[0])
        locationLongitude = float(latlong[1])
        
    except:
        address = 'SCENEN'
        locationLatitude = 56.09537115
        locationLongitude = 9.75162625
    
    dic = {
        "postType": "Performing Arts", 
        "genre": category,
        "url": ticket,
        "title": title,
        "address": address,
        "openingHours": doorOpen,
        "body": description,
        "monthlySchedule": {
            "startDate": date_str, 
            "endDate": date_str 
        },
        "photos": [
            {
            "provider": image
            }
        ],
        "channel": "@public",
        "parent": "ROOT",
        "locationLatitude": locationLatitude,
        "locationLongitude": locationLongitude
    }
    text = 'www.scenen.dk | ' + dic['title'] + ' | ' + total
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
    
    try:
        crawl2()
        logging.info(f" completed - total: {len(save)}")
    except Exception as e:
        error_message = ''.join(traceback.format_exception(type(e), e, e.__traceback__))
        logging.info("-" * 113)
        logging.error(f"An error occurred: (scrapers\\{filename})\n%s", error_message)
        logging.error("-" * 113)

    saving(savefile=save,filename=filename.replace('.py',''))
    return save

