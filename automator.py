import urllib.request
import schedule
import time
from bs4 import BeautifulSoup
from selenium import webdriver

class Match:
    def __init__(self, first_team, second_team, first_team_score, second_team_score):
        self.first_team = first_team
        self.second_team = second_team
        self.first_team_score = first_team_score
        self.second_team_score = second_team_score
        self.commentary = []

    def __repr__(self):
        return str(self.__dict__)

class Comment:
    def __init__(self, over, description):
        self.over = over
        self.description = description
        self.paragraphs = []

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)

    def __repr__(self):
        # return str(self.__dict__)
        return "over : {}, desc : {}, paras : {}".format(self.over, self.description, self.paragraphs)

def get_team_name_and_score(soup, top_list_item_class_name):
    TEAM_NAME_CLASS_NAME = "cscore_team icon-font-after"
    TEAM_SPAN_CLASS_NAME = "cscore_name cscore_name--long"
    SCORE_CLASS_NAME = "cscore_score"

    team = soup.find("li", {"class":top_list_item_class_name}).find("div", TEAM_NAME_CLASS_NAME)
    team_name = team.a.find("span", {"class":TEAM_SPAN_CLASS_NAME}).text
    team_score = team.find("div", {"class":SCORE_CLASS_NAME}).text

    return team_name, team_score

def get_commentary(soup):
    root_div_tags_children = soup.find("div", {"class":"content"})
    commentary = []

    for commentary_item in root_div_tags_children:
        over = commentary_item.find("div", {"class":"time-stamp"})
        description = commentary_item.find("div", {"class":"description"})

        if (over is None):
            over = ""
        else:
            over = over.text

        if (description is None):
            description = ""
        else:
            description = description.text

        comment = Comment(over, description)
        paragraphs = commentary_item.findAll("p", {"class":"comment"})

        if (paragraphs is not None):
            for p in paragraphs:
                comment.add_paragraph(p.text)

        if (len(over) != 0 or len(description) != 0 or len(comment.paragraphs) != 0):
            commentary.append(comment)

    commentary.reverse()

    return commentary

"""Function to parse ESPN's Cricinfo website, and fetch match details using other functions.

Can use the last_timestamp variable to get comments made only after the timestamp of the last comment fetched previously,
but there are no timestamp fields in the HTML, and anyway the site loads just a few comments, while more load on the go
by scrolling, so there's no desperate need to implement this for now.
"""
def get_match_info_from_espn(last_timestamp):
    MATCH_URL = "http://www.espncricinfo.com/series/18693/commentary/1144993/australia-vs-india-1st-test-india-in-aus-2018-19"
    FIRST_TEAM_TOP_LIST_ITEM_CLASS_NAME = "cscore_item cscore_item--home"
    SECOND_TEAM_TOP_LIST_ITEM_CLASS_NAME = "cscore_item cscore_item--away"

    request = urllib.request.Request(MATCH_URL)
    response = urllib.request.urlopen(request)

    page_content = response.read().decode("utf-8")
    soup = BeautifulSoup(page_content, "html.parser")

    first_team_name, first_team_score = get_team_name_and_score(soup, FIRST_TEAM_TOP_LIST_ITEM_CLASS_NAME)
    second_team_name, second_team_score = get_team_name_and_score(soup, SECOND_TEAM_TOP_LIST_ITEM_CLASS_NAME)
    match = Match(first_team_name, second_team_name, first_team_score, second_team_score)
    match.commentary = get_commentary(soup)

    return match

def get_match_info():
    match = get_match_info_from_espn(None)
    info_string = "*{} - {}*".format(match.first_team, match.first_team_score)
    info_string += "\n*{} - {}*".format(match.second_team, match.second_team_score)
    
    for comment in match.commentary:
        info_string += "\n*{}* - {}".format(comment.over, comment.description)

        if (len(comment.paragraphs) > 0):
            for p in comment.paragraphs:
                info_string += "\n{}".format(p)

    return info_string

def scheduled_job(driver, names):
    MESSAGE_BOX_CLASS_NAME = "_1Plpp"
    SEND_BUTTON_CLASS_NAME = "_35EW6"
    message_content = get_match_info()

    for name in names:
        user = driver.find_element_by_xpath("//span[@title = \"{}\"]".format(name))
        user.click()
        
        message_box = driver.find_element_by_class_name(MESSAGE_BOX_CLASS_NAME)
        message_box.send_keys(message_content)

        send_button = driver.find_element_by_class_name(SEND_BUTTON_CLASS_NAME)
        send_button.click()

def send_messages_on_whatsapp():
    URL = "https://web.whatsapp.com"

    driver = webdriver.Safari()
    driver.get(URL)

    user_input = input("Enter the names of the groups/users you want to text, separated by commas(Eg. - Arya, Sansa, Jon, Bran, Rickon, Robb) : ")
    names = [x.strip() for x in user_input.split(',')]

    scheduled_job(driver, names)
    schedule.every(5).minutes.do(scheduled_job, driver, names)
    # schedule.every(30).seconds.do(scheduled_job, driver, message_box)

    while (True):
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    send_messages_on_whatsapp()
