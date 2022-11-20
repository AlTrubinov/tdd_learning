from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import unittest


class NewVisitorTest(unittest.TestCase):
    '''Тест нового посетителя'''

    def setUp(self) -> None:
        '''Установка'''
        self.browser = webdriver.Firefox(
            executable_path="D:\\My Python APPs\\tdd_learning\\geckodriver\\0.32.0\\bin\\geckodriver.exe")

    def tearDown(self) -> None:
        '''Выход из браузера'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''Тест: можно начать список и получить его позже'''
        # Пользователь решает посетить домашнюю страницу онлайн-приложения неотложных дел
        self.browser.get('http://localhost:8000')

        # Пользователь видит заголовок и шапку страницы онлайн-приложения неотложных дел
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do', header_text)

        # Пользователю сразу же предлагается ввести элемент списка
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # Пользователь набирает в текстовом поле "Купить павлиньи перья" (его хобби –
        # вязание рыболовных мушек)
        inputbox.send_keys('Купить павлиньи перья')

        # Когда пользователь нажимает enter, страница обновляется, и теперь страница
        # содержит "1: Купить павлиньи перья" в качестве элемента списка
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Купить павлиньи перья', [row.text for row in rows])

        # Текстовое поле по-прежнему приглашает пользователя добавить еще один элемент.
        # Пользователь вводит "Сделать мушку из павлиньих перьев"
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Сделать мушку из павлиньих перьев')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Страница снова обновляется, и теперь показывает оба элемента списка
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn('1: Купить павлиньи перья', [row.text for row in rows])
        self.assertIn('2: Сделать мушку из павлиньих перьев', [row.text for row in rows])

        # Пользователю интересно, запомнит ли сайт список. Далее пользователь видит, что
        # сайт сгенерировал для него уникальный URL-адрес – об этом
        # выводится небольшой текст с объяснениями.
        self.fail('Закончить тест!')

        # Пользователь посещает этот URL-адрес – список по-прежнему там.

        # Пользователь выходит из браузера


if __name__ == '__main__':
    unittest.main(warnings='ignore')
