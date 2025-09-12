import os
from appium.options.android import UiAutomator2Options


def to_driver_options(context):
    options = UiAutomator2Options()

    if context == "bstack":
        options.platform_name = os.getenv("PLATFORM_NAME")
        options.platform_version = os.getenv("PLATFORM_VERSION")
        options.device_name = os.getenv("DEVICE_NAME")
        options.app = os.getenv("APP")
        options.app_wait_activity = os.getenv("APP_WAIT_ACTIVITY")

        # BrowserStack credentials и настройки проекта
        options.set_capability("bstack:options", {
            "userName": os.getenv("BSTACK_USER"),
            "accessKey": os.getenv("BSTACK_KEY"),
            "projectName": "eBay Mobile",
            "buildName": "bs-build-1",
            "sessionName": "Ebay Tests"
        })

    return options
