from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    '''Тест нового посетителя'''

    def setUp(self) -> None:
        '''Установка'''
        self.browser = webdriver.Firefox(
            executable_path="/geckodriver/0.32.0/bin/geckodriver.exe")

    def tearDown(self) -> None:
        '''Выход из браузера'''
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        '''Ожидание строки в таблице списка'''
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.3)

    def test_can_start_a_list_for_one_user(self):
        '''Тест: можно начать список для одного пользователя'''
        # Пользователь решает посетить домашнюю страницу онлайн-приложения неотложных дел
        self.browser.get(self.live_server_url)

        # Пользователь видит заголовок и шапку страницы онлайн-приложения неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Пользователю сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Пользователь набирает в текстовом поле "Купить павлиньи перья" (его хобби –
        # вязание рыболовных мушек)
        inputbox.send_keys('Купить павлиньи перья')

        # Когда Пользователь нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Текстовое поле по-прежнему приглашает Пользователя добавить еще один элемент.
        # Пользователь вводит "Сделать мушку из павлиньих перьев"
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)

        # Страница снова обновляется, и теперь показывает оба элемента списка
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')
        self.wait_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

        # Пользователю интересно, запомнит ли сайт список. Далее Пользователь видит, что
        # сайт сгенерировал для него уникальный URL-адрес – об этом
        # выводится небольшой текст с объяснениями.

        # Пользователь посещает этот URL-адрес – список по-прежнему там.

        # Пользователь выходит из браузера

    def test_multiple_users_can_start_lists_at_different_urls(self):
        '''Тест: многочисленные пользователи могут начать списки по разным url'''
        # Пользователь начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Купить павлиньи перья')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить павлиньи перья')

        # Пользователь замечает, что новый список имеет уникальный URL-адрес
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')

        # Теперь новый Посетитель приходит на сайт.

        ## Мы используем новый сеанс браузера, тем самым обеспечивая, чтобы никакая
        ## информация от Эдит не прошла через данные cookie и пр.
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path="/geckodriver/0.32.0/bin/geckodriver.exe")

        # Посетитель заходит на домашнюю страницу. Нет никаких признаков списка Пользователя
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertNotIn('Сделать мушку из павлиньих перьев', page_text)

        # Посетитель начинает новый список, вводя новый элемент
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Купить молоко')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Купить молоко')

        # Посетитель получает уникальный URL-адрес
        visitor_list_url = self.browser.current_url
        self.assertRegex(visitor_list_url, '/lists/.+')
        self.assertNotEqual(visitor_list_url, user_list_url)

        # Следов списка Пользователя нет
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Купить павлиньи перья', page_text)
        self.assertIn('Купить молоко', page_text)

        #Пользователь и посетитель покинули приложение


