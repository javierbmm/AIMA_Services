#!/usr/bin/env python3

import requests
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import selenium.common.exceptions
from selenium.common.exceptions import NoSuchElementException   
from selenium.common.exceptions import ElementNotSelectableException  
from selenium.common.exceptions import StaleElementReferenceException  
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from datetime import datetime, time, timedelta, date
import urllib3.exceptions
from time import sleep
from random import randint


delay = [1,2,1.5,2,2.3]
LINE = "\n--------------------------------------------\n"
# Users ID's:
AIMA_ID = '846646570'   # AIMA_Services
JAVIER_ID = '394580187' # Javier Merida
# List of XPath's:
XPATH_SECTION = '//div[starts-with(@class, "lpdgl")]'
XPATH_LEAGUE = '//div[@class="sm-CouponLink_Label "]'
XPATH_MATCH  = '//div[starts-with(@class,"sl-CouponParticipantWithBookCloses_Name ")]'
XPATH_MATCH_CONTAINER = '//div[@class= "sl-CouponParticipantWithBookCloses sl-CouponParticipantIPPGBase "]'
XPATH_HOME = '//'
XPATH_HOME_BUTTON = "//a[@class='hm-HeaderModule_Logo ']"
XPATH_ESPAÑOL = '//div[contains(text(), "Soccer")]'
XPATH_24HRS_BUTTON = '//div[contains(text(), "Next 24 hrs")]'
XPATH_ODDS_DROPDOWN = "//a[@class='hm-DropDownSelections_Button hm-DropDownSelections_DropLink ' and contains(.,'Odds')]"
XPATH_ODDS_DECIMAL = "//a[starts-with(@class,'hm-DropDownSelections_Item ') and contains(.,'Decimal')]"
# BTTS:
BTTS_STRING = 'BTTS'
XPATH_BTTS_CONTAINER = '//span[contains(text(), "Both Teams to Score")]/ancestor::div[@class="gl-MarketGroup "]' 
XPATH_BTTS = '//span[contains(text(), "Both Teams to Score")]' # Useless
XPATH_BTTS_OPTION = '//div[@class="gl-Participant gl-Participant_General gl-Market_CN-2 "]'
XPATH_BTTS_FEE = '//span[@class="gl-Participant_Odds"]'
XPATH_BTTS_YES_NO = '//span[@class="gl-Participant_Name"]'
XPATH_BTTS_MATCH = '//span[starts-with(@class,"cl-EnhancedDropDown ")]'
XPATH_BTTS_DATE = '//div[starts-with(@class,"cm-MarketGroupExtraData_TimeStamp ")]'
XPATH_CLOCK = '//div[@class="pi-CouponParticipantClockInPlay_GameTimerWrapper "]'
# OVER 2.5:
OVER25_STRING = 'OVER 2,5'
XPATH_OVER25_CONTAINER = '//span[contains(., "Goals Over/Under")]/ancestor::div[starts-with(@class,"gl-MarketGroup ")]'
XPATH_OVER25_SECTION = '//div[starts-with(@class,"gl-MarketValuesExplicit2 gl-Market_General gl-Market_PWidth-37-5 ")]'
XPATH_OVER25_OPTION = '//span[@class="gl-ParticipantRowValue_Name"]'
XPATH_OVER25_FEE = '//span[@class="gl-ParticipantOddsOnly_Odds"]'
# OVER 0.5 HT:
OVER05_HT_STRING = 'OVER 0.5 HT'
XPATH_OVER05_HT_CLICK_SECTION = '//div[@class="cl-MarketGroupNavBarButton " and contains(.,"Half")]'
XPATH_OVER05_HT_CONTAINER = '//span[contains(., "First Half Goals")]/ancestor::div[starts-with(@class,"gl-MarketGroup ")]'
XPATH_OVER05_HT_OPTION = '//span[@class="gl-ParticipantRowValue_Name"]'
XPATH_OVER05_HT_FEE = '//span[@class="gl-ParticipantOddsOnly_Odds"]'
# LIVE MATCHES:
XPATH_LIVE_BUTTON = '//div[@class="sl-LiveInPlayHeader_LiveLabel "]'
XPATH_LIVE_GENERAL = '//div[starts-with(@class,"ip-ControlBar_BBarItem ") and contains(.,"Overview")]'
XPATH_LIVE_LEAGUE = '//div[@class="ipo-Competition ipo-Competition-open "]'
XPATH_LIVE_LEAGUE_NAME = '//div[@class="ipo-CompetitionButton_NameLabel ipo-CompetitionButton_NameLabelHasMarketHeading "]'
XPATH_LIVE_MATCH = '//div[@class="ipo-ScoreDisplayStandard_Wrapper "]'
XPATH_LIVE_MATCH_CLICK = '//div[@class="sl-CouponParticipantWithBookCloses_NameContainer "]' #useless
XPATH_LIVE_NAME = '//div[starts-with(@class,"ipe-GridHeader_FixtureCell ")]'
XPATH_LIVE_MIN = '//div[@class="ipe-SoccerHeaderLayout_ExtraData "]'
XPATH_LIVE_ATAQUES = '//div[@class="ml1-StatsCharts_Column ml1-StatsCharts_Column-left "]'
XPATH_LIVE_PELIGROSOS = '//div[@class="ml1-StatsCharts_Column ml1-StatsCharts_Column-middle "]'
XPATH_LIVE_POSESION = '//div[@class="ml1-StatsCharts_Column ml1-StatsCharts_Column-right "]'
XPATH_LIVE_STATS_TITLE = '//div[starts-with(@class,"ml1-AllStats_Title ")]'
XPATH_LIVE_STATS = '//div[starts-with(@class,"ml1-StatsCharts_Column ml1-StatsCharts_Column") or \
starts-with(@class,"ml1-AllStats_StatsBarsColumn ml1-AllStats_StatsBarsColumn")]'
XPATH_LIVE_ALL_STATS = '//div[@class="ml1-AllStats_StatsCharts "]'
XPATH_LIVE_TEAM_1 = '//div[@class="ml1-StatWheel_Team1Text "] | //span[@class="ml1-SoccerStatsBar_MiniBarValue ml1-SoccerStatsBar_MiniBarValue-1 "]'
XPATH_LIVE_TEAM_2 = '//div[@class="ml1-StatWheel_Team2Text "] | //span[@class="ml1-SoccerStatsBar_MiniBarValue ml1-SoccerStatsBar_MiniBarValue-2 "]'
XPATH_LIVE_OVER05_HT_CONTAINER = '//span[contains(., "First Half Goals")]/ancestor::div[starts-with(@class,"gl-MarketGroup ")]'
XPATH_LIVE_CORNERS = '//div[@class="ipe-SoccerGridColumn ipe-SoccerGridColumn_ICorner "]//div[@class="ipe-SoccerGridCell "]'
XPATH_LIVE_OVER_X_CONTAINER = '//span[contains(., "Match Goals")]/ancestor::div[starts-with(@class,"gl-MarketGroup ")]'
XPATH_MATCH_LIVE_BUTTON = '//div[contains(.,"Match Live") and starts-with(@class, "lv-ButtonBar_MatchLive ")]'


