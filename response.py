def process_responses(soup, qid,tries,writer):
    response=soup.find_all(class_="cont-box")
    if not response:
        return
    try:
        for each in response[1:]:
            lawyer_info = each.find(class_="lawyer-answer clearfix")
            layer_name=lawyer_info.find(class_="s-be f14 fb law-name show-info").get_text().strip()
            info=lawyer_info.find_all(class_="s-c666")
            location=info[0].get_text().strip()
            phone = info[1].get_text().strip()
            help_num = info[2].get_text().strip()
            like_num = info[3].get_text().strip()
            answer = each.find(class_="answer-box")
            reply = answer.find(class_="f14 lh26").get_text().strip()
            date = answer.find(class_="mt10 tr s-c999").get_text().strip()
            reply_like=each.find(class_="mt20 tr")
            reply_like_nums=reply_like.find(class_="dizan")
            reply_like_num=reply_like_nums.find("em").string
            writer.response_writer.writerow(
                (qid, layer_name, location, phone, help_num, like_num, reply, date, reply_like_num))
    except Exception:
        if tries != 0:
            process_responses(soup,qid, tries - 1)
        else:
            error = "response error"
            print(error)
            writer.response_writer.writerow((qid, error))


