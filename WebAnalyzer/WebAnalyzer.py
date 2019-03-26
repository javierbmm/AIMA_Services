import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException   
from selenium.common.exceptions import ElementNotSelectableException  
from selenium.common.exceptions import StaleElementReferenceException  
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from time import sleep
from random import randint

delay = [1,2,1.5,0.7,2.3]
LINE = "\n--------------------------------------------\n"
#Users ID's: 
AIMA_ID = '700187299'   #AIMA_Services
JAVIER_ID = '394580187' #Javier Merida
#List of XPath's:
XPATH_SECTION = '//div[starts-with(@class, "lpdgl")]'
XPATH_LEAGUE = '//div[contains(@class,"sm-CouponLink_Label")]'
XPATH_MATCH  = '//div[starts-with(@class,"sl-CouponParticipantWithBookCloses_Name ")]'
XPATH_MATCH_CONTAINER = '//div[@class= "sl-CouponParticipantWithBookCloses sl-CouponParticipantIPPGBase "]'
XPATH_LIVE_MATCH = '//div[@class="sl-CouponParticipantWithBookCloses sl-CouponParticipantIPPGBase \
sl-MarketCouponAdvancedBase_LastChild sl-CouponParticipantWithBookCloses_ClockPaddingLeft "'
XPATH_HOME = '//'
XPATH_ESPAÑOL = '//div[contains(text(), "Fútbol")]'
#BTTS:
BTTS_STRING = 'BTTS'
XPATH_BTTS_CONTAINER = '//span[contains(text(), "Ambos equipos anotarán")]/ancestor::div[@class="gl-MarketGroup "]' 
XPATH_BTTS = '//span[contains(text(), "Ambos equipos anotarán")]' # Useless
XPATH_BTTS_OPTION = '//div[@class="gl-Participant gl-Participant_General gl-Market_CN-2 "]'
XPATH_BTTS_FEE = '//span[@class="gl-Participant_Odds"]'
XPATH_BTTS_YES_NO = '//span[@class="gl-Participant_Name"]'
XPATH_BTTS_MATCH = '//span[starts-with(@class,"cl-EnhancedDropDown ")]'
XPATH_BTTS_DATE = '//div[starts-with(@class,"cm-MarketGroupExtraData_TimeStamp ")]'
XPATH_CLOCK = '//div[@class="pi-CouponParticipantClockInPlay_GameTimerWrapper "]'
#OVER 2,5:
OVER25_STRING = 'OVER 2,5'
XPATH_OVER25_CONTAINER = '//span[contains(., "Goles - M")]/ancestor::div[starts-with(@class,"gl-MarketGroup ")]'
XPATH_OVER25_SECTION = '//div[starts-with(@class,"gl-MarketValuesExplicit2 gl-Market_General gl-Market_PWidth-37-5 ")]'
XPATH_OVER25_OPTION = '//div[@class="gl-MarketColumnHeader "]'
XPATH_OVER25_FEE = '//span[@class="gl-ParticipantOddsOnly_Odds"]'

class match_info:
    # Constructor
    def __init__(self,match_name_,date_,option_,fee_,type_):
        # Variables initialization
        self.match_name = match_name_
        self.date       = date_
        self.option     = option_
        self.fee        = fee_
        self.type       = type_

    def to_string(self):
        string = '\n***MATCH: '+str(self.match_name)+'***\n***TYPE: '+self.type
        string +='***\n***-Date:*** '+str(self.date)+'\n***-Option:*** '+str(self.option)+'\n***-Amount:*** '+str(self.fee)
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

def open_website(url):
    # url                 = 'https://www.bet365.es/#/HO/'
    options             = Options()
    #options.headless    = True
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    options.add_argument("user-agent="+user_agent)
    browser             = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    #wait = WebDriverWait(browser, 6000) 
    sleep(delay[randint(0,4)]) # Time in seconds.

    return browser

