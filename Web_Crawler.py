import datetime
import locale
from bs4 import BeautifulSoup
import urllib.request

# locale.setlocale(locale.LC_TIME, 'ko_KR.UTF-8')
# now = datetime.datetime.now()
# df = '%Y년 %m월 %d일 %H시 %M분 입니다.'
# print(now.strftime(df))
# nowDate = now.strftime('%Y년 %m월 %d일 %H시 %M분 입니다.')

print("\n       ※ Python Webcrawling Project 1 ※ \n ")
# print('   환영합니다, ' + nowDate)
print('   환영합니다, ')
print('      오늘의 주요 정보를 요약해 드리겠습니다.\n')

# 오늘의 날씨
print('  ○>> #오늘의 #날씨 #요약 \n')
webpage = urllib.request.urlopen('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8')
soup = BeautifulSoup(webpage, 'html.parser')

temperature = soup.find('div', "temperature_text").get_text().strip().replace('현재 온도', '')

temperature_info = soup.find('div', "temperature_info")

summary_list = soup.find('dl', attrs={'class':'summary_list'})
humidity = summary_list.find_all('dd')[1].get_text().strip()
wind = summary_list.find_all('dd')[2].get_text().strip()

web_index = [temperature, humidity, wind]
print(web_index)

# 풍향 관련하여 고민하기
# 풍향이 시간에 따라 있는데 이를 크롤링할 방법 생각
# datetime 활용해서 시간만 받고 이를 통해 받기?
