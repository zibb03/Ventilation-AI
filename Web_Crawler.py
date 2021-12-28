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
# # print(soup)
# temps = soup.find('span',"blind")
# print(temps)
# cast = soup.find('p',"temperature_text")
# print(cast)

a = soup.find('div', "temperature_text")
b = a.find(a, 'span', "blind")
print(b)
# print('--> 서울 날씨 : ' , temps.get_text() , '℃' , cast.get_text())

webpage = urllib.request.urlopen('https://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%8C%80%EA%B5%AC+%EB%82%A0%EC%94%A8')
soup = BeautifulSoup(webpage, 'html.parser')
temps = soup.find('span',"todaytemp")
cast = soup.find('p',"cast_txt")
print('--> 대구 날씨 : ' , temps.get_text() , '℃' , cast.get_text())

webpage = urllib.request.urlopen('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%B6%80%EC%82%B0+%EB%82%A0%EC%94%A8&oquery=%EB%8C%80%EA%B5%AC+%EB%82%A0%EC%94%A8&tqi=UrZy%2Bsp0YidssAyki54ssssssKC-251380')
soup = BeautifulSoup(webpage, 'html.parser')
temps = soup.find('span',"todaytemp")
cast = soup.find('p',"cast_txt")
print('--> 부산 날씨 : ' , temps.get_text() , '℃' , cast.get_text())
print('\n')