def click_futbol_section(browser):
    #Navigation:
    sleep(delay[randint(0,4)]) # Time in seconds.
    browser.find_element_by_link_text("Español").click()
    sleep(delay[randint(0,4)]) # Time in seconds.
    WebDriverWait(browser,150).until(EC.presence_of_element_located((By.XPATH, XPATH_ESPAÑOL))) 

    futbol_section = browser.find_element_by_xpath(XPATH_ESPAÑOL)
    sleep(delay[randint(0,4)]) # Time in seconds.
    futbol_section.click()
    
    sleep(delay[randint(0,4)]) # Time in seconds.

    return

def get_leagues(browser):
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
            counter += 1
        except ElementNotSelectableException:
            browser.find_element_by_tag_name("html").send_keys(Keys.PAGE_DOWN)
            go_down = True
            times += 1
        except StaleElementReferenceException:
             counter +=1
             print('ERROR: League is not available anymore')
        # End try-except

        #Extracting MATCHES: 
        get_matches(browser,msg)
    # End while
        
    browser.quit()

    return 

def xpath_exists(xpath,browser):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def detect_btts(browser):
    btts = []
    if not xpath_exists(XPATH_BTTS_CONTAINER,browser): 
        print('ERROR: Couldn\'t find the element: "Ambos equipos anotarán"')
        return btts
    container = browser.find_element_by_xpath(XPATH_BTTS_CONTAINER)
    section = container.find_elements_by_xpath('.'+XPATH_BTTS_OPTION)
    for item in section:
        if float(item.find_element_by_xpath('.'+XPATH_BTTS_FEE).text) >= 1.8:
            yes_or_no   = item.find_element_by_xpath('.'+XPATH_BTTS_YES_NO).text
            fee         = item.find_element_by_xpath('.'+XPATH_BTTS_FEE).text
            match       = browser.find_element_by_xpath(XPATH_BTTS_MATCH).text
            date        = browser.find_element_by_xpath(XPATH_BTTS_DATE).text
            btts.append(match_info(match,date,yes_or_no,fee,BTTS_STRING))

    return btts

def detect_over25(browser):
    over25 = []
    if not xpath_exists(XPATH_OVER25_CONTAINER,browser): 
        print('ERROR: Couldn\'t find the element: "Goles - Más/Menos que"')
        return over25
    container = browser.find_element_by_xpath(XPATH_OVER25_CONTAINER)
    section = container.find_elements_by_xpath('.'+XPATH_OVER25_SECTION)
    for item in section:
        if float(item.find_element_by_xpath('.'+XPATH_OVER25_FEE).text) >= 1.8:
            option      = item.find_element_by_xpath('.'+XPATH_OVER25_OPTION).text
            fee         = item.find_element_by_xpath('.'+XPATH_OVER25_FEE).text
            match       = browser.find_element_by_xpath(XPATH_BTTS_MATCH).text  # XPath for match is the same as BTTS 
            date        = browser.find_element_by_xpath(XPATH_BTTS_DATE).text   # XPath for date is the same as BTTS
            over25.append(match_info(match,date,option,fee,OVER25_STRING))

    return over25

def extract_matches_information(browser):
    print('Looking for matches')
    print('->match')
    match_info_= []
    match_info_.extend(detect_btts(browser))
    match_info_.extend(detect_over25(browser))

    return match_info_


#Not live matches:
def get_matches(browser, league):
    WebDriverWait(browser,150).until(EC.presence_of_element_located((By.XPATH, XPATH_MATCH))) 
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
    browser.back()

    return

def  scroll_down(browser, times):
    
    # Scroll down using PAGE_DOWN button
    for i in range(times):
        browser.find_element_by_tag_name("html").send_keys(Keys.PAGE_DOWN)

    return

def test():

    url = 'https://www.bet365.es/'
    browser = open_website(url)
    click_futbol_section(browser)
    scroll_down(browser)

    return;

def main():

    url = 'https://www.bet365.es/'
    try:
        browser = open_website(url)
    except:
        print('ERROR: Unable to open website ', url) # Error handling 
    click_futbol_section(browser)
    get_leagues(browser)

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
  
