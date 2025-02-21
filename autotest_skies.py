import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

link = "https://yesihelp-stage.skies.land/"

@pytest.fixture(scope="function")
def browser():
    print("\nstart browser for test..")
    browser = webdriver.Chrome()
    browser.maximize_window()
    yield browser
    print("\nquit browser..")
    browser.quit()

class TestMainPage:

    def test_cl_1(self, browser):
        # auth
        browser.get(link)
        browser.find_element(By.XPATH, "//*[@id=\"skies-app\"]/div/top-menu/div/div/nav/ul/li[4]/a").click()
        browser.find_element(By.ID, "mat-input-0").send_keys("тестовый логин")
        browser.find_element(By.ID, "mat-input-1").send_keys("тестовый пароль")
        browser.find_element(By.CSS_SELECTOR,"input.login-window__submit-button").click()
        # test_see_3_counters
        time.sleep(1)
        browser.execute_script("arguments[0].scrollIntoView(true);", browser.find_element(By.CSS_SELECTOR, 'div.counters'))
        time.sleep(3)
        browser.find_element(By.CSS_SELECTOR, "div.counters__items:nth-child(1)")
        browser.find_element(By.CSS_SELECTOR, "div.counters__items:nth-child(2)")
        browser.find_element(By.CSS_SELECTOR, "div.counters__items:nth-child(3)")

        #test_see_6_projects
        browser.execute_script("arguments[0].scrollIntoView(true);", browser.find_element(By.CSS_SELECTOR,'h2.creator-badge-list__header'))
        time.sleep(3)
        browser.find_element(By.CSS_SELECTOR,"creator-badge:nth-child(1) > div")
        browser.find_element(By.CSS_SELECTOR,"creator-badge:nth-child(2) > div")
        browser.find_element(By.CSS_SELECTOR,"creator-badge:nth-child(3) > div")
        browser.find_element(By.CSS_SELECTOR,"creator-badge:nth-child(4) > div")
        browser.find_element(By.CSS_SELECTOR,"creator-badge:nth-child(5) > div")
        browser.find_element(By.CSS_SELECTOR,"creator-badge:nth-child(6) > div")
        print("Тест 1 закончен")

