"""

"""

import pytest
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from settings import user_agreement_url, user_phone, user_mail, user_login, user_ls
from settings import vk_title, ok_title, mail_title, ya_title, rt_title
from settings import valid_phone, valid_mail, valid_login, valid_ls, valid_password, invalid_password

def get_login_form_auth_tabs(login_form):
    '''
    Возвращает все найденные элементы табов для типа авторизации в порядке:
    таб "Телефон", таб "Почта", таб "Логин", таб "Лицевой счёт"
    '''

    tab_phone = login_form.find_element(By.ID, 't-btn-tab-phone')
    tab_mail = login_form.find_element(By.ID, 't-btn-tab-mail')
    tab_login = login_form.find_element(By.ID, 't-btn-tab-login')
    tab_ls = login_form.find_element(By.ID, 't-btn-tab-ls')

    return [tab_phone, tab_mail, tab_login, tab_ls]


def clear_input_element(input_element):
    '''
    Функция просто очищает поля ввода логина и пароля.
    Специальный метод clear() не позволяет очистить формы, поэтому используется
    комбинация CTRL+a, Delete
    '''
    input_element.send_keys(Keys.CONTROL + "a")
    input_element.send_keys(Keys.DELETE)


def test_login_form_present(web_browser):
    '''
    Тест проверят загрузку и отображение формы авторизации.
    Наличие всех типов авторизации: "Телефон",  "Почта", "Логин", "Лицевой счёт".
    По умолчанию выбран тип "Телефон".
    Поля ввода логина и пароля, а также кнопка "Войти" доступны.
    '''
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')

    tab_phone = login_form.find_element(By.ID, 't-btn-tab-phone')
    assert tab_phone.is_displayed() is True

    tab_mail = login_form.find_element(By.ID, 't-btn-tab-mail')
    assert tab_mail.is_displayed() is True

    tab_login = login_form.find_element(By.ID, 't-btn-tab-login')
    assert tab_login.is_displayed() is True

    tab_ls = login_form.find_element(By.ID, 't-btn-tab-ls')
    assert tab_ls.is_displayed() is True

    # По умолчанию должен быть выбран тип "Телефон" (значение атрибута == 'PHONE')
    tab_type = login_form.find_element(By.NAME, 'tab_type')
    assert tab_type.get_attribute('value') == 'PHONE'

    # Формы ввода логина и пароля также видимы
    input_username = login_form.find_element(By.ID, 'username')
    assert input_username.is_displayed() is True

    input_password = login_form.find_element(By.ID, 'password')
    assert input_password.is_displayed() is True

    # Кнопка "Войти" доступна
    login_btn = login_form.find_element(By.XPATH, '//*[@id="kc-login"]')
    assert login_btn.text == u'Войти'


def auto_tab_selection(tab, login_form):
    '''
    Функция позволяет сделать тест автоматического выбора типа аутентификации
    по параметрам заданным в форме ввода. При этом перед каждым вводом параметров
    тип аутентификации устанавливается в начальное заданное значение переданное функции в аргументе tab
    '''
    # находим элемент хранящий значение текущего типа аутентификации
    tab_type = login_form.find_element(By.NAME, 'tab_type')

    # найдем формы ввода параметров пользователя и пароля
    input_username = login_form.find_element(By.ID, 'username')
    input_password = login_form.find_element(By.ID, 'password')

    # здесь мы определяем словарь с ключами в виде значений принимаемых элементом tab_type
    # и в качестве значений задаем соотвествующие параметры сохраненные в settings.py
    tabs = {'PHONE': user_phone,
            'EMAIL': user_mail,
            'LOGIN': user_login,
            'LS': user_ls}

    for key in tabs.keys():
        # каждый раз устанавливаем тип айтентификации переданный в параметре tab
        tab.click()

        # очистим форму ввода для параметров пользователя после предыдущего теста
        clear_input_element(input_username)
        # установим значение в форме, соотвествующее текущему типу аутентификации из словаря
        input_username.send_keys(tabs.get(key))
        # перейдем на форму ввода пароля, чтобы сработало автоопределение типа аутентификации
        input_password.click()
        # значение автоматически определенного типа должно соотвествовать значению key
        assert tab_type.get_attribute('value') == key


def test_auto_auth_selection_from_phone_tab(web_browser):
    '''
    Функция проверяет тест-кейс автоматического опредления аутентификации с таба "Телефон"
    '''
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    tab_phone, _, _, _ = get_login_form_auth_tabs(login_form)

    auto_tab_selection(tab_phone, login_form)


def test_auto_auth_selection_from_email_tab(web_browser):
    '''
    Функция проверяет тест-кейс автоматического опредления аутентификации с таба "Почта"
    '''
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    _, tab_email, _, _ = get_login_form_auth_tabs(login_form)

    auto_tab_selection(tab_email, login_form)


