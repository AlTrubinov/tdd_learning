from selenium import webdriver

browser = webdriver.Firefox(executable_path="D:\\My Python APPs\\tdd_learning\\geckodriver\\0.32.0\\bin\\geckodriver.exe")
browser.get('http://localhost:8000')

assert 'Congratulations' in browser.title