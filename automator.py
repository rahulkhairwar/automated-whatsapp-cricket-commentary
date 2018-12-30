import urllib.request
import schedule
import datetime
import time
import properties
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

match_start_time = ""
match_end_time = ""
last_comment = ""
has_updates = True
LOGGER = ""

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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def __repr__(self):
        # return str(self.__dict__)
        return "over : {}, desc : {}, paras : {}".format(self.over, self.description, self.paragraphs)


# class Logger(logging.getLoggerClass()):
class Logger():
    def __init__(self, log_filename):
        logging.basicConfig(filename=log_filename, level=logging.DEBUG)

    def debug_with_time(self, message):
        logging.debug("{} => {}".format(get_current_time(), message))
    
    def debug(self, message):
        logging.debug(message)

    def info_with_time(self, message):
        logging.info("{} => {}".format(get_current_time(), message))

    def info(self, message):
        logging.info(message)

    def error_with_time(self, message):
        logging.error("{} => {}".format(get_current_time(), message))

    def error(self, message):
        logging.error(message)

    def exception_with_time(self, message):
        logging.exception("{} => {}".format(get_current_time(), message))

    def exception(self, message):
        logging.exception(message)


def get_current_time():
    return datetime.datetime.now()


def get_team_name_and_score(soup, top_list_item_class_name):
    TEAM_NAME_CLASS_NAME = "cscore_team icon-font-after"
    TEAM_SPAN_CLASS_NAME = "cscore_name cscore_name--long"
    SCORE_CLASS_NAME = "cscore_score"

    team = soup.find("li", {"class": top_list_item_class_name}).find(
        "div", TEAM_NAME_CLASS_NAME)
    team_name = team.a.find("span", {"class": TEAM_SPAN_CLASS_NAME}).text
    team_score = team.find("div", {"class": SCORE_CLASS_NAME}).text

    return team_name, team_score


def get_commentary(soup):
    global last_comment
    global has_updates

    root_div_tags_children = soup.find(
        "article", {"class": "sub-module match-commentary cricket"})

    if (root_div_tags_children is None):
        root_div_tags_children = soup.find(
            "article", {"class": "sub-module match-commentary cricket add-padding"})

    if (root_div_tags_children is None):
        LOGGER.error_with_time("Couldn't find article class. Aborting.")
        exit(1)

    root_div_tags_children = root_div_tags_children.find(
        "div", {"class": "content"})
    commentary = []

    for commentary_item in root_div_tags_children:
        over = commentary_item.find("div", {"class": "time-stamp"})
        description = commentary_item.find("div", {"class": "description"})

        if (over is None):
            over = ""
        else:
            over = over.text
            # over = over.text.replace("\"", "'")

        if (description is None):
            description = ""
        else:
            if properties.IS_TEST_MODE:
                description = ""
            else:
                description = description.text
            # description = description.text.replace("\"", "'")

        comment = Comment(over, description)
        paragraphs = commentary_item.findAll("p", {"class": "comment"})

        if (paragraphs is None):
            paragraphs = []

        if not properties.IS_TEST_MODE:
            for p in paragraphs:
                comment.add_paragraph(p.text)
                # comment.add_paragraph(p.text.replace("\"", "'"))

        if (len(over) != 0 or len(description) != 0 or len(comment.paragraphs) != 0):
            commentary.append(comment)

    commentary.reverse()
    ind = -1

    for i in range(len(commentary)):
        if (commentary[i].over == last_comment.over):
            ind = i

            break

    if (ind >= 0 and (commentary[ind].description != last_comment.description or commentary[ind].paragraphs != last_comment.paragraphs)):
        ind -= 1

    commentary = commentary[(ind + 1): len(commentary)]

    if (len(commentary) > 0):
        last_comment = commentary[-1]
    else:
        has_updates = False

    return commentary


