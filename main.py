from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from colorama import  Back, Style,Fore
import keyboard
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import subprocess

options = Options()
# options.add_argument("--headless")
path_to_extension = "C:\\Users\\King\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\28mz8j6g.default-release\\extensions\\uBlock0@raymondhill.net.xpi"
options.add_argument('--load-extension' + path_to_extension)
try:

        li = [
            "Global", "Argentina", "Australia", "Austria", "Belgium", "Bolivia",
            "Brazil", "Canada", "Chile", "Colombia", "Costa Rica", "Czechia", "Denmark",
            "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Estonia", "Finland",
            "France", "Germany", "Guatemala", "Honduras", "Hungary", "Iceland", "India",
            "Indonesia", "Ireland", "Israel", "Italy", "Japan", "Kenya", "Luxembourg",
            "Mexico", "Netherlands", "New Zealand", "Nicaragua", "Nigeria", "Norway",
            "Panama", "Paraguay", "Peru", "Poland", "Portugal", "Romania", "Russia",
            "Saudi Arabia", "Serbia", "South Africa", "South Korea", "Spain", "Sweden",
            "Switzerland", "Tanzania", "Turkey", "Uganda", "Ukraine", "United Arab Emirates",
            "United Kingdom", "United States", "Uruguay", "Zimbabwe"
        ]

        print("================= Welcome to Terminal Music ==================")

        for i, country in enumerate(li[:62], 1):
            print(f"{i}) {country}")
        
        print("==============================================================\n")
        s = int(input("Enter your Choice : "))
        print("Please wait...\n")
        driver = webdriver.Firefox(options=options)
        driver.install_addon(path_to_extension, temporary=True)
        driver.get("https://music.youtube.com/charts")
        time.sleep(1)
        driver.find_element(By.XPATH,"//button[@class='style-scope ytmusic-sort-filter-button-renderer']").click()
        search = driver.find_element(By.XPATH,f"(//ytmusic-multi-select-menu-item-renderer[@class='style-scope ytmusic-multi-select-menu-renderer'])[position() = {s+1}]")
        time.sleep(2)
        search.click()
        time.sleep(1)
        # text = driver.find_elements(By.XPATH,"//yt-formatted-string[@class='text style-scope ytmusic-multi-select-menu-item-renderer']")
        # for i in text:
        #     print(i.text)
        driver.find_element(By.XPATH,"(//div[@class='yt-spec-touch-feedback-shape__fill'])[position()=2]").click()
        time.sleep(2)
        title = driver.find_element(By.XPATH,"//yt-formatted-string[@class='title style-scope ytmusic-responsive-header-renderer']")
        print("=================================================================================\n")
        print(title.text)
        print("\n")
        songs = driver.find_elements(By.XPATH,"//yt-formatted-string[@class='title style-scope ytmusic-responsive-list-item-renderer complex-string']")
        for index , song in enumerate(songs):
            print(f"{index+1}) {song.get_attribute('title')}")
        print("==================================================================================")
        m = int(input("Which Song do you want to play? "))
        choose_song = driver.find_element(By.XPATH,f"(//yt-formatted-string[@class='title style-scope ytmusic-responsive-list-item-renderer complex-string'])[position() = {m}]")
        choose_song.click()
        try :
             time.sleep(2)
             driver.find_element(By.XPATH,"//ytmusic-play-button-renderer[@class='style-scope ytmusic-responsive-header-renderer']/div").click()
        except:
             pass
        time.sleep(2)
        print("\n")
        print("==================================================================================\n")
        song_name = driver.find_element(By.XPATH,"//yt-formatted-string[@class='title style-scope ytmusic-player-bar']").text
        print(Fore.YELLOW+f"{song_name} is Playing...")
        try:
            artist = driver.find_element(By.XPATH,"//yt-formatted-string[@class='byline style-scope ytmusic-player-bar complex-string']/a").text
            print(Fore.LIGHTCYAN_EX+f"Artist : {artist}\n")
        except Exception as e:
             pass
        
        print(Fore.WHITE+"==================================================================================\n")
        time.sleep(5)   
        # try:
        #     # Check for modern skip button (priority)
        #     skip_button = driver.find_element(By.XPATH, "//button[@class='ytp-ad-skip-button-modern ytp-button']")
        #     skip_button.click()
        #     print("Ad skipped!")
        #     time.sleep(1)
        # except NoSuchElementException:
        #     pass

        # # Check for preview container with possible skip button later
        # try:
        #     if driver.find_element(By.XPATH, "//span[@class='ytp-ad-preview-container ytp-ad-preview-container-detached']"):
        #         print("Ad detected. Waiting for skip button...")
        #         time.sleep(7)

        #         try:
        #             skip_button = driver.find_element(By.XPATH, "//button[@class='ytp-ad-skip-button-modern ytp-button']")
        #             skip_button.click()
        #             print("Ad skipped!")
        #         except NoSuchElementException:
        #             print("Skip button not found. Ad may be unskippable or playing.")

        # except NoSuchElementException:
        #     pass
        
        print(Fore.LIGHTGREEN_EX+"Press ESC to close...")
        while True:
            if keyboard.is_pressed("esc"): 
                driver.close()
                print("Thank You for Using")
                break

except Exception as e:
        print(e)