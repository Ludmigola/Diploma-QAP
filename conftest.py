"""

"""

import pytest
import uuid

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# добавм имя и пароль для входа
from settings import target_url


@pytest.fixture
def chrome_options(chrome_options):
    # chrome_options.binary_location = '../web-drivers/chromedriver_win32/chromedriver.exe'
    chrome_options.add_argument('--kiosk')
    return chrome_options


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def driver():
    driver = webdriver.Chrome(executable_path="../web-drivers/chromedriver_win32/chromedriver.exe")
    return driver


@pytest.fixture
def web_browser(request, driver):
    browser = driver
    browser.set_window_size(1400, 1000)

    browser.get(target_url)

    auth_form = WebDriverWait(browser, timeout=15).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')))


    # Return browser instance to test case:
    yield browser
    browser.close()

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screenshot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screenshot for local debug:
            browser.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass  # just ignore any errors here