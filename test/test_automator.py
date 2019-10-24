# from "../src/automator" import get_match_info, has_updates, scheduled_job, datetime, properties, Comment, webdriver, last_comment
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../src/')
sys.path.insert(2, '../utils/')
sys.path.insert(3, '../models/')

from automator import get_match_info, has_updates, scheduled_job, properties, Comment, webdriver, last_comment
from models.Match import Match
from models.Comment import Comment
from utils import TimeUtils

match_start_time = ""

def test_scheduled_job():
    message_content = get_match_info()

    if not has_updates:
        message_content = "No new updates right now..."

    print(message_content)

def test_scheduler():
    # scheduled_job(None, None)
    test_scheduled_job()

def test_send_messages_on_whatsapp():
    global match_start_time
    global last_comment
    
    current_time = TimeUtils.get_current_time()
    match_start_time = current_time.replace(hour = properties.MATCH_START_HOURS, minute = properties.MATCH_START_MINUTES, second = 0, microsecond = 0)
    last_comment = Comment("None", "No comment yet...")
    # URL = "https://web.whatsapp.com"

    # driver = webdriver.Safari()
    # driver.get(URL)

    # user_input = input("Enter the names of the groups/users you want to text, separated by commas(Eg. - Arya Stark, Sansa Stark, Jon Snow, Bran, Rickon, Robb) : ")
    # names = [x.strip() for x in user_input.split(',')]

    test_scheduled_job()
    # test_scheduler()

if __name__ == "__main__":
    test_send_messages_on_whatsapp()
    