class live_match_info:
    # Constructor
    def __init__(self, match_name_, min_, e1_ataques_, e1_ataques_peligrosos_, e1_tiros_puerta_, e1_corners_,
                 e1_posesion_,
                 e2_ataques_, e2_ataques_peligrosos_, e2_tiros_puerta_, e2_corners_, e2_posesion_, fee_, option_,
                 ht_checked_=False, ft_checked_=False):
        self.match_name = match_name_
        self.min = min_
        self.fee = fee_
        self.option = option_

        # Equipo 1:
        self.e1_ataques = e1_ataques_
        self.e1_a_peligrosos = e1_ataques_peligrosos_
        self.e1_tiros_puerta = e1_tiros_puerta_
        self.e1_corners = e1_corners_
        self.e1_posesion = e1_posesion_
        # Equipo 2:
        self.e2_ataques = e2_ataques_
        self.e2_a_peligrosos = e2_ataques_peligrosos_
        self.e2_tiros_puerta = e2_tiros_puerta_
        self.e2_corners = e2_corners_
        self.e2_posesion = e2_posesion_

        #Half time and full time
        self.ht_checked = ht_checked_
        self.ft_checked = ft_checked_
        return

    def get_name(self): 
        name = str(self.match_name)
        return name


    def is_ht_checked(self):
        return self.hf_checked

    def is_ft_checked(self):
        return self.ft_checked


    def to_string(self):
        string = '\n***MATCH(Equipo1 vs Equipo2): '+str(self.match_name)+'***\n***-MIN:*** '+self.min
        string += '\n***--'+str(self.option)+':*** '+str(self.fee)
        string += '\n***--Ataques:*** ' + str(self.e1_ataques) +'|'+str(self.e2_ataques)
        string += '\n***--Ataques peligrosos:*** '+ str(self.e1_a_peligrosos) +'|'+str(self.e2_a_peligrosos)
        string += '\n***--Tiros a puerta:*** '+ str(self.e1_tiros_puerta) +'|'+str(self.e2_tiros_puerta)
        string += '\n***--Posesion:*** '+ str(self.e1_posesion) +'|'+str(self.e2_posesion)

        return string

    def __str__(self):
        string = '\n***MATCH(Equipo1 vs Equipo2): '+str(self.match_name)+'***\n***-MIN:*** '+self.min
        string += '\n***--'+str(self.option)+':*** '+str(self.fee)
        string += '\n***--Ataques:*** ' + str(self.e1_ataques) +'|'+str(self.e2_ataques)
        string += '\n***--Ataques peligrosos:*** '+ str(self.e1_a_peligrosos) +'|'+str(self.e2_a_peligrosos)
        string += '\n***--Tiros a puerta:*** '+ str(self.e1_tiros_puerta) +'|'+str(self.e2_tiros_puerta)
        string += '\n***--Posesion:*** '+ str(self.e1_posesion) +'|'+str(self.e2_posesion)

        return string



