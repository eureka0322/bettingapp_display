import time
import datetime
import requests
import csv
import mysql.connector
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from mysql.connector import Error

def save_csv(array, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(array)
    print("Array saved as CSV successfully.")

def parse_to_number(str_num):
    new_str = str_num.translate({ord(letter): None for letter in '+ '})
    new_num = new_str
    if len(new_str)==0:
        return ""
    if new_str[-1] == '½':
        new_num = new_str[:-1]
        if len(new_num)==0 or new_num=='-' : 
            new_num +='0.5'
        else: 
            new_num+='.5'
    return new_num

def get_spread_infos(info):
    new_info = info.translate({ord(letter): None for letter in '()'})
    if new_info == None:
        return ["", ""]
    infos = new_info.split('\xa0')
    if len(infos)==1:
        return [parse_to_number(infos[0]), ""]
    return [parse_to_number(infos[0]), parse_to_number(infos[1])]

def insert_data_into_table(category, team, spread_odd, spread_standard, money_line, game_id, game_date, game_title):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='bettingapp',
                                             user='root',
                                             password='')
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO tbl_betevo88 (category, team, spread_odd, spread_standard, money_line, game_id, game_date, game_title, game_datetime) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """

        current_date = datetime.datetime.now()
        record = (category, team, spread_odd, spread_standard, money_line, game_id, game_date, game_title, current_date)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print(spread_odd, spread_standard)
        print("Record inserted successfully into Betevo88 table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument("--disable-dev-shm-using")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_browser = webdriver.Chrome(options = chrome_options)

essential_cards = ["NFL", "NCAA Football", "WNBA", "High School Football", "International Baseball", "MLB", "NBA"]
checkbox_dic = {}
checkbox_id_list = []

csv_data = []

current_date = datetime.datetime.now()
date_string = current_date.strftime("%A %b %d")

try:
    chrome_browser.get('https://betevo88.com/')

    username = chrome_browser.find_element(By.ID,'customerid')
    username.clear()
    username.send_keys('Wc777')

    password = chrome_browser.find_element(By.ID, 'password')
    password.clear()
    password.send_keys('Test')

    login_button = chrome_browser.find_element(By.ID, 'submit')
    login_button.click()
    time.sleep(3)

    html = chrome_browser.page_source
    html_content = BeautifulSoup(html, "html.parser")    
    cards = html_content.find_all("div", {"class": "card"})
    flag = True
    for card in cards :
        top_header = card.find("span", {"class": "bg-top-box"})
        if top_header and top_header.text=="LEAGUES" :
            league_cards = card.find_all("div", {"class": "card"})

            for league_card in league_cards :
                card_header = league_card.find("span", {"class": "league-item-header-string"})
                if card_header and card_header.text in essential_cards : 
                    #print(card_header.text + "///")
                    list_items = league_card.find_all("label", {"class": "form-check-label"})

                    for list_item in list_items :
                        check_item_text = list_item.find("div").text
                        element_id = list_item.find_parent().find("input").get("id")
                        checkbox_dic[element_id] = check_item_text
                        checkbox_id_list.append(element_id)

    for item_id in checkbox_id_list :
        checkbox = chrome_browser.find_element(By.ID, item_id)
        checkbox.click()
        time.sleep(2)

        continue_button = chrome_browser.find_element(By.NAME, 'btn-continue')
        parent_continue = chrome_browser.execute_script('return arguments[0].parentNode;', continue_button)
        chrome_browser.execute_script("return arguments[0].scrollIntoView(0);", parent_continue)
        time.sleep(2)

        parent_continue.click()
        time.sleep(2)

        SCROLL_PAUSE_TIME = 2

        last_height = chrome_browser.execute_script("return document.body.scrollHeight")
        while True:
            chrome_browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = chrome_browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        schedule_html = chrome_browser.page_source
        schedule_content = BeautifulSoup(schedule_html, "html.parser")
        game_rows = schedule_content.find_all("div", {"class": "game-row"})

        bool_found = False
        folder_array = []
        for idx,row in enumerate(game_rows):
            game_date_div = row.find("div", {"class": "folder-label"})
            if game_date_div :
                game_date = game_date_div.find("div").text
                if game_date.find(date_string)!=-1:
                    folder_array.append(idx)
                if len(folder_array) and game_date.find(date_string)==-1:
                    folder_array.append(idx)
                    bool_found = True
                    break
        if bool_found == False and len(folder_array)>0:
            folder_array.append(len(game_rows))
        if len(folder_array)>0:
            for i in range(len(folder_array)-1):
                start_row = folder_array[i]
                end_row = folder_array[i+1]
                time_array = []
                for j in range(start_row, end_row):
                    row = game_rows[j]
                    time_div = row.find("div", {"class": "game-time-desktop"})
                    if(time_div): time_array.append(j)
                if len(time_array): time_array.append(end_row)
                for j in range(len(time_array)-1):
                    start_time_row = time_array[j]
                    end_time_row = time_array[j+1]
                    if end_time_row-start_time_row!=3: 
                        break
                    game_data_row = game_rows[start_time_row]
                    game_id = game_data_row.find("div", {"class": "game-time-desktop"})['id']
                    game_time = game_data_row.find("div", {"class": "time-desktop"}).text
                    game_name = game_data_row.find("div", {"class": "description-desktop"}).text

                    for k in range(start_time_row+1, end_time_row):
                        row_data = game_rows[k]
                        team_data = row_data.find("div", {"class":"team-row"})
                        team_info = team_data.find("div", {"class": None}).text
                        spread_info = team_data.find("div", {"class", "spread-cell"}).find("span", {"class": "ng-value-label"})
                        spread_odd_info = ""
                        spread_standard_info = ""
                        if spread_info == None : 
                            spread_info = team_data.find("div", {"class", "spread-cell"}).find("div", {"class", "straight-cell"})
                        if spread_info:
                            spread_odd_info = spread_info.text
                        money_line_info = ""
                        money_line_cell = team_data.find("div", {"class", "moneyline-cell"}).find("div",{"class": "straight-cell"})
                        if money_line_cell : 
                            money_line_info = money_line_cell.text
                        #if money_line_info == None: money_line_info = ""
                        #total_info= team_data.find("div", {"class": "total-cell"}).find("span", {"class": "ng-value-label"})
                        #if total_info: total_info = ""
                        #team_total_infos = team_data.find_all("div",{"class": "straight-cell"})
                        #total_info1 = ""
                        #total_info2 = ""
                        #if len(team_total_infos):
                        #    total_info1 = team_total_infos[0]
                            #total_info2 = team_total_infos[1]                item_id, team_info, spread_odd_info, spread_standard_info,  money_line_info            
                        spread_infos = get_spread_infos(spread_odd_info)
                        if team_info:
                            csv_data.append([checkbox_dic[item_id], team_info, spread_infos[0], spread_infos[1], money_line_info, game_id, game_time, game_name])
                            insert_data_into_table(checkbox_dic[item_id], team_info, spread_infos[0], spread_infos[1], money_line_info, game_id, game_time, game_name)
                            #print(item_id, team_info, spread_infos[0], spread_infos[1], money_line_info)
                #print(item_id, start_row, end_row, time_array)
        #print(len(game_rows))
        #print(folder_array, item_id)
        home_logo = chrome_browser.find_element(By.CLASS_NAME, 'button-home-desktop')
        parent_logo = chrome_browser.execute_script('return arguments[0].parentNode;', home_logo)
        chrome_browser.execute_script("return arguments[0].scrollIntoView(0);", parent_logo)
        time.sleep(2)
        home_logo.click()
        time.sleep(2)
        
    save_csv(csv_data, 'output.csv')

#    for item in checkbox_list :
#        print(item)
#    find_cards(html)
    #div_elements = soup.find_all("div", {"class": "form-check"})


finally:
   chrome_browser.quit()