class TestProject:

    def test_cl_2(self, browser):
        # auth
        browser.get(link)
        browser.find_element(By.XPATH, "//*[@id=\"skies-app\"]/div/top-menu/div/div/nav/ul/li[4]/a").click()
        browser.find_element(By.ID, "mat-input-0").send_keys("test-login@mail.com")
        browser.find_element(By.ID, "mat-input-1").send_keys("WYFo66SVbh!uw#D")
        browser.find_element(By.CSS_SELECTOR,"input.login-window__submit-button").click()
        time.sleep(3)
        browser.find_element(By.CSS_SELECTOR, "top-menu li:nth-child(2)").click()
        browser.find_element(By.ID, "mat-input-0").send_keys("привет") # ищем проекты по слову "привет"
        browser.find_element(By.ID, "mat-input-0").send_keys(Keys.RETURN)
        time.sleep(3)
        amount_of_projects_found=browser.find_element(By.CSS_SELECTOR, "search li:nth-child(1) a")
        assert "(1)" in amount_of_projects_found.text, "найденных проектов не 1" # найденных проектов 1?
        amount_of_posts_found=browser.find_element(By.CSS_SELECTOR, "search li:nth-child(2) a")
        assert "(1)" in amount_of_posts_found.text, "найденных постов не 1" # найденных постов 1?
        # зайти в "Света Штрейс", проверить наличие "Об авторе", "Блог проекта", блока "Способы поддержки", кнопки "Ю-Мани"
        browser.find_element(By.CSS_SELECTOR, "div.creator-badge__avatar > a").click()
        time.sleep(3)
        browser.find_element(By.CSS_SELECTOR,"div.about__tab-item.active")
        browser.find_element(By.CSS_SELECTOR, "div.about__tab-group > div:nth-child(2)")
        browser.find_element(By.CSS_SELECTOR, "app-external-wallet > div")
        browser.find_element(By.CSS_SELECTOR,"app-external-wallet > div > a > div")
        # перейти в раздел "Блог"
        browser.find_element(By.CSS_SELECTOR,"div.about__tab-group > div:nth-child(2)").click()
        time.sleep(2)
        # ищем тело для комментариев последнего поста (первый на стене)
        browser.execute_script("arguments[0].scrollIntoView(true);", browser.find_element(By.CSS_SELECTOR,"textarea.editor__textarea"))
        time.sleep(2)
        comment_text="комментарий автотестостеровщика_11"
        browser.find_element(By.CSS_SELECTOR, "textarea.editor__textarea").send_keys(comment_text)
        time.sleep(2)
        browser.find_element(By.CLASS_NAME,"mdc-button__label").click() # клик по первой кнопке "Комментировать"
        time.sleep(3)
        # проверить отображение комментария
        try:
            browser.execute_script("arguments[0].scrollIntoView(true);",browser.find_element(By.CSS_SELECTOR, "post.ng-star-inserted:first-of-type comment.ng-star-inserted:last-child p"))
            last_comment = browser.find_element(By.CSS_SELECTOR, "post.ng-star-inserted:first-of-type comment.ng-star-inserted:last-child p").text
            time.sleep(3)
            if last_comment==comment_text:
                print("последний оставленный комментарий отображается")
            else:
                print("не нашли")
        finally:
            # нажать "Поддержать"
            browser.execute_script('window.scrollTo(0,0);')
            time.sleep(2)
            browser.find_element(By.CSS_SELECTOR,"div.umoney-button").click()
            # проверить переход на страницу поддержки (https://yoomoney.ru/to/4100118713279755)
            browser.switch_to.window(browser.window_handles[1])
            time.sleep(3)
            new_web = browser.current_url
            assert new_web=="https://yoomoney.ru/to/4100118713279755" and requests.head(new_web).status_code==200
            print("Тест 2 закончен")

    def test_cl_3(self, browser):
        # auth at svetlana page
        browser.get('https://yesihelp-stage.skies.land/svetlana')
        browser.find_element(By.XPATH, "//*[@id=\"skies-app\"]/div/top-menu/div/div/nav/ul/li[4]/a").click()
        browser.find_element(By.ID, "mat-input-0").send_keys("test-login@mail.com")
        browser.find_element(By.ID, "mat-input-1").send_keys("WYFo66SVbh!uw#D")
        browser.find_element(By.CSS_SELECTOR, "input.login-window__submit-button").click()

        # зафиксировать "стиль" (img>src) кнопки "Отслеживать" до нажатия
        WebDriverWait(browser,5,1).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"img.poster__button-icon")))
        style_before = browser.find_element(By.CSS_SELECTOR, "img.poster__button-icon").get_attribute("src")
        # нажать "Отслеживать" (звёздочка)
        browser.find_element(By.CSS_SELECTOR, "img.poster__button-icon").click()
        time.sleep(3)
        style_after=browser.find_element(By.CSS_SELECTOR, "img.poster__button-icon").get_attribute("src")
        # должна изменить стиль
        assert style_before!=style_after, "ошибка в сравнении стилей"
        # перейти в "Избранное" на этой же странице и проверить, что проект там появился
        browser.find_element(By.CSS_SELECTOR,"creator-menu > nav > ul > li:nth-child(4) > a").click()
        WebDriverWait(browser,5,1).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.creators__item:last-child span")))
        search_text = "Света Штрейс"
        assert search_text==browser.find_element(By.CSS_SELECTOR,"div.creators__item:last-child span").text, "не нашёл блог в избранном"
        # удалить его из закладок (нажать "Звёздочку"), обновить страницу, проверить, что проекта больше нет в списке
        browser.find_element(By.CSS_SELECTOR,"div.creators__content > div > div > button").click()
        browser.refresh()
        try:
            block=WebDriverWait(browser,5,1).until(ec.presence_of_element_located((By.CSS_SELECTOR,"div.creators__item:last-child span")))
            if block:
                assert search_text!=browser.find_element(By.CSS_SELECTOR,"div.creators__item:last-child span").text,"ошибка удаления блока"
        except:
            print("Тест 3 закончен")

"""Запуск тестов и получение отчёта в терминале PyCharm в виртуальном окружении, где находится исполняемый файл:
pytest -s -v autotest_skies.py,
или из cmd ОС (питон должен быть уже установлен на компе):
(установить модули командами)
python -m pip install pytest
python -m pip install selenium
python -m pip install requests
"""
