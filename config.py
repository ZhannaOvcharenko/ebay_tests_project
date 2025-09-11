import os
from dotenv import load_dotenv
from appium.options.android import UiAutomator2Options
from utils import file

load_dotenv()  # Загружает переменные из .env.bstack автоматически


def to_driver_options(context: str):
    options = UiAutomator2Options()

    if context == "bstack":
        # Берем remote_url отдельно, не через options
        options.device_name = os.getenv("DEVICE_NAME")
        options.platform_name = os.getenv("PLATFORM_NAME")
        options.platform_version = os.getenv("PLATFORM_VERSION")
        options.app_wait_activity = os.getenv("APP_WAIT_ACTIVITY")

        app_path = file.abs_path_from_project(os.getenv("APP"))
        options.app = app_path

        options.set_capability("bstack:options", {
            "projectName": "eBay Mobile Tests",
            "buildName": "browserstack-build",
            "sessionName": "eBay Mobile Session",
            "userName": os.getenv("BSTACK_USER"),
            "accessKey": os.getenv("BSTACK_KEY"),
        })

    return options
