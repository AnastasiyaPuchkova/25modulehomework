import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('./PycharmProjects/SkillfactoryProject/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()

def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('vasya@mail.com')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

def test_page_user():
    pytest.driver.implicitly_wait(10)
    images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = pytest.driver.find_elements_by_css_selector('.card-deck .card-title')
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''  #проверяем, что путь, указанный в атрибуте src, не пустой.
        assert names[i].text != '' #имя, имеет не пустой текст
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

def test_my_user_pets():
    pytest.driver.find_element_by_css_selector('a.nav-link[href="/my_pets"]').click() #Открываем страницу Мои питомцы

    photos = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'th[scope="row"]'))
    )
    count = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/text()[1]'))
    )
    pets = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr'))
    )
    Names = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]'))
    )
    breeds = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]'))
    )
    ages = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]'))
    )
    for i in range(len(pets)):
        assert photos[i].get_attribute('src') != '' #проверяем, что есть фото
        assert count.text != ''
        assert ': ' in count
        part = count.text.split(": ")
        assert part[0] != ''
        assert part[1] == len(pets) #Проверяем, что присутствуют все питомцы
        assert len(Names) == len(pets) #Проверяем, что у всех питомцев есть имя
        assert len(breeds) == len(pets)  # Проверяем, что у всех питомцев есть порода
        assert len(ages) == len(pets)  # Проверяем, что у всех питомцев есть возраст


