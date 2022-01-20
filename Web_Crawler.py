from bs4 import BeautifulSoup
import urllib.request

def start():
    webpage = urllib.request.urlopen('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8')
    soup = BeautifulSoup(webpage, 'html.parser')

    temperature = soup.find('div', "temperature_text").get_text().strip().replace('현재 온도', '')

    temperature_info = soup.find('div', "temperature_info")

    summary_list = soup.find('dl', attrs={'class':'summary_list'})
    humidity = summary_list.find_all('dd')[1].get_text().strip()
    wind = summary_list.find_all('dd')[2].get_text().strip()

    direction_text = summary_list.find_all('dt')[2].get_text().strip().replace('바람(', '')
    direction = direction_text.replace(')', '')

    report_card = soup.find('div', "report_card_wrap")

    item1 = report_card.find('li', attrs={'class': 'item_today level1'})
    a1 = item1.find('span', attrs={'class': 'txt'}).get_text().strip()

    item2 = report_card.find('li', attrs={'class': 'item_today level2'})
    a2 = item2.find('span', attrs={'class': 'txt'}).get_text().strip()

    web_index = [temperature, humidity, direction, wind, a2, a1]
    # print(web_index)
    return web_index


# webpage = urllib.request.urlopen('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8')
# soup = BeautifulSoup(webpage, 'html.parser')
#
# temperature = soup.find('div', "temperature_text").get_text().strip().replace('현재 온도', '')
#
# temperature_info = soup.find('div', "temperature_info")
#
# summary_list = soup.find('dl', attrs={'class':'summary_list'})
# humidity = summary_list.find_all('dd')[1].get_text().strip()
# wind = summary_list.find_all('dd')[2].get_text().strip()
#
# direction_text = summary_list.find_all('dt')[2].get_text().strip().replace('바람(', '')
# direction = direction_text.replace(')', '')
#
# report_card = soup.find('div', "report_card_wrap")
#
# item1 = report_card.find('li', attrs={'class':'item_today level1'})
# a1 = item1.find('span', attrs={'class':'txt'}).get_text().strip()
#
# item2 = report_card.find('li', attrs={'class':'item_today level2'})
# a2 = item2.find('span', attrs={'class':'txt'}).get_text().strip()
#
# print(a2, a1)