import os
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


def to_driver_options(context):
    if context == 'bstack':
        platform = os.getenv('PLATFORM_NAME', 'iOS')
        if platform.lower() == 'android':
            options = UiAutomator2Options()
        else:
            options = XCUITestOptions()

        options.set_capability('platformName', os.getenv('PLATFORM_NAME'))
        options.set_capability('platformVersion', os.getenv('PLATFORM_VERSION'))
        options.set_capability('deviceName', os.getenv('DEVICE_NAME'))
        options.set_capability('app', os.getenv('APP'))
        options.set_capability('appWaitActivity', os.getenv('APP_WAIT_ACTIVITY', '*'))
        options.set_capability('bstack:options', {
            'projectName': 'eBay Mobile',
            'buildName': 'browserstack-build-1',
            'sessionName': 'Mobile Test',
            'userName': os.getenv('BSTACK_USER'),
            'accessKey': os.getenv('BSTACK_KEY'),
        })

        options.set_capability('remote_url', os.getenv('REMOTE_URL'))
        return options
