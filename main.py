from scrapers import kultunaut_Gastronomi,kultunaut_BornFamily,scenen,kunsten
from datetime import datetime
import json
import codecs
import html

# Create new scraper.log file
def clear_log_file():
    with open('scraper.log', 'w'):
        pass

# Saving the file
def save(savefile: list):
    current_date = datetime.now().strftime('%Y%m%d')
    with codecs.open(f'.\\savefiles\\cultures_save_{current_date}.json', 'w', encoding='utf-8') as f:
        json.dump({'posts': savefile}, f, ensure_ascii=False, indent=4)

# Check if hours is in correct format
def check_hours(time_str:str):
    
    if time_str == '' or time_str == None or type(time_str) == float:
        return False
    time_str = time_str.strip()
    if 'pm' in time_str.lower() or 'am' in time_str.lower():
        return True
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# Check if Date is in correct ISO 8601 format
def check_date(date_str:str):
    date_str = date_str.get('startDate')
    if date_str == None:
        return False
    
    if date_str == '' or date_str == None or type(date_str) == float:
        return False
    
    date_str = date_str.strip()
    date_str = date_str.replace('+','.')
    try:
        datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return True
    except ValueError:
        return False

# Cleaning the scrape Data
def clean_data(savefile:list):
    
        
    final_save = []
    keys_approved = ['title','openingHours','url','body','photos','genre','monthlySchedule','postType','channel','locationLatitude','locationLongitude','address','parent']
    
    for item in savefile:
        keys_item = item.keys()
        passed = True
        for key_ in keys_approved:
            if key_ not in keys_item:
                #print('key_ notfound : ',key_,item['address'])
                passed = False
        
        if passed == False:
            continue
        
        time = check_hours(item['openingHours'])
        if time == False:
            continue

        date = check_date(date_str=item['monthlySchedule'])
        if date == False:
            continue
        
        item['body'] = html.unescape(item['body'])
        final_save.append(item)

    save(savefile=final_save)

# Main 
def crawler():
    
    savefile = []
    
    # Returning a [list] contains of {dict} scrape data - from each script from /scrapers folder
    savefile.extend(kultunaut_Gastronomi.run())
    savefile.extend(kultunaut_BornFamily.run())
    savefile.extend(scenen.run())
    savefile.extend(kunsten.run())
    
    return savefile

if __name__ == '__main__':
    clear_log_file()
    savefile = crawler()
    clean_data(savefile=savefile)