class match_info:
    # Constructor
    def __init__(self,match_name_,date_,btts_,over25_,over05ht_):
        # Variables initialization
        self.match_name         = match_name_
        self.date               = date_
        self.btts_amount        = btts_
        self.over25_amount      = over25_
        self.over05_ht_amount   = over05ht_

    def get_name(self): 
        name = str(self.match_name)
        return name

    def to_string(self):
        string = '\n***MATCH: '+str(self.match_name)
        string +='***\n***-Date:*** '+str(self.date)
        string +='\n***--BTTS:*** '+str(self.btts_amount)+'\n***--OVER 2.5:*** '+str(self.over25_amount)
        string +='\n***--OVER 0.5 HT:*** '+str(self.over05_ht_amount)

        return string

#Not used classes:
class BTTS:
    # Constructor
    def __init__(self,match_name_,date_,option_,fee_):
        # Variables initialization
        self.match_name = match_name_
        self.date       = date_
        self.option     = option_
        self.fee        = fee_
        self.type       = 'BTTS'

    def to_string(self):
        string = '\n***MATCH: '+str(self.match_name)+'***\n***TYPE: '+self.type
        string =+'***\n***-Date:*** '+str(self.date)+'\n***-Option:*** '+str(self.option)+'\n***-Amount:*** '+str(self.fee)
        return string
class OVER_2_5:
    # Constructor
    def __init__(self,match_name_,date_,option_,fee_):
        # Variables initialization
        self.match_name = match_name_
        self.date       = date_
        self.option     = option_
        self.fee        = fee_
        self.type       = 'OVER 2,5'

    def to_string(self):
        string = '\n***MATCH: '+str(self.match_name)+'***\n***TYPE: '+self.type
        string =+'***\n***-Date:*** '+str(self.date)+'\n***-Option:*** '+str(self.option)+'\n***-Amount:*** '+str(self.fee)
        return string
##################

def add_match_list_to_dictionary(match_list_,dict_):
    for item in match_list_:
        dict_[item.get_name()] = item

    return

def send_msg_by_groups(bot_message):
    counter = 0
    msg = ''

    for x in bot_message:
        print('info: '+x+LINE)
        msg += x
        if(counter >=10):
            bot_send_msg(msg)
            msg = ''
            counter = 0
        # end if
        counter+=1
    # end for
    print('Sending information')
    bot_send_msg(msg)

    return

def bot_send_msg(msg):
    #Bot token for AIMA_futBot:     
    bot_token = '656778310:AAHyZaNhAQwVYitZcIHAfi2TmQN_CBKdOIU'
    #Insert your ID below. 
    #AIMA_ID = '700187299' <- for AIMA_Services 
    bot_chatID = JAVIER_ID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + msg
    response = requests.get(send_text)

    print(send_text)

    return response.json()


def bot_send_msg_to(msg, user_id):
    # Bot token for AIMA_futBot:
    bot_token = '656778310:AAHyZaNhAQwVYitZcIHAfi2TmQN_CBKdOIU'
    # Insert your ID below.
    # AIMA_ID = '700187299' <- for AIMA_Services
    bot_chatID = user_id
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + msg
    response = requests.get(send_text)

    print(send_text)

    return response.json()


def open_website(url):

    # url                 = 'https://www.bet365.es'
    options             = Options()
    options.headless    = True
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    options.add_argument('user-agent='+user_agent)
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("detach", True)
    #options.add_argument("--disable-gpu")

    #browser = webdriver.Chrome(ChromeDriverManager().install())
    # TODO: Catch exception when unable to open website
    global browser
    browser = webdriver.Chrome('/usr/bin/chromedriver',options=options)

    browser.get(url)
    wait = WebDriverWait(browser, 6000) 
    sleep(delay[randint(0,4)]) # Time in seconds.

    return browser

def click_español(browser):
    #Navigation:
    sleep(delay[randint(0,4)]) # Time in seconds.
    sleep(delay[randint(0,4)]) # Time in seconds.
    español = browser.find_element_by_link_text("English")
    español.send_keys(Keys.ENTER)
    sleep(delay[randint(0,4)]) # Time in seconds.
  
    return

