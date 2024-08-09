from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import string

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.nytimes.com/games/wordle/index.html")


play_button = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".Welcome-module_button__ZG0Zh[data-testid='Play']"))
)
play_button.click()


WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, "Modal-module_closeIcon__TcEKb"))
)
x_button = driver.find_element(By.CLASS_NAME, "Modal-module_closeIcon__TcEKb")
x_button.click()


WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//button[@aria-label='add q']"))
)

enter_button = driver.find_element(By.XPATH, "//button[@aria-label='enter']")

buttons = {}
for letter in range(ord('a'), ord('z')+1):
    char = chr(letter)
    xpath = f"//button[@aria-label='add {char}']"
    button = driver.find_element(By.XPATH, xpath)
    buttons[char] = button

words = []
with open("valid_solutions.csv", "r") as file:
    lines = file.readlines()
    for line in lines:
        words.append(line.strip())

def getNextWord(green, yellow, grey):
    for word in words:
        validWord = True
        #check for grey letters
        for letter in grey:
            if letter in word:
                validWord = False
        #check that word contains yellow letters
        for letter in yellow:
            if letter not in word:
                validWord = False
        #check that yellow letters aren't in wrong spots
        for letter in yellowPositions:
            for position in yellowPositions[letter]:
                if word[position-1] == letter:
                    validWord = False
        #check that green letters are in correct spots
        for letter in green:
            if word[green[letter]-1] != letter:
                validWord = False
        if validWord:
            return word


def makeGuess(word):
    for letter in word:
        key = buttons[letter]
        time.sleep(.5)
        key.click()
    enter_button.click()

def analyzeGuess(rowNum):
    time.sleep(1.5)
    yellowLetters.clear()
    for i in range(1, 6):
        letter_element = driver.find_element(By.XPATH, f'//*[@id="wordle-app-game"]/div[1]/div/div[{rowNum}]/div[{i}]/div')
        attribute = letter_element.get_attribute("data-state")
        if attribute == 'correct':
            greenLetters[letter_element.get_attribute("aria-label")[12].lower()] = i
    for i in range(1, 6):
        letter_element = driver.find_element(By.XPATH, f'//*[@id="wordle-app-game"]/div[1]/div/div[{rowNum}]/div[{i}]/div')
        attribute = letter_element.get_attribute("data-state")
        if attribute == 'present':
            yellowPositions[letter_element.get_attribute("aria-label")[12].lower()].append(i)
            yellowLetters.append(letter_element.get_attribute("aria-label")[12].lower())
    for i in range(1, 6):
        letter_element = driver.find_element(By.XPATH, f'//*[@id="wordle-app-game"]/div[1]/div/div[{rowNum}]/div[{i}]/div')
        attribute = letter_element.get_attribute("data-state")
        if attribute == 'absent':
            if letter_element.get_attribute("aria-label")[12].lower() not in greenLetters and letter_element.get_attribute("aria-label")[12].lower() not in yellowLetters:
                greyLetters.append(letter_element.get_attribute("aria-label")[12].lower())                
                


def guessIsCorrect():
    if len(greenLetters) == 5:
        return True
    return False


notDone = True
currentRow = 1
nextWord = 'adieu'
greyLetters = []
yellowLetters = []
yellowPositions = {letter: [] for letter in string.ascii_lowercase}

greenLetters = {}
while notDone:
    if guessIsCorrect() or currentRow == 7:
        notDone = False
    else:
        makeGuess(nextWord)
        analyzeGuess(currentRow)
        print(greyLetters)
        currentRow += 1
        nextWord = getNextWord(greenLetters, yellowLetters, greyLetters)
        
time.sleep(3)
        
driver.quit()