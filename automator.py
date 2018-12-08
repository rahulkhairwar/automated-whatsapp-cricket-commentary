import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver

def get_latest_commentary(last_timestamp):
    MINI_SCORE_CLASS_NAME = "cb-min-bat-rw"
    MINI_SCORE_SPAN_CLASS_NAME = "cb-font-20 text-bold"
    CRICBUZZ_URL = "https://www.cricbuzz.com/live-cricket-scores/20301/aus-vs-ind-1st-test-india-tour-of-australia-2018-19"

    request = urllib.request.Request(CRICBUZZ_URL)
    response = urllib.request.urlopen(request)

    page_content = response.read().decode("utf-8")
    soup = BeautifulSoup(page_content, "html.parser")
    # data = soup.find("div", {"class":"{}".format(MINI_SCORE_CLASS_NAME)})

    for data in soup.findAll("div", {"class":"{}".format(MINI_SCORE_CLASS_NAME)}):
        for item in data.findAll("span", {"class":"{}".format(MINI_SCORE_SPAN_CLASS_NAME)}):
            mini_score = item.text

    return mini_score
    # print(mini_score_div)

def send_messages():
    # CODEFORCES_URL = "http://www.codeforces.com"
    WHATSAPP_URL = "https://web.whatsapp.com"
    MESSAGE_BOX_CLASS_NAME = "_1Plpp"
    SEND_BUTTON_CLASS_NAME = "_35EW6"

    driver = webdriver.Safari()
    driver.get(WHATSAPP_URL)

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
    latest_commentary = get_latest_commentary(None)
    print(latest_commentary)