def click_futbol_section(browser):
    WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH, XPATH_ESPAÑOL))) 

    futbol_section = browser.find_element_by_xpath(XPATH_ESPAÑOL)
    sleep(delay[randint(0,4)]) # Time in seconds.
    futbol_section.click()
    
    sleep(delay[randint(0,4)]) # Time in seconds.

    return

def click_home_button(browser):
    sleep(delay[randint(0,4)]) # Time in seconds.

    WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH, XPATH_HOME_BUTTON))) 
    live_section = browser.find_element_by_xpath(XPATH_HOME_BUTTON)
    sleep(delay[randint(0,4)]) # Time in seconds.
    live_section.click()
    
    sleep(delay[randint(0,4)]) # Time in seconds.

    return

def set_decimal_odds(browser):
    WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH, XPATH_ODDS_DROPDOWN))) 
    drop_down = browser.find_element_by_xpath(XPATH_ODDS_DROPDOWN)
    drop_down.click()
    sleep(delay[randint(0,4)]) # Time in seconds.
    browser.find_element_by_xpath(XPATH_ODDS_DECIMAL).click()

    sleep(delay[randint(0,4)]) # Time in seconds.

    return
    
def click_live_button(browser):
    WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH, XPATH_LIVE_BUTTON))) 
    live_section = browser.find_element_by_xpath(XPATH_LIVE_BUTTON)
    sleep(delay[randint(0,4)]) # Time in seconds.
    live_section.click()
    
    sleep(delay[randint(0,4)]) # Time in seconds.

    return

def click_live_general(browser):
    WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH, XPATH_LIVE_GENERAL))) 
    live_section = browser.find_element_by_xpath(XPATH_LIVE_GENERAL)
    sleep(delay[randint(0,4)]) # Time in seconds.
    live_section.click()
    
    sleep(delay[randint(0,4)]) # Time in seconds.

    return

def click_proximas24hrs(browser):
    WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH, XPATH_24HRS_BUTTON))) 
    live_section = browser.find_element_by_xpath(XPATH_24HRS_BUTTON)
    sleep(delay[randint(0,4)]) # Time in seconds.
    live_section.click()
    
    sleep(delay[randint(0,4)]) # Time in seconds.

    return

def click_match_live(browser):
    WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, XPATH_MATCH_LIVE_BUTTON)))
    live_section = browser.find_element_by_xpath(XPATH_MATCH_LIVE_BUTTON)
    sleep(delay[randint(0, 4)])  # Time in seconds.
    live_section.click()
    sleep(delay[randint(0, 4)])  # Time in seconds.
    live_section.click()

    sleep(delay[randint(0, 4)])  # Time in seconds.

    bot_send_msg_to("Clicked match live button", JAVIER_ID)

    return

def get_leagues(browser):
    click_futbol_section(browser)
    click_proximas24hrs(browser)

    match_dict = {}
    #Searching by LEAGUES: 

    WebDriverWait(browser,250).until(EC.presence_of_element_located((By.XPATH, XPATH_LEAGUE)))


    LEAGUES = browser.find_elements_by_xpath(XPATH_LEAGUE)
    
    number_of_leagues = len(LEAGUES)
    counter = 0
    go_down = False
    times = 0
    
    while counter < number_of_leagues:
        if go_down: scroll_down(browser, times)
        WebDriverWait(browser,150).until(EC.presence_of_element_located((By.XPATH, XPATH_LEAGUE))) 
        league_elements = browser.find_elements_by_xpath(XPATH_LEAGUE)
        league = league_elements[counter]
        msg = LINE + league.text + LINE
        print(msg)
        print(counter)
        print(len(LEAGUES))
        try:
            sleep(delay[randint(0,4)]) # Time in seconds.
            league.click()
            sleep(delay[randint(0,4)]) # Time in seconds.
            #browser.back()
        except (ElementNotVisibleException):
            if league.text == '': #Ignore it if it's empty 
                counter+=1
                continue
            print('exception 1')
            go_down = True
            times += 1
            continue
        except:
             counter +=1
             print('ERROR: League is not available anymore')
             continue
        # End try-except

        #Extracting MATCHES: 
        match_dict.update(get_matches(browser,msg))
        browser.back()
        click_futbol_section(browser)
        counter += 1
    # End while
        break

    return match_dict

