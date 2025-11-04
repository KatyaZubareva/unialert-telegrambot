from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://my.itmo.ru/login")
    input("Войди вручную, потом нажми Enter...")

    page.wait_for_load_state("networkidle")
    time.sleep(3)

    page.goto("https://my.itmo.ru/schedule")

    page.wait_for_load_state("networkidle")
    time.sleep(3)

    html = page.content()

    soup = bs(html, "html.parser")

    lessons = page.locator("div.title").all_inner_texts()
    times = page.locator("span.mr-1").all_inner_texts()
    teachers = page.locator("a.text-muted").all_inner_texts()
    classrooms = page.locator("div.max-lines-1").all_inner_texts()
    campuses = page.locator("div.building.max-lines-1").all_inner_texts()

    print(lessons, times, teachers, classrooms, campuses)

    browser.close()
