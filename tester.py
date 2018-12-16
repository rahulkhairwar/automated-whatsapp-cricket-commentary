from automator import get_match_info, has_updates, scheduled_job, datetime, properties, Comment, webdriver, last_comment

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
    
    current_time = datetime.datetime.now()
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