def xpath_exists(xpath,browser):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def detect_btts(browser, min_amount):  # min_amount: 1.80
    btts = -1

    if not xpath_exists(XPATH_BTTS_CONTAINER, browser):  # Trying again in case website haven't loaded correctly
        sleep(delay[randint(0, 4)])  # Time in seconds.
        if not xpath_exists(XPATH_BTTS_CONTAINER, browser):
            print('ERROR: Couldn\'t find the element: "Both Teams to Score"')
            return btts
        # end if
    # end if
    container = browser.find_element_by_xpath(XPATH_BTTS_CONTAINER)
    section = container.find_elements_by_xpath('.' + XPATH_BTTS_OPTION)
    for item in section:
        yes_or_no = item.find_element_by_xpath('.' + XPATH_BTTS_YES_NO).text
        fee = item.find_element_by_xpath('.' + XPATH_BTTS_FEE).text
        if float(fee) <= float(min_amount) and str(yes_or_no) == 'Yes':
            btts = fee
        else:
            continue
        # end if-else
    # end for

    return btts


def detect_over25(browser, min_amount):  # min_amount: 1.80
    over25 = -1

    if not xpath_exists(XPATH_OVER25_CONTAINER, browser):  # Trying again in case website haven't loaded correctly
        sleep(delay[randint(0, 4)])  # Time in seconds.
        if not xpath_exists(XPATH_OVER25_CONTAINER, browser):
            print('ERROR: Couldn\'t find the element: "Goals Over/Under"')
            return over25
        # end if
    # end if

    container = browser.find_element_by_xpath(XPATH_OVER25_CONTAINER)
    section = container.find_elements_by_xpath('.' + XPATH_OVER25_SECTION)
    for item in section:
        option = container.find_element_by_xpath('.' + XPATH_OVER25_OPTION).text
        fee = item.find_element_by_xpath('.' + XPATH_OVER25_FEE).text
        if float(fee) <= float(min_amount) and option == '2.5':
            over25 = fee
        else:
            continue
        # end if-else
    # end for
    return over25


def detect_over05_ht(browser, min_amount):  # min_amount: 1.40
    over05_ht = -1
    if not xpath_exists(XPATH_OVER05_HT_CLICK_SECTION, browser):
        print('ERROR: Couldn\'t find the element: "Half"')
        return over05_ht

    print('Clicking')
    sleep(delay[randint(0, 4)])  # Time in seconds.
    browser.find_element_by_xpath(XPATH_OVER05_HT_CLICK_SECTION).click()
    print('clicked')

    sleep(delay[randint(0, 4)])  # Time in seconds.

    if not xpath_exists(XPATH_OVER05_HT_CONTAINER, browser):  # Trying again in case website haven't loaded correctly
        sleep(delay[randint(0, 4)])  # Time in seconds.
        if not xpath_exists(XPATH_OVER05_HT_CONTAINER, browser):
            print('ERROR: Couldn\'t find the element: "First Half Goals"')
            browser.back()
            return over05_ht
        # end if
    # end if

    container = browser.find_element_by_xpath(XPATH_OVER05_HT_CONTAINER)
    section = container.find_elements_by_xpath('.' + XPATH_OVER05_HT_OPTION)
    i = 0
    print('OPTIONS: ')
    for item in section:
        print(item.text)
        print(i)
        i += 1

    amount = container.find_elements_by_xpath('.' + XPATH_OVER05_HT_FEE)
    i = 0
    print('AMOUNTS')
    for item in amount:
        print(item.text)
        print(i)
        i += 1

    if section[0].text == '0.5':  # Index 0 for '0.5 HT'
        amount = container.find_elements_by_xpath('.' + XPATH_OVER05_HT_FEE)
        if float(amount[0].text) <= float(min_amount):  # Index 0 for '0.5 HT'
            over05_ht = amount[0].text
            print(over05_ht)

    browser.back()
    sleep(delay[randint(0, 4)])  # Time in seconds.

    return over05_ht


def extract_matches_information(browser):
    print('Looking for matches')
    print('->match')
    btts = detect_btts(browser, 1.80)
    over25 = detect_over25(browser, 1.80)
    print('btts:'+str(btts))
    print('over25:'+str(over25))
    match_info_= []

    if float(btts) < 0 or float(over25) < 0: return match_info_
    
    over05_ht = detect_over05_ht(browser, 1.40)
    if float(over05_ht) < 0: return match_info_

    match = browser.find_element_by_xpath(XPATH_BTTS_MATCH).text
    date  = browser.find_element_by_xpath(XPATH_BTTS_DATE).text
    print('got a match')
    new_match = match_info(match,date,btts,over25,over05_ht)
    print(new_match.to_string())
    match_info_.append(new_match)

    return match_info_

