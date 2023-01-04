# use selenium for web crawler
import time
import os
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from tqdm import tqdm, trange
# keyboard support
from selenium.webdriver.common.keys import Keys
import csv

import numpy as np
import re
import pandas as pd

# create a driver using firefox
page_number = 94
repo_name = "github/docs"
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("blink-settings=imagesEnabled=false")


def issue_href_collection(start, end, repo):
    driver = webdriver.Firefox(options=options)
    href_elem = []
    for i in trange(start, end):
        driver.get("https://github.com/" + repo + "/issues?page=" + str(i) + "&q=is%3Aissue")
        # find html element by name
        elem = driver.find_elements(By.XPATH, "//a[contains(@href, \'/github/docs/issues/\')]")
        # element input clear
        for j in elem:
            text = j.get_attribute('href')
            href_elem.append(text.replace('/linked_closing_reference?reference_location=REPO_ISSUES_INDEX', ''))
    driver.close()
    a = np.asarray(href_elem)
    a = np.unique(a)
    return a


def title_label_collection(href_elem):
    driver = webdriver.Firefox(options=options)
    final = []
    for i in tqdm(href_elem):
        driver.get(i)
        temp = []
        title = driver.find_element(By.XPATH, "//h1/span").get_attribute("textContent")
        try:
            label = driver.find_element(By.XPATH, "//div[2]/a/span").get_attribute('textContent')
        except NoSuchElementException:
            label = ""
        temp.append(i)
        temp.append(title)
        temp.append(label)
        final.append(temp)
    driver.close()
    return final


def main():
    href_elem = issue_href_collection(1, page_number, repo_name)
    final = title_label_collection(href_elem)
    b = np.asarray(final)
    pd.DataFrame(b).to_csv('info.csv')


if __name__ == '__main__':
    s = time.time()
    main()
    e = time.time()
    print('time：', e - s)
