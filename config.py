import os
from dotenv import load_dotenv
from appium.options.android import UiAutomator2Options
from utils import file

load_dotenv()


def to_driver_options(context: str):
    options = UiAutomator2Options()

    if context == 'bstack':
        # Настройки устройства и приложения
        options.set_capability('deviceName', os.getenv('DEVICE_NAME'))
        options.set_capability('platformName', os.getenv('PLATFORM_NAME'))
        options.set_capability('platformVersion', os.getenv('PLATFORM_VERSION'))
        options.set_capability('appWaitActivity', os.getenv('APP_WAIT_ACTIVITY'))

        app_path = file.abs_path_from_project(os.getenv('APP'))
        options.set_capability('app', app_path)

        # BrowserStack options
        options.set_capability('bstack:options', {
            'projectName': 'eBay Mobile Tests',
            'buildName': 'browserstack-build',
            'sessionName': 'eBay Mobile Session',
            'userName': os.getenv('BSTACK_USER'),
            'accessKey': os.getenv('BSTACK_KEY'),
        })

    elif context == 'local':
        # Локальный запуск (эмулятор/устройство)
        options.set_capability('deviceName', os.getenv('DEVICE_NAME'))
        options.set_capability('platformName', os.getenv('PLATFORM_NAME'))
        options.set_capability('platformVersion', os.getenv('PLATFORM_VERSION'))
        options.set_capability('app', file.abs_path_from_project(os.getenv('APP')))
        options.set_capability('appWaitActivity', os.getenv('APP_WAIT_ACTIVITY'))

    return options
