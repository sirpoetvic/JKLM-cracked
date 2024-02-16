import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import InvalidElementStateException

used_words = dict()


def setup_selenium(link):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    c_Service = webdriver.ChromeService()
    driver = webdriver.Chrome(options=options, service=c_Service)

    driver.get(link)
    return driver


def username(driver, username):
    elem = driver.find_element(By.CSS_SELECTOR, ".nickname")
    elem.clear()
    elem.send_keys(input("username: "))
    elem.send_keys(Keys.RETURN)


def switch_to_iframe(driver):
    # Find the iframe using its src attribute
    iframe = driver.find_element(
        By.XPATH, '//iframe[@src="https://falcon.jklm.fun/games/bombparty"]'
    )

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
            time.sleep(0.05)
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
        print("Element was not interactable at this time.")
        pass
    except InvalidElementStateException:
        print("Element was in an invalid state.")
        pass


def __main__():
    game_is_active, is_your_turn = False, False
    with open("dict.txt") as f:
        list = [line[:-1] for line in f]
    driver = setup_selenium("https://jklm.fun/WCXC")
    username(driver, "beep's rival")  # username is currently "beep"
    time.sleep(3)  # need to wait for things to load, can probably lower time
    switch_to_iframe(driver)  # jklm uses an iframe to host its gameplay
    join_game(driver, 2)  # join the game

    # insert manual override for slow game activation

    # in testing: print all of the syllables, using scan_for_syllable, just
    # to see if .syllable is the CSS element we are looking for
    game_is_active = True

    while game_is_active:
        is_your_turn = get_player_turn(driver) == ""
        while is_your_turn:
            word = get_word(scan_for_syllable(driver), list)
            input_word(driver, word)
            time.sleep(0.05)
            is_your_turn = get_player_turn(driver) == ""


__main__()


# Next steps!!
# -- COMPLETE --# 1. get the syllable
# -- COMPLETE --# 2. Check if it's your turn - maybe using .selfturn? By.CSS_Selector -- depends on what this outputs -- a name? a boolean?
# -- COMPLETE --# 3. Inputting words into the text box - figure out what element name it uses
# -- COMPLETE --# 4. Word list library (txt doc or something else) - research efficiency

# 5. Make code
# 6. Add usage of "q", "j", "z", "y", and "w" to increase lives
# 7. Add escape keys so that the program doesn't just crash immediately

# CHANGE THE IFRAME (THE SERVER WILL RESET OR SOMETHING EVERY ONCE IN A WHILE) -- LINE 34
# CHANGE THE LOBBY CODE -- LINE 91

# Tuning:
# Determine the time needed for the iframe to load after entering a username?
# Determine the time needed
