import requests
import os
import time
import mysql.connector
import bs4
import lxml
import time

# CREATE TABLE `match_result` (
# 	`id` INT PRIMARY KEY AUTO_INCREMENT,
# 	`team1` VARCHAR(255),
# 	`team2` VARCHAR(255),
# 	`winner` VARCHAR(255),
# 	`margin` VARCHAR(255),
# 	`ground` VARCHAR(255),
# 	`matchDate` VARCHAR(255),
# 	`scorecard` VARCHAR(255)
# );

def database_login() :
    command_data_base= mysql.connector.connect(
    host="localhost",
    user="root",
    password="saurav",
    database="match_data"
    )
    return(command_data_base)

match_result_url ="https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament"

command_data_base=database_login()
time.sleep(1)
mycursor=command_data_base.cursor()

match_result_header ={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # Cookie: SWID=31bb1ab1-fbcd-4560-b481-ba839f47ef35; AMCVS_EE0201AC512D2BE80A490D4C%40AdobeOrg=1; AMCV_EE0201AC512D2BE80A490D4C%40AdobeOrg=-330454231%7CMCIDTS%7C19382%7CMCMID%7C90243146121700889758599875745506251111%7CMCAID%7CNONE%7CMCOPTOUT-1674543978s%7CNONE%7CvVersion%7C3.1.2; s_ips=581; s_nr30=1674537083185-New; s_gpv=espncricinfo%3Aseries%3Aicc-men-s-t20-world-cup-2022-23%3Avideo; s_tp=2028; s_pers=%20s_c24%3D1674537089182%7C1769145089182%3B%20s_c24_s%3DFirst%2520Visit%7C1674538889182%3B%20s_gpv_pn%3Dcricinfo%253Aicc%2520men%2527s%2520t20%2520world%2520cup%252C%25202022/23%2520site%253Arecords%253Ahomepage%7C1674538889195%3B; s_ensCDS=0; s_sess=%20s_cc%3Dtrue%3B%20s_omni_lid%3D%3B%20s_sq%3Dwdgespcricinfo%25252Cwdgespge%253D%252526c.%252526a.%252526activitymap.%252526page%25253Despncricinfo%2525253Aseries%2525253Aicc-men-s-t20-world-cup-2022-23%2525253Avideo%252526link%25253DStats%252526region%25253Dmain-container%252526pageIDType%25253D1%252526.activitymap%252526.a%252526.c%252526pid%25253Despncricinfo%2525253Aseries%2525253Aicc-men-s-t20-world-cup-2022-23%2525253Avideo%252526pidt%25253D1%252526oid%25253Dhttps%2525253A%2525252F%2525252Fwww.espncricinfo.com%2525252Fci%2525252Fengine%2525252Fseries%2525252F1298134.html%2525253Fview%2525253Drecords%252526ot%25253DA%3B%20s_ppvl%3Dcricinfo%25253Aicc%252520men%252527s%252520t20%252520world%252520cup%25252C%2525202022/23%252520site%25253Arecords%25253Ahomepage%252C50%252C50%252C581%252C1280%252C581%252C1280%252C720%252C1.5%252CP%3B%20s_ppv%3Dcricinfo%25253Aicc%252520men%252527s%252520t20%252520world%252520cup%25252C%2525202022/23%252520site%25253Arecords%25253Ahomepage%252C50%252C50%252C581%252C725%252C581%252C1280%252C720%252C1.5%252CP%3B
    "Host": "stats.espncricinfo.com",
    "Referer": "https://www.espncricinfo.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-site",
    # "Sec-Fetch-User": ?1
    # "Sec-GPC": "1"
    # "Upgrade-Insecure-Requests": "1"
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

session = requests.session()
match_result_html=session.get(match_result_url,headers=match_result_header,verify=False)
match_result_soup=bs4.BeautifulSoup(match_result_html.text,'xml')
# print(match_result_soup.encode('utf-8'))

match_result_table = match_result_soup.find('table',{'class':'engineTable'})
# print(match_result_table)
match_result_table_row = match_result_table.find_all('tr')
match_result_list = []
match_links_list = []
for row in match_result_table_row[1:]:
    match_result_table_data = row.find_all('td')
    data_list =[]
    for data in match_result_table_data:
        # data = data.find('a')
        # print(data.text)
        data_list.append(data.text.replace("\n",""))
        if data.find('a') != None:
            if "/ci/engine/match/" in data.find('a')['href']:
                match_links = data.find('a')['href']
                match_links_list.append("https://stats.espncricinfo.com" + match_links)
    match_result_list.append(tuple(data_list))
    
sql_query="INSERT INTO match_result(team1,team2,winner ,margin,ground,matchDate,scorecard) VALUES (%s,%s,%s,%s,%s,%s,%s)"
mycursor.executemany(sql_query, match_result_list)
command_data_base.commit()
print("Data inserted")
    
# print(match_result_list)
# print(match_links_list)