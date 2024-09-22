from selenium import webdriver
from configparser import ConfigParser
from selenium.webdriver.chrome.service import Service
import logging

# Configurando o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SeleniumDriver:
    def __init__(self, config: ConfigParser):
        logger.info("Inicializando SeleniumDriver")
        self.driver = None
        self.driver_path = config.get('webdriver', 'driver_path')
        self.chrome_options = webdriver.ChromeOptions()
        self.headless = config.getboolean('webdriver', 'headless')

    def set_up(self):
        self._apply_config()
        self.driver = webdriver.Chrome(service=Service(executable_path=self.driver_path), options=self.chrome_options)
        logger.info("ChromeDriver iniciado com sucesso")
        return self.driver

    def exit(self):
        logger.info("Fechando ChromeDriver")
        self.driver.quit()

    def _apply_config(self):
        logger.info("Aplicando configurações do ChromeDriver")
        user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
        prefs = {"download.default_directory": r".\\temp\\"}
        self.chrome_options.add_experimental_option("prefs", prefs)
        self.chrome_options.add_argument(f"--user-agent={user_agent}")
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option("useAutomationExtension", False)
        if self.headless:
            self.chrome_options.add_argument("--headless=new")
        logger.info("Configurações aplicadas com sucesso")