def detect_live_over05ht(browser, min_amount):
    over05_ht = -1

    sleep(delay[randint(0,4)]) # Time in seconds.

    if not xpath_exists(XPATH_LIVE_OVER05_HT_CONTAINER,browser):  # Trying again in case website haven't loaded correctly 
        sleep(delay[randint(0,4)]) # Time in seconds.
        if not xpath_exists(XPATH_LIVE_OVER05_HT_CONTAINER,browser):
            print('ERROR: Couldn\'t find the element: "1ª mitad - Goles"')
            return over05_ht
        #end if
    #end if

    container = browser.find_element_by_xpath(XPATH_LIVE_OVER05_HT_CONTAINER)
    section = container.find_elements_by_xpath('.' + XPATH_OVER05_HT_OPTION)
    i = 0 

    if section[0].text == '0.5': #Index 0 for '0.5 HT' 
        amount = container.find_elements_by_xpath('.'+ XPATH_OVER05_HT_FEE)
        if float(amount[0].text) >= float(min_amount): #Index 0 for '0.5 HT'
            over05_ht = amount[0].text
            print('over 0.5 ht amount: '+over05_ht)
  

    sleep(delay[randint(0,4)]) # Time in seconds.

    return over05_ht

def detect_live_overX(browser, min_amount):
    overX = [-1,'']

    sleep(delay[randint(0,4)]) # Time in seconds.

    if not xpath_exists(XPATH_LIVE_OVER_X_CONTAINER,browser):  # Trying again in case website haven't loaded correctly 
        sleep(delay[randint(0,4)]) # Time in seconds.
        if not xpath_exists(XPATH_LIVE_OVER_X_CONTAINER,browser):
            print('ERROR: Couldn\'t find the element: "Goles en el partido"')
            return overX
        #end if
    #end if

    container = browser.find_element_by_xpath(XPATH_LIVE_OVER_X_CONTAINER)
    section = container.find_elements_by_xpath('.' + XPATH_OVER05_HT_OPTION)
    i = 0 

    overX[1] = section[0].text  
    amount = container.find_elements_by_xpath('.'+ XPATH_OVER05_HT_FEE)
    if float(amount[0].text) >= float(min_amount): #Index 0 for the next goal
        overX[0] = amount[0].text
        print('over X amount: '+overX[0])
  
    sleep(delay[randint(0,4)]) # Time in seconds.

    return overX

def extract_live_matches_information(browser, match_dict):
    print('here')
    WebDriverWait(browser, 150).until(EC.presence_of_element_located((By.XPATH, XPATH_LIVE_NAME)))
    name = browser.find_element_by_xpath(XPATH_LIVE_NAME).text
    min = browser.find_element_by_xpath(XPATH_LIVE_MIN).text
    option = ''
    fee = ''
    time = str(min).split(':')
    ht_checked = False
    ft_checked = False
    minutes = time[0]
    seconds = time[1]
    total_time = float(minutes) + float(seconds) / 60
    live_match_info_ = []
    from_dict = ''
    # Check if match is inside 'match_dict' and storing it in from_dict:
    if name in match_dict:
        from_dict = match_dict.get(name)
    else:
        return live_match_info

    if total_time < 45.0 and not from_dict.is_ht_checked():
        print('under ht')
        fee = detect_live_over05ht(browser, 1.50)
        option = 'OVER 0,5 HT'
        ht_checked = True
    elif total_time >= 45.0 and from_dict.is_ft_checked():
        print('over ht')
        result = detect_live_overX(browser, 1.50)
        fee = result[0]
        option = 'OVER ' + str(result[1])
        ft_checked = True

    if float(fee) < 0: return live_match_info_
    print('got it')
    # else do this:

    e1_ataques = ''
    e2_ataques = ''
    e1_a_peligrosos = ''
    e2_a_peligrosos = ''
    e1_posesion = ''
    e2_posesion = ''
    e1_tiros_puerta = ''
    e2_tiros_puerta = ''
    e1_corners = ''
    e2_corners = ''

    # Extracting information:
    if not xpath_exists(XPATH_LIVE_STATS_TITLE, browser) and not xpath_exists(XPATH_LIVE_STATS,
                                                                              browser): return live_match_info_
    titles = browser.find_elements_by_xpath(XPATH_LIVE_STATS_TITLE)
    stats = browser.find_elements_by_xpath(XPATH_LIVE_STATS)
    corners = browser.find_elements_by_xpath(XPATH_LIVE_CORNERS)
    e1_corners = corners[0].text
    e2_corners = corners[1].text
    i = 0

    # Getting stats depending on the type ('title' in 'titles'), and storing it for each team.
    for title in titles:
        if title.text == 'Attacks':
            e1_ataques = stats[i].find_element_by_xpath('.'+XPATH_LIVE_TEAM_1).text
            e2_ataques = stats[i].find_element_by_xpath('.'+XPATH_LIVE_TEAM_2).text
        elif title.text == 'Dangerous Attacks':
            e1_a_peligrosos = stats[i].find_element_by_xpath('.'+XPATH_LIVE_TEAM_1).text
            e2_a_peligrosos = stats[i].find_element_by_xpath('.'+XPATH_LIVE_TEAM_2).text
        elif title.text == 'Possession %':
            e1_posesion = stats[i].find_element_by_xpath('.'+XPATH_LIVE_TEAM_1).text
            e2_posesion = stats[i].find_element_by_xpath('.'+XPATH_LIVE_TEAM_2).text
        elif title.text == 'On Target':
            e1_tiros_puerta = stats[i].find_element_by_xpath('.'+XPATH_LIVE_TEAM_1).text
            e2_tiros_puerta = stats[i].find_element_by_xpath('.'+XPATH_LIVE_TEAM_2).text
        #end if-elif
        i+=1
    #end for

    corners = ''
    match = live_match_info(name, min, e1_ataques, e1_a_peligrosos, e1_tiros_puerta, e1_corners, e1_posesion,
                            e2_ataques, e2_a_peligrosos, e2_tiros_puerta, e2_corners, e2_posesion, fee, option,
                            ht_checked, ft_checked)

    print(match.to_string())


    return live_match_info_


