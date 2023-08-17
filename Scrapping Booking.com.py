#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
from bs4 import BeautifulSoup
import requests


# In[ ]:


link = 'https://www.booking.com/searchresults.id.html?label=gen173nr-1BCAEoggI46AdIM1gEaGiIAQGYARK4ARfIAQzYAQHoAQGIAgGoAgO4Aozj_KUGwAIB0gIkYzkwMjE4YWMtOTVjZC00NGQzLThjNzUtZjM3OWY2YWJjMjlk2AIF4AIB&sid=5602bf3ea84393825995cab6308add2b&aid=304142&ss=Indonesia&ssne=Yogyakarta&ssne_untouched=Yogyakarta&lang=id&src=searchresults&dest_id=99&dest_type=country&ac_position=0&ac_click_type=b&ac_langcode=en&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=4ad4126e4b3802bb&ac_meta=GhA0YWQ0MTI2ZTRiMzgwMmJiIAAoATICZW46BGluZG9AAEoAUAA%3D&checkin=2023-10-14&checkout=2023-10-15&group_adults=2&no_rooms=1&group_children=0&nflt=class%3D5&offset=0'
link = link.replace('offset=0', 'offset={}')

hotels = []

for i in range(0, 40):
    url = link.format(i*25) # Increase by 25 cards
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    cards = soup.find_all('div', {'data-testid':'property-card'}) 

    for card in cards:
        title = card.find('div', {'data-testid':'title'}).get_text()
    
#         location = card.find('span', {'data-testid':'address'}).get_text()
        
        room_type1 = card.find('span', {'class':'df597226dd'})
        if room_type1:
            room_type = (room_type1.get_text())
        else:
            room_type = 'Not mentioned'
    
        score1 = card.find('div', {'class':'b5cd09854e d10a6220b4'})
        if score1:
            score = (score1.get_text())
        else:
            score = 0
    
        rating1 = card.find('div', {'class':'b5cd09854e f0d4d6a2f5 e46e88563a'})
        if rating1:
            rating = rating1.get_text()
        else:
            rating = 'Not mentioned'
    
        review1 = card.find('div', {'class':'d8eab2cf7f c90c0a70d3 db63693c62'})
        if review1:
            review = review1.text.split(' ')[0]
        else:
            review = 0
    
        distance1 = card.find('span', {'data-testid':'distance'})
        if distance1:
            distance = distance1.get_text().replace(' from centre', '')
        else:
            distance = 'Not mentioned'
    
        price = card.find('span', {'data-testid':'price-and-discounted-price'}).get_text().split('\xa0')[1].replace(',', '')
        
        href = card.find('a', {'class':'e13098a59f'})['href']
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        response = requests.get(href, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')
        location1 = soup.find('span', {'class':'hp_address_subtitle js-hp_address_subtitle jq_tooltip'})
        if location1:
            location = location1.get_text()
        else:
            location = 'Not mentioned'
            
        coord = soup.find('a', {'class':'loc_block_link_underline_fix bui-link show_on_map_hp_link show_map_hp_link'})['data-atlas-latlng']
        
        hotels.append([title, room_type, score, rating, review, distance, price, href, location, coord])
        
df = pd.DataFrame(hotels, columns=['Hotel Name', 'Room Type', 'Score', 'Rating', 'Review', 'Distance From Centre', 'Price', 'Link', 'Location', 'Coordinate'])
df.drop_duplicates(keep='first', inplace=True, ignore_index=True)
df['Location'] = df['Location'].str.replace('\n', '')
df