def test_auto_auth_selection_from_login_tab(web_browser):
    '''
    Функция проверяет тест-кейс автоматического опредления аутентификации с таба "Логин"
    '''
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    _, _, tab_login, _ = get_login_form_auth_tabs(login_form)

    auto_tab_selection(tab_login, login_form)


def test_auto_auth_selection_from_ls(web_browser):
    '''
    Функция проверяет тест-кейс автоматического опредления аутентификации с таба "Лицевой счёт"
    '''
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    _, _, _, tab_ls = get_login_form_auth_tabs(login_form)

    auto_tab_selection(tab_ls, login_form)


def auth_by_type(login_form, tab_type, username, password):
    '''
    Функция выбираете переданный в параметре tab_type тип аутентификации.
    Вводит в форму логина переданный username, соответствующий типу аутентификации.
    Воодит в форму пароля соотвествующий валидный пароль valid_password, определенный в settings.py
    Нажимает на кнопку войти
    '''

    tab_type.click()

    # найдем формы ввода параметров пользователя и пароля
    input_username = login_form.find_element(By.ID, 'username')
    input_password = login_form.find_element(By.ID, 'password')

    input_username.send_keys(username)
    input_password.send_keys(password)

    # Кнопка "Войти" доступна
    login_btn = login_form.find_element(By.XPATH, '//*[@id="kc-login"]')
    login_btn.click()


def test_auth_with_phone(web_browser):
    '''
    Фунцкция передает тип аeтентификации "Телефон" и значение valid_phone.
    Вызывает auth_by_type.
    Ожидает загрузки страницы личного кабинета пользователя и проверяет значение title страницы,
    соотвествующий странице личного кабинета после успешной аутентификации
    '''
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    tab_phone, _, _, _ = get_login_form_auth_tabs(login_form)

    auth_by_type(login_form, tab_phone, valid_phone, valid_password)

    WebDriverWait(web_browser, 5).until(EC.title_is(rt_title))
    assert web_browser.title == rt_title


def test_auth_with_email(web_browser):
    '''
    Фунцкция передает тип аeтентификации "Почта" и значение valid_mail.
    Вызывает auth_by_type.
    Ожидает загрузки страницы личного кабинета пользователя и проверяет значение title страницы,
    соотвествующий странице личного кабинета после успешной аутентификации
    '''
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    _, tab_email, _, _ = get_login_form_auth_tabs(login_form)

    auth_by_type(login_form, tab_email, valid_mail, valid_password)

    WebDriverWait(web_browser, 5).until(EC.title_is(rt_title))
    assert web_browser.title == rt_title


def test_auth_with_login(web_browser):
    '''
    Фунцкция передает тип аeтентификации "Логин" и значение valid_login.
    Вызывает auth_by_type.
    Ожидает загрузки страницы личного кабинета пользователя и проверяет значение title страницы,
    соотвествующий странице личного кабинета после успешной аутентификации
    '''
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    _, _, tab_login, _ = get_login_form_auth_tabs(login_form)

    auth_by_type(login_form, tab_login, valid_login, valid_password)

    WebDriverWait(web_browser, 5).until(EC.title_is(rt_title))
    assert web_browser.title == rt_title


def test_auth_with_ls(web_browser):
    '''
    Фунцкция передает тип аeтентификации "Лицевой счёт" и значение valid_ls.
    Вызывает auth_by_type.
    Ожидает загрузки страницы личного кабинета пользователя и проверяет значение title страницы,
    соотвествующий странице личного кабинета после успешной аутентификации
    '''
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    _, _, _, tab_ls = get_login_form_auth_tabs(login_form)

    auth_by_type(login_form, tab_ls, valid_ls, valid_password)

    WebDriverWait(web_browser, 5).until(EC.title_is(rt_title))
    assert web_browser.title == rt_title


def test_auth_with_login_and_invalid_password(web_browser):
    '''
    Функция проверяет корректность работы с заведомо неправильным паролем и правильным логином
    '''
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    _, _, tab_login, _ = get_login_form_auth_tabs(login_form)

    auth_by_type(login_form, tab_login, valid_login, invalid_password)

    error_form = WebDriverWait(web_browser, 5).until(EC.presence_of_element_located((By.ID, 'form-error-message')))
    assert error_form.text == "Неверный логин или пароль"


def test_social_network_auth_vk(web_browser):
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    vk_link = login_form.find_element(By.ID, 'oidc_vk')
    vk_link.click()

    WebDriverWait(web_browser, 5).until(EC.title_is(vk_title))
    assert web_browser.title == vk_title


