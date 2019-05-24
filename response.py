
def process_responses(soup, qid, tries, writer, dynamic_content):
    answer_block = soup.find_all(True, {'class':['badge-best','badge-answer']})

    if not answer_block:
        return
    try:
        for each_answer_block in answer_block:
            lawyer_answer = each_answer_block.find_all(class_="answer")
            for each_lawyer_answer in lawyer_answer:

                answer_type = each_answer_block.find(class_="best-title").get_text().strip()
                # print(answer_type)
                try:
                    layer_info = each_lawyer_answer.find(class_="law-info")
                    layer= layer_info.find_all(class_="info-list")
                    layer_name = layer_info.find(class_="i-name").get_text().strip()
                    # print(layer_name)
                except Exception:
                    layer_name="无"

                try:
                    item=layer[1].find_all(class_="ib-item")
                    layer_phone = item[0].get_text().strip()
                    layer_phone=layer_phone[5:]
                except Exception:
                    layer_phone="无"

                try:
                    num_answered = item[1].get_text().strip()
                    num_answered=num_answered[4:]
                except Exception:
                    num_answered=0

                try:
                    num_good_answers = item[2].get_text().strip()
                    num_good_answers=num_good_answers[4:]
                except Exception:
                    num_good_answers=0


                # try:
                #     office_and_phone = layer_info.find(class_="address")
                #     office = office_and_phone.get_text()[0:office_and_phone.get_text().find("咨询电话")].strip()
                #     phone=office_and_phone.find(class_="num").get_text().strip()
                # except Exception:
                #     office = ""
                #     phone = ""
                # num_good_review=""
                # num_selected=""
                # num_helped=""
                # if len(review)==2:
                #     num_good_review=review[0].find(class_="num").get_text().strip()
                #     num_helped = review[1].find(class_="num").get_text().strip()
                # if len(review)==3:
                #     num_good_review = review[0].find(class_="num").get_text().strip()
                #     num_selected = review[1].find(class_="num").get_text().strip()
                #     num_helped = review[2].find(class_="num").get_text().strip()
                date = each_lawyer_answer.find_all(class_="an-time")
                if len(date) != 1:
                    date = date[1].get_text().strip()
                else:
                    date = date[0].get_text().strip()
                # print(date)
                content = each_lawyer_answer.find(class_="about-text").get_text().strip()
                content = content.replace("\n", " ")
                content = content.replace("\r", " ")
                # print(content)


                try:
                    aid=each_lawyer_answer.find(class_="an-zan")
                    num_stars = dynamic_content['anSupport'][aid['data-aid']]
                except Exception:
                    num_stars = ""

                row = list([qid, layer_name,layer_phone, date, content, num_stars, answer_type, num_answered, num_good_answers])
                # try:
                #     comment_list=[]
                #     comment = each_lawyer_answer.find_all(class_="text-list")
                #     for index in range(len(comment)):
                #         if (index+1)%2==0:
                #             comment_list.append(comment[index].get_text().strip())
                # except Exception:
                #     comment_list = ""
                # row.append(comment_list)

                try:
                    follow_up_questions = each_lawyer_answer.find_all(class_="dialog")
                    if follow_up_questions:
                        for follow_up_question in follow_up_questions:
                            # follow_up_type = follow_up_question.find(class_="reply-type").get_text().strip()
                            follow_up_content = follow_up_question.get_text().strip()
                            follow_up_content = follow_up_content.replace("\n", " ")
                            follow_up_content = follow_up_content.replace("\r", " ")
                            follow_up_content = follow_up_content[3:]
                            # print(follow_up_content)
                            # follow_up_time = follow_up_question.find(class_="reply-time").get_text().strip()
                            # row.append(follow_up_type)
                            # row.append(follow_up_time)
                            row.append(follow_up_content)
                except Exception as e:
                    follow_up_questions=""

                writer.response_writer.writerow(tuple(row))

    except Exception as e:
        # print(traceback.format_exc())
        if tries != 0:
            process_responses(soup,qid, tries - 1, writer)
        else:
            error = "response error"
            print(error)
            writer.response_writer.writerow((qid, error))