def get_match_info_from_espn(last_timestamp):
    """Function to parse ESPN's Cricinfo website, and fetch match details using other functions.
    """
    FIRST_TEAM_TOP_LIST_ITEM_CLASS_NAME = "cscore_item cscore_item--home"
    SECOND_TEAM_TOP_LIST_ITEM_CLASS_NAME = "cscore_item cscore_item--away"

    try:
        request = urllib.request.Request(properties.MATCH_URL)
        response = urllib.request.urlopen(request)

        page_content = response.read().decode("utf-8")
        soup = BeautifulSoup(page_content, "html.parser")

        first_team_name, first_team_score = get_team_name_and_score(
            soup, FIRST_TEAM_TOP_LIST_ITEM_CLASS_NAME)
        second_team_name, second_team_score = get_team_name_and_score(
            soup, SECOND_TEAM_TOP_LIST_ITEM_CLASS_NAME)
        match = Match(first_team_name, second_team_name,
                      first_team_score, second_team_score)
        match.commentary = get_commentary(soup)

        return match
    except (ConnectionResetError, urllib.error.URLError) as e:
        LOGGER.exception_with_time(e)

        return None


def get_match_info():
    global has_updates

    match = get_match_info_from_espn(None)

    if (match == None):
        has_updates = False

        return ""

    info_string = "*{} - {}*".format(match.first_team, match.first_team_score)
    info_string += "\n*{} - {}*".format(match.second_team,
                                        match.second_team_score)

    for comment in match.commentary:
        info_string += "\n*{}* - {}".format(comment.over, comment.description)

        if (len(comment.paragraphs) > 0):
            for p in comment.paragraphs:
                info_string += "\n{}".format(p)

    return info_string


def scheduled_job(driver, names):
    global has_updates, match_start_time, match_end_time

    current_time = datetime.datetime.now()
    # print("entered scheduled_job")
    LOGGER.debug_with_time("Entered scheduled_job...")

    # the match hasn't started yet...
    if current_time < match_start_time or current_time > match_end_time:
        # return "The match hasn't started yet..."
        return

    MESSAGE_BOX_CLASS_NAME = "_1Plpp"
    SEND_BUTTON_CLASS_NAME = "_35EW6"
    has_updates = True
    message_content = get_match_info()

    if not has_updates:
        message_content = "No new updates right now..."

    for name in names:
        user = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[@title = \"{}\"]".format(name)))
        )
        LOGGER.debug_with_time("User found!")
        user.click()

        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, MESSAGE_BOX_CLASS_NAME))
        )
        LOGGER.debug_with_time("Message box found!")

        if len(message_content) == 0:
            continue
        
        message_box.send_keys(message_content)
        # message_box.text = message_content

        LOGGER.debug_with_time("Will wait to locate send_button...")
        send_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, SEND_BUTTON_CLASS_NAME))
        )
        LOGGER.debug("send_button found!")
        send_button.click()


def scheduler(driver, names):
    scheduled_job(driver, names)
    schedule.every(2).minutes.do(scheduled_job, driver, names)
    # schedule.every(10).seconds.do(scheduled_job, driver, names)

    while (True):
        schedule.run_pending()
        time.sleep(1)


def send_messages_on_whatsapp():
    global match_start_time, match_end_time, last_comment

    current_time = datetime.datetime.now()
    match_start_time = current_time.replace(
        hour=properties.MATCH_START_HOURS, minute=properties.MATCH_START_MINUTES, second=0, microsecond=0)
    match_end_time = current_time.replace(
        hour=properties.MATCH_END_HOURS, minute=properties.MATCH_END_MINUTES, second=0, microsecond=0)
    last_comment = Comment("None", "No comment yet...")
    URL = "https://web.whatsapp.com"

    driver = webdriver.Safari()
    driver.get(URL)

    user_input = input(
        "Enter the names of the groups/users you want to text, separated by commas(Eg. - Arya Stark, Sansa Stark, Jon Snow, Bran, Rickon, Robb) : ")
    names = [x.strip() for x in user_input.split(',')]
    scheduler(driver, names)


def init_logger():
    global LOGGER

    LOGGER = Logger(properties.LOG_FILENAME)


if __name__ == "__main__":
    init_logger()
    send_messages_on_whatsapp()
