from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidElementStateException


def setup_selenium(link):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    c_Service = webdriver.ChromeService()
    driver = webdriver.Chrome(options=options, service=c_Service)

    driver.get(link)
    return driver


def switch_to_iframe(driver):
    # Find the iframe using its src attribute
    iframe = driver.find_element(By.TAG_NAME, "iframe")

    # Switch to the iframe
    driver.switch_to.frame(iframe)


def join_game(driver, time_to_load):
    wait = WebDriverWait(driver, time_to_load)
    element = wait.until(
        # EC.element_to_be_clickable((By.CSS_SELECTOR, ".styled.joinRound")) -- CHANGE THIS
    )
    element.click()


def get_equation(driver):
    element = driver.find_element(By.CSS_SELECTOR, "PLACEHOLDER")
    return element.text


def get_answer(driver, equation):
    return equation


def select_answer(driver, answer):
    # cycle through the answer elements and
    # see if one of them matches the given
    # answer parameter
    pass
