import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException   
from selenium.common.exceptions import ElementNotSelectableException  
from selenium.common.exceptions import StaleElementReferenceException  
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from time import sleep
from random import randint

delay = [1,2,1.5,2,2.3]
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
#OVER 2.5:
OVER25_STRING = 'OVER 2,5'
XPATH_OVER25_CONTAINER = '//span[contains(., "Goles - M")]/ancestor::div[starts-with(@class,"gl-MarketGroup ")]'
XPATH_OVER25_SECTION = '//div[starts-with(@class,"gl-MarketValuesExplicit2 gl-Market_General gl-Market_PWidth-37-5 ")]'
XPATH_OVER25_OPTION = '//span[@class="gl-ParticipantRowValue_Name"]'
XPATH_OVER25_FEE = '//span[@class="gl-ParticipantOddsOnly_Odds"]'
#OVER 0.5 HT:
OVER05_HT_STRING = 'OVER 0.5 HT'
XPATH_OVER05_HT_CLICK_SECTION = '//div[@class="cl-MarketGroupNavBarButton " and contains(.,"1ª/2ª mitad")]'
XPATH_OVER05_HT_CONTAINER = '//span[contains(., "1º tiempo - Goles")]/ancestor::div[starts-with(@class,"gl-MarketGroup ")]'
XPATH_OVER05_HT_OPTION = '//span[@class="gl-ParticipantRowValue_Name"]'
XPATH_OVER05_HT_FEE = '//span[@class="gl-ParticipantOddsOnly_Odds"]'


class match_info:
    # Constructor
    def __init__(self,match_name_,date_,btts_,over25_,over05ht_):
        # Variables initialization
        self.match_name         = match_name_
        self.date               = date_
        self.btts_amount        = btts_
        self.over25_amount      = over25_
        self.over05_ht_amount   = over05ht_

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
    options.add_argument("--start-maximized")
    #browser = webdriver.Chrome(ChromeDriverManager().install())
    # TODO: Catch exception when unable to open website
    browser             = webdriver.Chrome('.\chromedriver.exe',options=options)
    browser.get(url)
    wait = WebDriverWait(browser, 6000) 
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
    btts = -1
    
    if not xpath_exists(XPATH_BTTS_CONTAINER,browser):  # Trying again in case website haven't loaded correctly 
        sleep(delay[randint(0,4)]) # Time in seconds.
        if not xpath_exists(XPATH_BTTS_CONTAINER,browser):
            print('ERROR: Couldn\'t find the element: "Ambos equipos anotarán"')
            return btts
        #end if
    #end if
    container = browser.find_element_by_xpath(XPATH_BTTS_CONTAINER)
    section = container.find_elements_by_xpath('.'+XPATH_BTTS_OPTION)
    for item in section:
        yes_or_no   = item.find_element_by_xpath('.'+XPATH_BTTS_YES_NO).text
        fee         = item.find_element_by_xpath('.'+XPATH_BTTS_FEE).text
        if float(fee) >= 1.8 and str(yes_or_no) == 'Sí':
            btts = fee
        else:
            continue
        #end if-else
    #end for

    return btts

def detect_over25(browser):
    over25 = -1

    if not xpath_exists(XPATH_OVER25_CONTAINER,browser):  # Trying again in case website haven't loaded correctly 
        sleep(delay[randint(0,4)]) # Time in seconds.
        if not xpath_exists(XPATH_OVER25_CONTAINER,browser):
            print('ERROR: Couldn\'t find the element: "Goles - Más/Menos que"')
            return over25
        #end if
    #end if

    container = browser.find_element_by_xpath(XPATH_OVER25_CONTAINER)
    section = container.find_elements_by_xpath('.'+XPATH_OVER25_SECTION)
    for item in section:
        option      = container.find_element_by_xpath('.'+XPATH_OVER25_OPTION).text
        fee         = item.find_element_by_xpath('.'+XPATH_OVER25_FEE).text
        if float(fee) >= 1.8 and option == '2.5':
            over25 = fee
        else:
            continue
        #end if-else
    #end for    
    return over25

def detect_over05_ht(browser):
    over05_ht = -1
    if not xpath_exists(XPATH_OVER05_HT_CLICK_SECTION,browser):
        print('ERROR: Couldn\'t find the element: "1ª/2ª mitad2"')
        return over05_ht

    print('Clicking')
    sleep(delay[randint(0,4)]) # Time in seconds.
    browser.find_element_by_xpath(XPATH_OVER05_HT_CLICK_SECTION).click()
    print('clicked')
    sleep(delay[randint(0,4)]) # Time in seconds.
    
    if not xpath_exists(XPATH_OVER05_HT_CONTAINER,browser):  # Trying again in case website haven't loaded correctly 
        sleep(delay[randint(0,4)]) # Time in seconds.
        if not xpath_exists(XPATH_OVER05_HT_CONTAINER,browser):
            print('ERROR: Couldn\'t find the element: "1° tiempo - Goles"')
            browser.back()
            return over05_ht
        #end if
    #end if

    container = browser.find_element_by_xpath(XPATH_OVER05_HT_CONTAINER)
    section = browser.find_elements_by_xpath('.'+XPATH_OVER05_HT_OPTION)
    i = 0 
    if section[1].text == '0.5': #Index 1 for '0.5 HT' 
        amount = container.find_elements_by_xpath('.'+ XPATH_OVER05_HT_FEE)
        if float(amount[0].text) >= 1.40: #Index 0 for '0.5 HT'
            over05_ht = amount[0].text
            print(over05_ht)
  

    browser.back()
    sleep(delay[randint(0,4)]) # Time in seconds.

    return over05_ht

def extract_matches_information(browser):
    print('Looking for matches')
    print('->match')
    btts = detect_btts(browser)
    over25 = detect_over25(browser)
    print('btts:'+str(btts))
    print('over25:'+str(over25))
    match_info_= []

    if float(btts) < 0 or float(over25) < 0: return match_info_
    
    over05_ht = detect_over05_ht(browser)
    if float(over05_ht) < 0: return match_info_

    match = browser.find_element_by_xpath(XPATH_BTTS_MATCH).text
    date  = browser.find_element_by_xpath(XPATH_BTTS_DATE).text
    print('got a match')
    new_match = match_info(match,date,btts,over25,over05_ht)
    print(new_match.to_string())
    match_info_.append(new_match)

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

def scroll_down(browser, times):
    
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

    url = 'https://www.bet365.com/'
    browser = open_website(url)
    print('Website opened')
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
  
