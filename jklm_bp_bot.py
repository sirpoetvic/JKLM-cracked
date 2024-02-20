"""Module generates and runs a "bot" that responds to JKLM's Bomb Party.
-- Enter a username and a room code ID into the CLI to start
-- Escape key resets word bank
-- Ctrl+C to reset game (in CLI)
"""

import time
import sys
import keyboard
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidElementStateException

used_words = dict()
rare_letters = ["q", "k", "j", "x", "w", "z"]


def setup_selenium(link: str):
    """Sets up Selenium driver

    Args:
        link (string): Link of the website accessed

    Returns:
        WebDriver: Driver of the accessed website
    """

    # Changing options to keep window open after program runs through
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    c_Service = webdriver.ChromeService()

    # Setting custom options and service to Chrome
    driver = webdriver.Chrome(options=options, service=c_Service)

    # Get the driver using the link
    driver.get(link)
    return driver


def set_username(
    driver: webdriver, username: str, time_to_load: int = 30
) -> None:
    """Sets the username of the user

    Args:
        driver (WebDriver): Driver of the accessed websites
        username (string): custom username
        time_to_load (int, optional): Max time before timeout in seconds
    """
    wait = WebDriverWait(driver, time_to_load)
    elem = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".nickname"))
    )
    elem.clear()
    elem.send_keys(username)
    elem.send_keys(Keys.RETURN)


def switch_to_iframe(driver: webdriver, time_to_load: int = 30) -> None:
    """Switches to the IFrame of a given driver

    Args:
        driver (WebDriver): Driver of the accessed websites
        time_to_load (int): Max time before timeout in seconds
    """

    # Find the iframe using its tag name
    wait = WebDriverWait(driver, time_to_load)
    iframe = wait.until(EC.element_to_be_clickable((By.TAG_NAME, "iframe")))

    # Switch to the iframe
    driver.switch_to.frame(iframe)


def join_game(driver: webdriver, time_to_load: int = 30) -> None:
    """Joins the game

    Args:
        driver (WebDriver): Driver of the accessed websites
        time_to_load (int): Max time before timeout in seconds
    """
    wait = WebDriverWait(driver, time_to_load)
    element = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".styled.joinRound"))
    )
    element.click()


def scan_for_syllable(driver: webdriver) -> str:
    """Scans for the syllable element, returns a syllable string

    Args:
        driver (WebDriver): Driver of the accessed websites

    Returns:
        str: current syllable
    """
    element = driver.find_element(By.CSS_SELECTOR, ".syllable")
    return element.text.upper()


def get_player_turn(driver: webdriver) -> str:
    """Returns the name of the current player

    Args:
        driver (WebDriver): Driver of the accessed websites

    Returns:
        str: name of the player whose turn it is
    """
    element = driver.find_element(By.CSS_SELECTOR, ".player")
    return element.text


def get_word(syllable: str, words: list) -> str:
    """Searches word given a syllable and a list of words

    Args:
        syllable (str): syllable
        words (list): list of words

    Returns:
        str: word containing the syllable
    """
    longest = ""
    for word in words:
        if (
            syllable in word
            and len(word) > len(longest)
            and word not in used_words
        ):
            longest = word
            used_words[word] = 1

    return longest


def get_word_with_rare(syllable: str, words: list, num: int) -> str:
    """Searches word given a syllable and an int that refers to a list of
    letters rarely used in words and a list of words

    Args:
        syllable (str): syllable
        words (list): list of words
        num (int): number that refers to an index in a list of rare letters

    Returns:
        str: word containing the syllable and the rare letter
    """
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


def input_word(driver: webdriver, word: str) -> None:
    """Inputs given word into input box

    Args:
        driver (WebDriver): Driver of the accessed websites
        word (str): word to be input into input box
    """
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


PROGRAM_IS_ACTIVE, GAME_IS_ACTIVE, is_your_turn = True, False, False
username = input("Enter a username: ")
with open("dict.txt") as f:
    word_dict = [line[:-1] for line in f]
program_driver = setup_selenium(
    f"https://jklm.fun/{(input('room code id: '))}"
)
set_username(program_driver, username)
switch_to_iframe(program_driver)  # jklm uses an iframe to host its gameplay
join_game(program_driver, 30)  # join the game


GAME_IS_ACTIVE = True

RARE = 0
RARITY = 0

while PROGRAM_IS_ACTIVE:
    while GAME_IS_ACTIVE:
        if keyboard.is_pressed("esc"):
            word_dict.clear()
            print("All words have been cleared from the current dictionary.")
        is_your_turn = get_player_turn(program_driver) == ""
        while is_your_turn:
            if RARITY % 37 == 0:
                word_input = get_word_with_rare(
                    scan_for_syllable(program_driver), word_dict, RARE
                )
                RARE += 1
                RARE %= len(rare_letters)
            else:
                word_input = get_word(
                    scan_for_syllable(program_driver), word_dict
                )
            input_word(program_driver, word_input)
            time.sleep(0.05)
            is_your_turn = False
            RARITY = RARITY + 1
program_driver.quit()
sys.exit()
