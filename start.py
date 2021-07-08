from __future__ import print_function


from linkedIn import search_and_send_request, get_list_follows, get_list_connections, set_driver_path
from linkedIn import shutdown
from linkedIn import withdrawConnectionRequests

#These are the variables used to connect to your linkedin and find the right people

username = '' #The Email that you use to sign in to LinkedIn
password = '' #The Password that you use to sign in to LinkedIn
titles = ['president'] #The title of the people you are trying to seek
keywords = ['chef', 'cook'] #Some keywords for the industry of the people you are trying to seek
location = '%5B"103644278"%5D' #When you search for people on LinkedIn, you can select a location. When you do,
#you get a geoUrn. This code is what goes here. The current geoUrn is for the United States
not_accepted_keyword_array = ['sale', 'account', 'sell'] #Any keywords that you would like to stay away from. You can
#place any keyword here including business you want to avoid, or positions.
chromedriver_path = 'C:\\path\\to\\chromedriver.exe' #Download the proper version of chromedriver,
#https://chromedriver.chromium.org/downloads  Then you will need to place the full path on your local machine here.


def linkedin_connect_process():
    global username, password, titles, keywords, location, not_accepted_keyword_array
    #withdrawConnectionRequests(username, password) #UnComment this to go through the Withdraw sequence.
    for title in titles:
        for keyword in keywords:
            search_and_send_request(title + " " + keyword, 100, username, password, 0.01, location, not_accepted_keyword_array)
    shutdown()


#  Experimental, When it does work it calculates which people in your network
#  are not following you, but are in your network.
def linkedin_find_connections_not_following():
    global username, password, titles, keywords
    followers = get_list_follows(username, password)
    for follower in followers:
        print(follower.text)


#linkedin_find_connections_not_following()

set_driver_path(chromedriver_path)

linkedin_connect_process() #Start the Bot
