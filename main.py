import csv_writer
from util import get_soup
import question
import sys

START_MONTH = int(sys.argv[2])
START_YEAR = int(sys.argv[1])
PROVINCE_URL_PART = sys.argv[3]
PROVINCE_NAME = sys.argv[4]
RETRY_TIMES = 3
BASE_URL = "http://china.findlaw.cn/ask/"

print(START_MONTH, START_YEAR, PROVINCE_URL_PART, PROVINCE_NAME)


def start():
    print("------Starting findlaw crawler------")
    year = START_YEAR
    month = START_MONTH
    if month < 10:
        url = BASE_URL + PROVINCE_URL_PART + "_d" + str(year) + "0" + str(month)
    else:
        url = BASE_URL + PROVINCE_URL_PART + "_d" + str(year) + str(month)

    writer = csv_writer.CsvWriter(PROVINCE_NAME, year, month)
    last_page_number = None
    page_try = RETRY_TIMES
    while last_page_number is None:
        if page_try != 0:
            last_page_number = get_last_page_number(url)
            page_try = page_try - 1
        else:
            print("**** last_page_number failed after 3 tries")
            exit()

    for page_index in range(1, last_page_number + 1):
        print("Processing page: prov=" + PROVINCE_NAME + " year=" + str(year) + " month=" + str(month) +
              " page=" + str(page_index) + "/" + str(last_page_number))
        new_url = url + "_page" + str(page_index) + "/"
        process_page(new_url, RETRY_TIMES, writer)
        print("")
    writer.close_file()


def get_last_page_number(url):
    try:
        soup = get_soup(url)
        page_index = soup.find(class_="common-pagination")
        next_tag = page_index.find("a", string='尾页')
        last_page = next_tag['href'][next_tag['href'].rfind('_'):]
        last_page_number = int(last_page[last_page.find('e') + 1:last_page.find('/')])
        return last_page_number
    except Exception:
        print("get last page number failed!")
        return None


def process_page(url, tries, writer):
    try:
        soup = get_soup(url)
        question_list = soup.find_all(class_="result-lawyer-item")
        for item in question_list:
            question_url = item.find('a', href=True)
            if question_url['href'].startswith(BASE_URL):

                question.process_question(question_url['href'], RETRY_TIMES, writer)
    except Exception:
        if tries != 0:
            process_page(url, tries - 1, writer)
        else:
            print("**** process_page failed after 3 tries")
            exit()


if __name__ == '__main__':
    start()
