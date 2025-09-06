from pydantic import BaseSettings


class MobileConfig(BaseSettings):
    bstack_user: str
    bstack_key: str
    bstack_app: str
    bstack_device: str = "Google Pixel 6"
    bstack_os_version: str = "12.0"
    project: str = "eBay Mobile Tests"
    build: str = "browserstack-build"
    name: str = "ebay-automation"

    class Config:
        env_file = ".env.bstack"


mobile_config = MobileConfig()
