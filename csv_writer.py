import csv


class CsvWriter:
    __question_header = ["QID", "DATE", "URL", "TITLE", "CONTENT", "LOCATION","PHONE"]
    __response_header = ["QID", "LAWYER_NAME","LOCATION","PHONE","HELP_NUM","LIKE","REPLY","DATE","REPLY_LIKE_NUM"]
    question_writer = None
    response_writer = None

    def __init__(self):
        self.__questionfile = open("questions_" + ".csv", 'w', 1, encoding='utf-8')
        self.__responsefile = open("responses_" + ".csv", 'w', 1, encoding='utf-8')
        self.question_writer = csv.writer(self.__questionfile)
        self.response_writer = csv.writer(self.__responsefile)
        self.question_writer.writerow(self.__question_header)
        self.response_writer.writerow(self.__response_header)

    def close_file(self):
        self.__questionfile.close()
        self.__responsefile.close()
