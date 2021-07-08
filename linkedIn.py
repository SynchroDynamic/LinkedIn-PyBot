import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

chromedriver_path = ''
driver = None


def set_driver_path(path):
    global chromedriver_path
    chromedriver_path = path


def irregularWait(maxWait):
    time.sleep(random.randint(0, maxWait))


def standardWait(wait):
    time.sleep(wait)


def turn_on_driver(username, password):
    if driver is None:
        login(username, password)


def get_list_connections(username, password):
    turn_on_driver(username, password)
    query_url = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'
    driver.get(query_url)
    reached_page_end = False
    last_height = driver.execute_script("return document.body.scrollHeight")

    while not reached_page_end:
        while not reached_page_end:
            driver.find_element_by_xpath('//body').send_keys(Keys.END)
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            standardWait(0.5)
            if last_height == new_height:
                reached_page_end = True
            else:
                last_height = new_height
        standardWait(5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height != new_height:
            reached_page_end = False
            last_height = new_height
    return driver.find_elements_by_class_name('mn-connection-card__name')


def get_list_follows(username, password):
    turn_on_driver(username, password)
    query_url = 'https://www.linkedin.com/feed/followers/'
    driver.get(query_url)
    reached_page_end = False
    last_height = driver.execute_script("return document.body.scrollHeight")

    while not reached_page_end:
        while not reached_page_end:
            driver.find_element_by_xpath('//body').send_keys(Keys.END)
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                reached_page_end = True
            else:
                last_height = new_height
        standardWait(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if last_height != new_height:
            reached_page_end = False
            last_height = new_height
    return driver.find_elements_by_class_name('follows-recommendation-card__name')

# Functions
def search_and_send_request(keywords, till_page, username, password, excepted_keyword_density, location, not_accepted_keyword_array):
    noWarning = True
    turn_on_driver(username, password)
    for page in range(1, till_page + 1):
        if noWarning:
            query_url = 'https://www.linkedin.com/search/results/people/?geoUrn=' + location + '&keywords=' + keywords + '&origin=FACETED_SEARCH&page=' + str(page)
            driver.get(query_url)
            keyword_array = keywords.split()
            irregularWait(5)
            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            irregularWait(5)
            linkedin_urls = driver.find_elements_by_class_name('artdeco-button__text')
            linkedin_tagline = driver.find_elements_by_class_name('entity-result__primary-subtitle')
            # print('INFO: %s connections found on page %s' % (len(linkedin_urls), page))
            # print("ENTITIES: ", len(linkedin_tagline))
            count = 0
            tagCount = 0
            for connection in linkedin_urls:
                try:
                    # print("TAGLINE: ", linkedin_tagline[tagCount].text)
                    tagtolower = linkedin_tagline[tagCount].text.lower()
                    buttonText = connection.text
                    tag_array = tagtolower.split()
                    numerator = 0
                    denominator = len(keyword_array)
                    for keyword in keyword_array:
                        # print(keyword, "in Array?: ", tag_array)
                        if keyword in tag_array:
                            numerator += 1
                    keyword_density = numerator / denominator

                    if connection.text == 'Connect':
                        irregularWait(1)
                        # print(keyword_density)
                        # print(excepted_keyword_density)
                        reject = False

                        for unacceptable_keyword in not_accepted_keyword_array:
                            if tagtolower.find(unacceptable_keyword) > -1:
                                reject = True

                        if tagtolower.find('sale') > -1 or tagtolower.find('account') > -1 or tagtolower.find('msc') > -1  or tagtolower.find('fastenal') > -1:
                            print('Rejecting -> ' + tagtolower)
                        elif keyword_density >= excepted_keyword_density:
                            coordinates = connection.location_once_scrolled_into_view  # returns dict of X, Y coordinates
                            driver.execute_script("window.scrollTo(%s, %s);" % (coordinates['x'], coordinates['y']))
                            # text = str(connection.get_attribute('aria-label'))
                            # print("INFO: %s" % (text))
                            irregularWait(5)
                            connection.click()
                            irregularWait(5)
                            # ip-fuse-limit-alert__warning ip-fuse-limit-alert__warning--full
                            if driver.find_elements_by_class_name('artdeco-button--primary')[0].is_enabled():
                                driver.find_elements_by_class_name('artdeco-button--primary')[0].click()
                            else:
                                driver.find_elements_by_class_name('artdeco-modal__dismiss')[0].click()
                            irregularWait(2)
                            if driver.find_elements_by_class_name('warning--full')[0].is_enabled():
                                noWarning = False
                                break
                    if buttonText == 'Connect' or buttonText == 'Message' or buttonText == 'Pending':
                        tagCount += 1
                        # print("TagCount: ", tagCount)
                    count += 1

                except Exception as e:
                    print('ERROR: %s' % (e))
                    irregularWait(5)
        else:
            break


def withdrawConnectionRequests(username, password):
    if driver is None:
        login(username, password)
    for page in range(1, 3):
        # print('\nINFO: Checking on page %s' % (page))
        query_url = 'https://www.linkedin.com/mynetwork/invitation-manager/sent/?invitationType=&page=' + str(page)
        driver.get(query_url)
        irregularWait(1)
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        irregularWait(1)
        linkedin_urls = driver.find_elements_by_class_name('artdeco-button--tertiary')
        linkedin_time = driver.find_elements_by_class_name('time-ago')
        # print('INFO: %s connections found on page %s' % (len(linkedin_urls), page))
        count = 0
        for connection in linkedin_time:
            # print(connection)
            ar = connection.text.split(' ')
            if ar[1] == 'days' or ar[1] == 'weeks' or ar[1] == 'week' or ar[1] == 'months' or ar[1] == 'month':
                if int(ar[0]) > 3 or ar[1] != 'days':
                    try:
                        coordinates = linkedin_urls[count].location_once_scrolled_into_view  # returns dict of X, Y coordinates
                        driver.execute_script("window.scrollTo(%s, %s);" % (coordinates['x'], coordinates['y']))
                        # text = str(linkedin_urls[count].get_attribute('aria-label'))
                        # print("INFO: %s" % (text))
                        linkedin_urls[count].click()
                        driver.find_elements_by_class_name('artdeco-button--primary')[0].click()

                    except Exception as e:
                        print('ERROR: %s' % (e))
                        break
            count += 1


def login(username, password):
    global chromedriver_path
    # Login
    d = webdriver.Chrome(chromedriver_path)
    # d = webdriver.PhantomJS()
    d.get('https://www.linkedin.com/login')
    d.find_element_by_id('username').send_keys(username)
    d.find_element_by_id('password').send_keys(password)
    d.find_element_by_xpath('//*[@type="submit"]').click()
    global driver
    driver = d
    irregularWait(5)
    # name = driver.find_elements_by_class_name('profile-rail-card__actor-link')[0].text.replace(' ', '')


def shutdown():
    # Close browser
    driver.quit()
