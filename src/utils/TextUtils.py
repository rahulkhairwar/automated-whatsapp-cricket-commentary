from selenium.webdriver.common.keys import Keys

def replaceQuotesInText(text):
    text = text.replace("\"", "`")
    # Not working in Chrome(and not required in Safari).
    text = text.replace("\n", Keys.SHIFT + Keys.ENTER)

    return text
        