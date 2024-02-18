import time
import keyboard
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidElementStateException

used_words = dict()
rare_letters = ["q", "k", "j", "x", "w", "z"]


def setup_selenium(link):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    c_Service = webdriver.ChromeService()
    driver = webdriver.Chrome(options=options, service=c_Service)

    driver.get(link)
    return driver


def set_username(driver, username):
    wait = WebDriverWait(driver, 30)
    elem = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nickname")))
    elem.clear()
    elem.send_keys(username)
    elem.send_keys(Keys.RETURN)


def switch_to_iframe(driver):
    # Find the iframe using its src attribute
    wait = WebDriverWait(driver, 30)
    iframe = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "iframe")))
    # Switch to the iframe
    driver.switch_to.frame(iframe)


def join_game(driver, time_to_load):
    wait = WebDriverWait(driver, time_to_load)
    element = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".styled.joinRound"))
    )
    element.click()


def scan_for_syllable(driver):
    element = driver.find_element(By.CSS_SELECTOR, ".syllable")
    return element.text.upper()


def get_player_turn(driver):
    element = driver.find_element(By.CSS_SELECTOR, ".player")
    return element.text


def get_word(syllable, words):
    longest = ""
    for word in words:
        if (
            syllable in word
            and len(word) > len(longest)
            and word not in used_words.keys()
        ):
            longest = word
            used_words[word] = 1

    return longest


def get_word_with_rare(syllable, words, num):
    longest = ""
    for word in words:
        if (
            syllable in word
            and len(word) > len(longest)
            and word not in used_words.keys()
            and rare_letters[num]
        ):
            longest = word
            used_words[word] = 1

    return longest


def input_word(driver, word):
    try:
        elem = driver.find_element(
            By.XPATH, "/html/body/div[2]/div[3]/div[2]/div[2]/form/input"
        )
        elem.clear()
        elem.send_keys(word)
        elem.send_keys(Keys.RETURN)
    except ElementNotInteractableException:
        pass
    except InvalidElementStateException:
        pass


GAME_IS_ACTIVE, is_your_turn = False, False
username = input("Enter a username: ")
with open("dict.txt") as f:
    word_list = [line[:-1] for line in f]
driver = setup_selenium(f"https://jklm.fun/{(input('room code id: '))}")
set_username(driver, username)
switch_to_iframe(driver)  # jklm uses an iframe to host its gameplay
join_game(driver, 30)  # join the game


GAME_IS_ACTIVE = True

RARE = 0
RARITY = 0

while GAME_IS_ACTIVE:
    if keyboard.read_key("\\x1b"):
        driver.quit()
        sys.exit()
    is_your_turn = get_player_turn(driver) == ""
    while is_your_turn:
        if RARITY % 37 == 0:
            word = get_word_with_rare(scan_for_syllable(driver), word_list, RARE)
            RARE += 1
            RARE %= len(rare_letters)
        else:
            word = get_word(scan_for_syllable(driver), word_list)
        input_word(driver, word)
        time.sleep(0.05)
        is_your_turn = False
        RARITY = RARITY + 1
