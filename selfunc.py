import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import pickle
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def is_cookie_active():
    try:
        # Load the cookies from the file
        with open("cookies.pkl", "rb") as cookie_file:
            cookies = pickle.load(cookie_file)

        # Create a session and set the cookies
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # Send a GET request to the profile page to check if the cookie is still valid
        url = "https://www.storyblocks.com/member/profile"
        response = session.get(url, allow_redirects=False)

        # Check if the response is a 302 redirect to the login page
        if response.status_code == 302 and "https://www.storyblocks.com/login" == response.headers.get("location", "").lower():
            print("Cookie is not valid.")
            return False
        print("Cookie is still active!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False
def logging_in():
    print('Login script started\n')
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium"
    options.add_experimental_option("prefs", {
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    options.add_argument("--headless")  # No GUI
    options.add_argument("--no-sandbox")  # Required in some hostings
    options.add_argument("--disable-dev-shm-usage")  # Helps with limited RAM
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)

    try:
        driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)
        driver.get('https://www.storyblocks.com/login')

        # Wait for the login fields to be present
        wait = WebDriverWait(driver, 15)
        username_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        checkbox = wait.until(EC.element_to_be_clickable((By.ID, "agreement-checkbox")))

        email = os.getenv("WEB_EMAIL")
        password = os.getenv("WEB_PASSWORD")

        # Fill in the login form
        username_field.send_keys(email)
        password_field.send_keys(password)
        checkbox.click()
        password_field.send_keys(Keys.RETURN)

        # Wait for the post-login page to load completely (use a wait condition that confirms login)
        # For example, check for a dashboard element or a page title that indicates login success
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".some-element-on-dashboard")))

        # Now, wait a bit longer to ensure cookies are set after the final redirect
        time.sleep(5)  # Optional, just to ensure that the cookies are set
        cookies = driver.get_cookies()
        print(f"Cookies after login: {cookies}")

        # Check if the 'login_session' cookie is present
        login_session_cookie = next((cookie for cookie in cookies if cookie['name'] == 'login_session'), None)

        if login_session_cookie:
            # Save cookies to JSON file if login_session is found
            with open("cookies.pkl", "w") as cookie_file:
                pickle.dump(cookies, cookie_file)
            print("Login successful, cookies saved in JSON format.")
        else:
            print("login_session cookie not found.")

    except Exception as e:
        print(f"Login failed: {e}")
    finally:
        driver.quit()
        print('Login script finished\n')

def getCookie():
    print("Getting cookie...")

    def load_cookies_from_file():
        with open("cookies.pkl", "rb") as cookie_file:
            return pickle.load(cookie_file)

    try:
        try:
            # Attempt to load cookies
            cookies = load_cookies_from_file()
            print("Cookies loaded from file.")
        except Exception as e:
            print(f"Error loading cookies: {e}")
            print("Attempting to login and regenerate cookies...")
            logging_in()
            cookies = load_cookies_from_file()

        # Check if cookie is active
        if not is_cookie_active():
            print("Cookie is not active. Logging in again...")
            logging_in()
            cookies = load_cookies_from_file()

        # Extract the login_session cookie
        login_session_value = next(
            (cookie['value'] for cookie in cookies if cookie['name'] == 'login_session'),
            None
        )

        if not login_session_value:
            print("Login session cookie not found! login attempt")
            logging_in()
            cookies = load_cookies_from_file()
            login_session_value = next(
                (cookie['value'] for cookie in cookies if cookie['name'] == 'login_session'),
                None
            )
            if not login_session_value:
                print("Login session cookie still not found after login attempt!")
                return None
            return None

        print("Cookie retrieved successfully!")
        return login_session_value

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def getID(login_session, url):
    print(f"Getting ID for URL: {url}")
    try:
        if not login_session:
            return {'pageFound': False, 'id': 0}
        
        # Create a session and set the cookies
        headers = {
            "cookie": f"login_session={login_session}",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        # Check if the page was fetched successfully
        if response.status_code != 200:
            return {'pageFound': False, 'id': 0}
    
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the script tag containing the JSON-LD data
        script_tag = soup.find('script', {'type': 'application/ld+json'})
        
        if script_tag:
            try:
                # Extract the JSON content and parse it
                json_content = json.loads(script_tag.string)
                # Get the identifier
                id = json_content[0]["identifier"]
                print(f"ID found: {id}")
                return {'pageFound': True, 'id': id}
            except (json.JSONDecodeError, KeyError, IndexError):
                # Handle JSON decoding or missing expected fields
                return {'pageFound': False, 'id': 0}
        else:
            # If the script tag is not found
            return {'pageFound': False, 'id': 0}
    except:
        return {'pageFound': False, 'id': 0}
