from util import get_soup,get_dynamic_content
import response


def process_question(url, tries, writer):
    try:
        soup = get_soup(url)
        qid = url[url.rfind("_")+1:url.rfind(".")]
        cate= soup.find(class_="site-location")
        category1=cate.find_all(class_="loc-text")
        law_topic=category1[9].get_text().strip()


        # title
        title = soup.find(class_ ="q-title")
        title = title.string.strip()
        title = title.replace("\n", " ")
        title = title.replace("\r", " ")
        # print(title)
        # content
        content = soup.find(class_="q-detail")
        content = content.get_text().strip()
        content = content.replace("\n", " ")
        content = content.replace("\r", " ")
        # print(content)
        # date location law_topic question_status
        data = soup.find(class_="q-about")
        data1 = data.find_all(class_="about-item")
        date = data1[0].get_text().strip()
        date = date[3:]
        # print(date)
        location = data1[1].get_text().strip()
        location=location[3:]
        # print(location)
        num_answer = data1[2].get_text().strip()
        num_answer=num_answer[0]
        # print(num_answer)

        # dynamic_content include click and number of stars of each response
        answer_ids = soup.find_all(class_="an-zan")
        aid_list = [item["data-aid"] for item in answer_ids]
        dynamic_content = get_dynamic_content(qid, aid_list)
        num_helped = dynamic_content['askClick']

        # lawyer_answer = soup.find_all(class_="lawyer-answer")
        # num_answer = len(lawyer_answer)
        writer.question_writer.writerow((qid, date, url, title, content,law_topic,location, num_helped,num_answer))
        response.process_responses(soup, qid, 3, writer,dynamic_content)
        print("|", end='', flush=True)
    except Exception:
        if tries != 0:
            process_question(url, tries - 1, writer)
        else:
            error = "question error"
            print(".", end='', flush=True)
            writer.question_writer.writerow((url, error))



