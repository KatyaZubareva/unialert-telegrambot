from playwright.sync_api import sync_playwright
import pickle

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://my.itmo.ru/login")
    input("Войди вручную, потом нажми Enter...")
    
    cookies = page.context.cookies()
    with open("cookies.pkl", "wb") as f:
        pickle.dump(cookies, f)

    browser.close()