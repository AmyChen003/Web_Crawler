from util import get_soup
import response


def process_question(url, tries, writer):
    try:
        soup = get_soup(url)
        qid = url[url.rfind("/")+1:url.rfind(".")]
        # title
        title = soup.find(class_="f18").string
        title = title.string.strip()
        title = title.replace("\n", " ")
        title = title.replace("\r", " ")
        # content
        content = soup.find(class_="f14 lh24 s-c666")
        content = content.get_text().strip()
        content = content.replace("\n", " ")
        content = content.replace("\r", " ")
        q_details = soup.find(class_="cont-time mt20")
        data = q_details.find_all(class_="s-c999")
        location = data[1].get_text().strip()
        date=data[2].get_text().strip()
        reply_num=data[3].get_text().strip()
        writer.question_writer.writerow((qid, date, url, title, content,location,reply_num))
        response.process_responses(soup, qid, 3, writer)
        print("|", end='', flush=True)
    except Exception:
        if tries != 0:
            process_question(url, tries - 1, writer)
        else:
            error = "question error"
            print(".", end='', flush=True)
            writer.question_writer.writerow((url, error))
