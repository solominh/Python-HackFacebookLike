from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def load_accounts(file_path):
    accounts = []
    with open(file_path) as f:
        for line in f:
            cleaned_line = line.strip()
            if not cleaned_line:
                continue
            space_pos = cleaned_line.index(' ')
            email = cleaned_line[:space_pos]
            password = cleaned_line[space_pos:].strip()
            if email and password:
                accounts.append(dict(email=email, password=password))
    return accounts


def login(account):
    # Chrome option
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    url = 'https://www.facebook.com/'
    driver.get(url)

    # Find elements
    email_input = driver.find_element_by_id('email')
    password_input = driver.find_element_by_id('pass')
    sign_in_button = driver.find_element_by_id('u_0_l')

    # Login
    email_input.send_keys(account['email'])
    password_input.send_keys(account['password'])
    sign_in_button.click()

    return driver


def like_a_post(driver, url):
    driver.get(url)
    try:
        like_button_xpath = '//*[@id="fbPhotoSnowliftFeedback"]/div/div[1]/div/div/div/div/span[1]/div/a'
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, like_button_xpath)))

        aria_pressed_attribute = element.get_attribute('aria-pressed')
        if aria_pressed_attribute == 'false':
            element.click()
            print('Like successfully!')
        else:
            print('This post is already liked!')
    except Exception as e:
        print('Like button not found')

link_to_like = 'https://www.facebook.com/photo.php?fbid=871123139735797&set=a.871123186402459.1073741826.100005143570218&type=3'


def main(url_to_like, accounts_filepath='./accounts.txt'):
    accounts = load_accounts(accounts_filepath)
    for account in accounts:
        driver = login(account)
        like_a_post(driver, url_to_like)
        time.sleep(3)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Please add url to like')
    else:
        url_to_like = sys.argv[1]
        if len(sys.argv) > 2:
            accounts_filepath = sys.argv[2]
        else:
            print('Use default accounts file path in ./accounts.txt')

        main(url_to_like, accounts_filepath='./accounts.txt')
