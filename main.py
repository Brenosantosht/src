# main
import os
from time import sleep
from threading import Condition, Thread
from configparser import ConfigParser
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import boto3
from driver import SeleniumDriver


BASE_URL = "https://dados.pbh.gov.br/dataset/tempo_real_onibus_-_coordenada/"\
            "resource/d7ce6e9b-343f-4e83-8b46-68fa90a12d59"
TEMP_DIR = './temp/'
SCRAPING_FINISHED = False



if __name__ == "__main__":
    write_key_count = 10
    write_item_size = 1000
    print(
        f"Writing {write_key_count*write_key_count} items to the table. "
        f"Each item is {write_item_size} characters."
    )
    write_data_to_dax_table(write_key_count, write_item_size)



def write_to_db():
    global SCRAPING_FINISHED

    if dyn_resource is None:
        dyn_resource = boto3.resource("dynamodb")

    if same_files():
        os.remove(TEMP_DIR)

    table = dyn_resource.Table("TryDaxTable")
    some_data = "X"

    for partition_key in range(1, key_count + 1):
        for sort_key in range(1, key_count + 1):
            table.put_item(
                Item={
                    "partition_key": partition_key,
                    "sort_key": sort_key,
                    "some_data": some_data,
                }
            )


def same_files():
    try:
        files = os.scandir(TEMP_DIR)
        files_sizes = []

        for file in files:
            if file.is_file():
                files_sizes.append(file.stat().st_size)

        if len(files_sizes) < 2:
            return True

        elif files_sizes[0] == files_sizes[1]:
            return True

        elif files_sizes[0] != files_sizes[1]:
            return False


    except Exception.with_traceback() as e:
        print(e)


def download(condition):
    try:
        config = ConfigParser()
        config.read('./config.ini')
        driver = SeleniumDriver(config)
        browser = driver.set_up()
        browser.get(BASE_URL)
        while True:
            try:
                download_btn = WebDriverWait(browser, 25).until(ec.visibility_of_element_located(
                    (By.CLASS_NAME, "btn.btn-primary.resource-url-analytics")
                )
                )
                download_btn.click()
                sleep(7)
                condition.notify()
            except Exception.with_traceback() as e:
                print(e)
                browser.refresh()
        # browser.quit()

    except Exception.with_traceback() as e:
        print(e)


def main():
    global SCRAPING_FINISHED
    try:
        condition = Condition()
        writer_thread = Thread(target=write_to_db, args=())
        writer_thread.daemon = True
        writer_thread.start()
        download(condition)

    except Exception.with_traceback() as e:
        print(e)
        os.remove(TEMP_DIR)


if __name__ == '__main__':
    while True:
        main()