def test_social_network_auth_ok(web_browser):
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    ok_link = login_form.find_element(By.ID, 'oidc_ok')
    ok_link.click()

    WebDriverWait(web_browser, 5).until(EC.title_is(ok_title))
    assert web_browser.title == ok_title


def test_social_network_auth_mail(web_browser):
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    mail_link = login_form.find_element(By.ID, 'oidc_mail')
    mail_link.click()

    WebDriverWait(web_browser, 5).until(EC.title_is(mail_title))
    assert web_browser.title == mail_title


def test_social_network_auth_ya(web_browser):
    login_form = web_browser.find_element(By.XPATH, '//*[@id="page-right"]/div[1]/div[1]')
    ya_link = login_form.find_element(By.ID, 'oidc_ya')
    ya_link.click()

    #link = ya_link.get_attribute('href')
    #web_browser.get(link)

    WebDriverWait(web_browser, 5).until(EC.title_is(ya_title))
    assert web_browser.title == ya_title


def test_help_info_phone(web_browser):
    '''
    Функция проверяет наличие телефона поддержки в footer страницы
    '''
    phone_link = web_browser.find_element(By.CLASS_NAME, 'rt-footer-right__support-phone')
    assert phone_link.text == '8 800 100 0 800'


def test_help_info_cookie(web_browser):
    '''
    Тест проверяет отображение вспомогательной информации для клиента: popup текст с инофрмацией о cookie
    '''
    cookie_link = web_browser.find_element(By.XPATH, '//*[@id="cookies-tip-open"]')
    cookie_link.click()

    cookie_window = web_browser.find_element(By.XPATH, '//*[@id="app-footer"]/div[1]/div[2]/span[1]/div[1]')
    cookie_title = cookie_window.find_element(By.XPATH, '// *[ @ id = "app-footer"] / div[1] / div[2] / span[1]\
                                                         / div[1] / div[2] / span[1]')
    assert cookie_title.text == 'Мы используем Cookie'


def test_user_agreement_from_auth_form(web_browser):
    '''
    Функция проверяет доступность пользовательтского соглашения по ссылке в форме авторизации
    '''
    # сохраним ID текущего окна, как в примере из документации selenium
    original_window = web_browser.current_window_handle

    user_agreement_link = web_browser.find_element(By.LINK_TEXT, u"пользовательского соглашения")
    user_agreement_link.click()

    # из документации selenium эта функция используется для ожидания табов браузера также
    WebDriverWait(web_browser, 10).until(EC.number_of_windows_to_be(2))

    # код из документации selenium для переключения  табов браузера
    for window_handle in web_browser.window_handles:
        if window_handle != original_window:
            web_browser.switch_to.window(window_handle)
            break

    assert web_browser.title == "User agreement"


def test_user_agreement_from_footer(web_browser):
    '''
    Функция проверяет доступность страницы пользовательского соглашения по ссылке с footer
    '''
    # сохраним ID текущего окна, как в примере из документации selenium
    original_window = web_browser.current_window_handle

    user_agreement_link = web_browser.find_element(By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[2]')
    user_agreement_link.click()

    # из документации selenium эта функция используется для ожидания табов браузера также
    WebDriverWait(web_browser, 10).until(EC.number_of_windows_to_be(2))

    # код из документации selenium для переключения  табов браузера
    for window_handle in web_browser.window_handles:
        if window_handle != original_window:
            web_browser.switch_to.window(window_handle)
            break

    assert web_browser.title == "User agreement"


def test_private_policy(web_browser):
    '''
    Функция проверяет доступность страницы "Политика конфеденциальности" по ссылке с footer
    '''
    # сохраним ID текущего окна, как в примере из документации selenium
    original_window = web_browser.current_window_handle

    user_agreement_link = web_browser.find_element(By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[1]')
    user_agreement_link.click()

    # из документации selenium эта функция используется для ожидания табов браузера также
    WebDriverWait(web_browser, 10).until(EC.number_of_windows_to_be(2))

    # код из документации selenium для переключения  табов браузера
    for window_handle in web_browser.window_handles:
        if window_handle != original_window:
            web_browser.switch_to.window(window_handle)
            break

    assert web_browser.title == "Privacy policy"


def test_password_recovery(web_browser):
    '''
    Функция проверяет доступность страницы восстановления пароля
    '''

    forgot_password_link = web_browser.find_element(By.ID, 'forgot_password')
    forgot_password_link.click()

    title = WebDriverWait(web_browser, 5).until(EC.visibility_of_element_located((By.XPATH,
                  '//*[@id="page-right"]/div[1]/div[1]/h1[1]')))

    assert title.text == 'Восстановление пароля'


