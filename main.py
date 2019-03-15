import csv_writer
from util import get_soup
import question


RETRY_TIMES = 3
BASE_URL = "http://www.66law.cn/question/"


def start():
    print("------Starting 66law crawler------")
    writer = csv_writer.CsvWriter()
    for i in range(3,100):
        url = BASE_URL + str(i)+ ".aspx"
        question.process_question(url,RETRY_TIMES,writer)
    writer.close_file()


if __name__ == '__main__':
    start()