def get_live_leagues(browser, match_dict):
    #Searching by LEAGUES: 
    WebDriverWait(browser,250).until(EC.presence_of_element_located((By.XPATH, XPATH_LIVE_LEAGUE))) 
    LEAGUES = browser.find_elements_by_xpath(XPATH_LIVE_LEAGUE)
    
    number_of_leagues = len(LEAGUES)
    counter = 0
    go_down = False
    times = 0
    while counter < number_of_leagues:
        if go_down: scroll_down(browser, times)
        WebDriverWait(browser,150).until(EC.presence_of_element_located((By.XPATH, XPATH_LIVE_LEAGUE))) 
        league_elements = browser.find_elements_by_xpath(XPATH_LIVE_LEAGUE)
        if counter >= len(league_elements): break
        league = league_elements[counter]
        league_name = league.find_element_by_xpath('.'+XPATH_LIVE_LEAGUE_NAME)
        msg = LINE + league_name.text + LINE
        print(msg)
        print(counter)
        print(len(LEAGUES))

        #Extracting MATCHES: 
        get_live_matches(browser,msg, league, match_dict)
        counter += 1

    # End while
        

    return 
    
def get_live_matches(browser, msg, league, match_dict):
    print('getting matches')
    try:
        WebDriverWait(browser,15).until(EC.presence_of_element_located((By.XPATH, XPATH_LIVE_MATCH)))
    except:
        return
    MATCHES = league.find_elements_by_xpath('.'+XPATH_LIVE_MATCH)
    print('got matches')
    if xpath_exists(XPATH_MATCH_LIVE_BUTTON, browser): click_match_live(browser)
    #List of matches
    counter = 0
    times = 0
    go_down = False
    matches_information = [] # List of matches 
    while counter < len(MATCHES):
        if go_down: scroll_down(browser, times)
        WebDriverWait(browser,150).until(EC.presence_of_element_located((By.XPATH, XPATH_LIVE_MATCH))) 

        try:
            matches_elements = league.find_elements_by_xpath('.'+XPATH_LIVE_MATCH)
            if counter >= len(matches_elements): break

            match = matches_elements[counter]
            print(match.text)
            sleep(delay[randint(0,4)]) # Time in seconds.
            match.click()
            sleep(delay[randint(0,4)]) # Time in seconds.
        except StaleElementReferenceException:
            counter +=1
            print('ERROR: Match not available anymore') # Error handling 
            continue
        except ElementNotSelectableException:
            #browser.find_element_by_tag_name("html").send_keys(Keys.PAGE_DOWN)
            print('non visible')
            go_down = True
            times += 1
            continue
        # End try-except
        # Extrating match information: 
        sleep(delay[randint(0,4)]) # Time in seconds.
        match_info_ = extract_live_matches_information(browser, match_dict)
        if match_info_: matches_information.extend(match_info_) 
        counter+=1
        print('back') #Flag
        sleep(delay[randint(0,4)]) # Time in seconds.
        click_live_general(browser)
    # End while
 
    messages = []
    messages.append(msg)
    for match in matches_information: messages.append(match.to_string())
    if not matches_information: print('**********False*************') # Flag
    if matches_information: send_msg_by_groups(messages) # Don't send the message if the matches list is empty
    sleep(delay[randint(0,4)]) # Time in seconds.

    return

