import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver

class Comment:
    def __init__(self, over, description):
        self.paragraphs = []

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph)

def get_team_name_and_score(soup, top_list_item_class_name):
    TEAM_NAME_CLASS_NAME = "cscore_team icon-font-after"
    TEAM_SPAN_CLASS_NAME = "cscore_name cscore_name--long"
    SCORE_CLASS_NAME = "cscore_score"

    team = soup.find("li", {"class":top_list_item_class_name}).find("div", TEAM_NAME_CLASS_NAME)
    team_name = team.a.find("span", {"class":TEAM_SPAN_CLASS_NAME}).text
    team_mini_score = team.find("div", {"class":SCORE_CLASS_NAME}).text

    return team_name, team_mini_score

def get_commentary(soup):
    root_div_tags_children = soup.find("div", {"class":"content"})
    commentary = []

    for commentary_item in root_div_tags_children:
        over = commentary_item.find("div", {"class":"time-stamp"})
        description = commentary_item.find("div", {"class":"description"})
        # print("over : {}, desc : {}\n".format(over, description))

        if (over is None):
            over = "-"
        else:
            over = over.text

        if (description is None):
            description = "-"
        else:
            description = description.text

        # if (over is not None and description is not None):
        comment = Comment(over, description)
        paragraphs = commentary_item.findAll("p", {"class":"comment"})

        if (paragraphs is not None):
            for p in paragraphs:
                comment.add_paragraph(p.text)

        commentary.append(comment)

    return commentary

def get_latest_commentary_from_espn(last_timestamp):
    MATCH_URL = "http://www.espncricinfo.com/series/18693/commentary/1144993/australia-vs-india-1st-test-india-in-aus-2018-19"
    FIRST_TEAM_TOP_LIST_ITEM_CLASS_NAME = "cscore_item cscore_item--home"
    SECOND_TEAM_TOP_LIST_ITEM_CLASS_NAME = "cscore_item cscore_item--away"

    request = urllib.request.Request(MATCH_URL)
    response = urllib.request.urlopen(request)

    page_content = response.read().decode("utf-8")
    soup = BeautifulSoup(page_content, "html.parser")

    first_team_name, first_team_mini_score = get_team_name_and_score(soup, FIRST_TEAM_TOP_LIST_ITEM_CLASS_NAME)
    print("{} - {}".format(first_team_name, first_team_mini_score))

    second_team_name, second_team_mini_score = get_team_name_and_score(soup, SECOND_TEAM_TOP_LIST_ITEM_CLASS_NAME)
    print("{} - {}".format(second_team_name, second_team_mini_score))

    commentary = get_commentary(soup)

    for comment in commentary:
        print("Commentary : {}\n".format(comment))

    return first_team_mini_score

def get_latest_commentary(last_timestamp):
    SCORE_CLASS_NAME = "cb-min-bat-rw"
    MINI_SCORE_SPAN_CLASS_NAME = "cb-font-20 text-bold"
    SOURCE_URL = "https://www.cricbuzz.com/live-cricket-scores/20301/aus-vs-ind-1st-test-india-tour-of-australia-2018-19"

    request = urllib.request.Request(SOURCE_URL)
    response = urllib.request.urlopen(request)

    page_content = response.read().decode("utf-8")
    soup = BeautifulSoup(page_content, "html.parser")
    # data = soup.find("div", {"class":"{}".format(SCORE_CLASS_NAME)})

    for data in soup.findAll("div", {"class":"{}".format(SCORE_CLASS_NAME)}):
        for item in data.findAll("span", {"class":"{}".format(MINI_SCORE_SPAN_CLASS_NAME)}):
            first_team_mini_score = item.text

    for data in soup.findAll("div", {"ng-init":"comm = match.commentary"}):
        print(data)
        break

    return first_team_mini_score

def send_messages():
    URL = "https://web.whatsapp.com"
    MESSAGE_BOX_CLASS_NAME = "_1Plpp"
    SEND_BUTTON_CLASS_NAME = "_35EW6"

    driver = webdriver.Safari()
    driver.get(URL)

    name = input("Enter the name of the group/user you want to text : ")
    user = driver.find_element_by_xpath("//span[@title = \"{}\"]".format(name))
    user.click()

    message_box = driver.find_element_by_class_name(MESSAGE_BOX_CLASS_NAME)
    count = 50

    for i in range(count):
        message_box.send_keys("test {}".format(i + 1))
        send_button = driver.find_element_by_class_name(SEND_BUTTON_CLASS_NAME)
        send_button.click()

if __name__ == "__main__":
    # send_messages()
    # latest_commentary = get_latest_commentary(None)
    # print(latest_commentary)

    espn_commentary = get_latest_commentary_from_espn(None)
    print(espn_commentary)
