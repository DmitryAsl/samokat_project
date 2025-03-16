import pytest
from selenium import webdriver
from selene import browser
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from config import config

from helpers.pages.main_page import MainPage
from utils import attach

cookies = [{'domain': 'samokat.ru', 'expiry': 1769106694, 'httpOnly': True, 'name': '__Secure-next-auth.session-token',
             'path': '/', 'sameSite': 'Lax', 'secure': True,
             'value': 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0.._1Wsf_JHNI0F3a0m.HxgCDTjzL7AbVFqf0S4KKO5pr0oWiRXI0ZN3s0xAoD-ZteKy4lsp-8PmVRO9CVMO-gFzfRUY5u8x1R1XeCTWFxurj58w5p8LyDbg4seqxHgLLlG488ml_XEfexUV-ZD97e9CVq2UPvAL1FtVvQ9mTFFAbOneDsupd7VjUTNvEbZjKVP-4v2SoZS--s-gNDqhhO83ssgn7kKnipxJ_QLCpRDN1pzTMFNCYWkMKrt06EQQ5tLp1-5qSGTMAtHLFmgtHqEPRBUempIHh853bnHmK93IIDY2IeVYIP3HXksIBNOvwBSxd1-vjua_1ebNw19JRZ5BVHcXmPlXeaXwP0vyNpPHbKE5TNTRoE3Q5PGDjYe5n-HWgqy6ZFFQzo98m_QQe3KLjHGGmjSGLClLrdG49_2-KPfMqydv2jWLu8dGRvjFT6OfLGy9b7X5XPFZdyBjvt_bLxihY_5GtVds43dEGxPZojhvSk5itMeasBfUvqUM5Ax2DU7iMsw7qBvqxPuy-u61_QVAoMuJ5IzCsXldFcEA2no-xnysysHYwSqo30qtBUCpr1_C_ggKWenE_AwGSAYGuVQoo3xQkyAvFcQfQeedHkWP5gY_v_rlvu2PEDOsyut4L7tG6Eh5_D6rGOmORZU29abqomRprfGZL53WDMxHCBcJL-bjt88GVbzRcXsAvD7A9Mlxlv2Kiu3XdswOrRg3jXcPuLngmP-0JJLRrfTO6-a_NYgLp6QFC5RYCZVGgR6Qje_8nmkjmfzW4dhcWI4o107E_5exfJtcJ-WehPZepwd99AbNemdH-P5b7mOXB9BvlrIvSjIgAo40Dwi4p0MF64CmSQ-fL1mUWT-Z9OaAe9ZIRBf_38rG-RiIivORrBpnPrPiEukzdl4H3vEqAo6tKt3vZfTQYPW-bkjyqrue8Gu-3bNvwyx5Ln0tW04qQ0VXIwsu4O2S67wZp99RTtqrRVwvkOMsjTSCBGm8OuwPKoY5IpeXbC9F1VE8l4BMVhFwZ-k3cyX8Ud-vbVDAhiK97wTyu11WsM20kr412fUsxilW1J5wD_S3tAhwjKvlmk_TobMutQCvWMda3BAoynZk76XG_dFI8z6aeWtZOjoFI2m-dxoXGL1S0PfBgK1fipLkhE2WIMWHKT4MrSiXumj5aC3JxUMX3dsq.mn1bCppn4H8BkVe7TlZI7Q'},
           {'domain': 'samokat.ru', 'expiry': 1737657102, 'httpOnly': False, 'name': 'CITY_BY_IP_STATUS', 'path': '/',
             'sameSite': 'Lax', 'secure': False, 'value': '%22CONFIRMED%22'},
           {'domain': 'samokat.ru', 'expiry': 1737950784, 'httpOnly': False, 'name': 'SELECTED_ADDRESS_KEY',
             'path': '/', 'sameSite': 'Lax', 'secure': False,
             'value': '{"id":157264919,"region":"Москва","city":"Москва","street":"Загородное шоссе","district":"Донской","house":"10 к5","lat":55.693559,"lon":37.601984}'},
           ]


@pytest.fixture(scope='function', autouse=True)
def browser_config():
    browser_name = config.browser_name
    browser.config.driver_name = browser_name
    browser_version = config.browser_version
    run_mode = config.run_mode
    options = Options() if browser_name == 'chrome' else webdriver.FirefoxOptions()
    login = config.login
    password = config.password

    options.page_load_strategy = 'eager'
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-cache")

    if run_mode == 'remote':
        selenoid_capabilities = {
            "browserName": browser_name,
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            }
        }
        options.capabilities.update(selenoid_capabilities)
        driver = webdriver.Remote(
            command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
            options=options)
    else:
        if browser_name == 'chrome':
            driver = webdriver.Chrome(options=options)
        elif browser_name == 'firefox':
            driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f'Unsupported broswer: {browser_name}')

    browser.config.driver = driver
    browser.config.window_width = config.window_width
    browser.config.window_height = config.window_height
    browser.config.base_url = config.base_url

    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()


@pytest.fixture(scope='function')
def browser_with_selected_address(browser_config):
    main_page = MainPage()
    main_page.open()

    for cookie in cookies:
        browser.driver.add_cookie(cookie)

    # одной перезагрузки страницы почему то хватает не всегда
    main_page.open()
    main_page.open()