#Not live matches:
def get_matches(browser, league):
    print('getmatches')
    match_dict = {}

    try:
        WebDriverWait(browser,150).until(EC.presence_of_element_located((By.XPATH, XPATH_MATCH))) 
    except:
        return match_dict
    MATCHES = browser.find_elements_by_xpath(XPATH_MATCH_CONTAINER)
    #List of matches
    counter = 0
    times = 0
    go_down = False
    matches_information = [] # List of matches 
    while counter < len(MATCHES):
        if go_down: scroll_down(browser, times)
        WebDriverWait(browser,150).until(EC.presence_of_element_located((By.XPATH, XPATH_MATCH_CONTAINER))) 
        matches_elements = browser.find_elements_by_xpath(XPATH_MATCH_CONTAINER)
        if counter >= len(matches_elements): break
        match = matches_elements[counter].find_element_by_xpath('.'+XPATH_MATCH)
        msg = LINE + match.text + LINE
        print(msg) # Flag
        sleep(delay[randint(0,4)]) # Time in seconds.
        try:
            match.click()
            sleep(delay[randint(0,4)]) # Time in seconds.

        except ElementNotSelectableException:
            #browser.find_element_by_tag_name("html").send_keys(Keys.PAGE_DOWN)
            go_down = True
            times += 1
            continue
        except StaleElementReferenceException:
            counter +=1
            print('ERROR: Match not available anymore') # Error handling 
            continue
        # End try-except
        # Extrating match information: 
        match_info_ = extract_matches_information(browser)
        if match_info_: matches_information.extend(match_info_)
        counter+=1
        print('back') #Flag
        sleep(delay[randint(0,4)]) # Time in seconds.
        browser.back()
    # End while

    messages = []
    messages.append(league)
    for match in matches_information: messages.append(match.to_string())
    if not matches_information: print('**********False*************') # Flag
    if matches_information: send_msg_by_groups(messages) # Don't send the message if the matches list is empty
    sleep(delay[randint(0,4)]) # Time in seconds.

    add_match_list_to_dictionary(matches_information,match_dict)
    return match_dict

def scroll_down(browser, times):
    
    # Scroll down using PAGE_DOWN button
    for i in range(times):
        browser.find_element_by_tag_name("html").send_keys(Keys.PAGE_DOWN)

    return

def save_in_file(file_name, object):
    # open the file for writing
    fileObject = open(file_name, 'wb')

    # this writes the object 'object' to the
    # file named 'testfile'
    pickle.dump(object, fileObject)

    # here we close the fileObject
    fileObject.close()

def load_from_file(file_name):
    # we open the file for reading
    fileObject = open(file_name, 'rb')
    # load the object from the file into var b
    object = pickle.load(fileObject)

    return object

def delete_file_content(fName):
    fileObject = open(fName, 'w')
    fileObject.close()

    return

def test():

    url = 'https://www.bet365.es/'
    browser = open_website(url) 
    click_futbol_section(browser)
    scroll_down(browser)

    return;

def main2():

    return

def main():
    import traceback
    url = 'https://www.bet365.com/'
    browser = open_website(url)
    click_español(browser)
    print('clicked "English"')
    sleep(delay[randint(0,4)]) # Time in seconds.
    set_decimal_odds(browser)
    number_of_errors = 0
    match_dict = {}
    dict_updated = True
    file_name = "./matchesFile.txt"
    tomorrow = date.today() + timedelta(days=1)
    tomorrow_0h = datetime.now() #datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)

    while True:
        sleep(30) # 30 secs
        try:
            print('Clicking soccer button')
            now = datetime.now()
            click_home_button(browser)
            print(now >= tomorrow_0h)
            if now >= tomorrow_0h:
                dict_updated = False
                delete_file_content(file_name)
                print('pregames')
                # Updating match_dict
                match_dict.clear()
                match_dict.update(get_leagues(browser))
                # Saving match_dict in a file:
                dict_updated = True
                save_in_file(file_name,match_dict)
                dict_updated = True
                # Updating tomorrows date:
                tomorrow = date.today() + timedelta(days=1)
                tomorrow_0h = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
            print("im here")
            if dict_updated == True:
                print("loading file")
                match_dict = load_from_file(file_name)

            if not match_dict: #Checking if the dictionary is empty
                print('Empty dictionary. Trying again')
                continue
            print('live')
            click_futbol_section(browser)
            click_live_button(browser)
            get_live_leagues(browser, match_dict)
        except Exception:
            print(traceback.print_exc())
            number_of_errors+=1
            continue
        finally:
            if number_of_errors > 2:
                bot_send_msg_to("something happened D:", JAVIER_ID)
                browser.save_screenshot("error_screenshot.png")
                number_of_errors = 0

        #end try-except
        print("ending while")
        sleep(5*60)

    #end while

    warn_msg = "WARNING: Something happened. Please, check the bot"
    print(warn_msg)
    bot_send_msg(warn_msg)
    return

def test_bot():
    btts = [match_info('bcn-madrid','19-03-05','yes','12',BTTS_STRING),match_info('bcn-madrid','19-03-05','yes','12',OVER25_STRING)]
    msg = []
    for item in btts:
        msg.append(item.to_string())
        print(item.to_string())
    send_msg_by_groups(msg)
    return

if __name__ == '__main__': main()
  
