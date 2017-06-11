import os
import re
import time
import random
import fbchat
from mosql.query import insert, select
import sqlite3
from account import ID, PWD


def answer(client, s, cur):
    answer_set = {}
    cur.execute(select('pycon2017'))
    for data in cur.fetchall():
        answer_set[data[0]] = data[1]

    while True:

        msg = client.getThreadInfo('299082580532144', last_n=5)
        msg.reverse()

        msg_list = [x.body for x in msg]
        msg_list = [x for x in msg_list if x != ''][-3:]

        try:
            question = list(filter(lambda x: '題目:' in x, msg_list))[0]
        except:
            print(msg_list)

        print('題目是:\n%s' % question)

        try:
            a = re.search(r'\(A\): (.+)', question).group(1)
        except:
            print('太快了抓不到惹 QQ 先休息一下')
            time.sleep(1)
            continue

        question = re.search(r'題目: (.+)\n', question).group(1)

        if question in answer_set:
            print('之前答過了，答案是：%s' % answer_set[question])
            try:
                client.send('299082580532144', answer_set[question])
            except:
                continue

        else:
            b = re.search(r'\(B\): (.+)', question).group(1)
            c = re.search(r'\(C\): (.+)', question).group(1)
            try:
                d = re.search(r'\(D\): (.+)', question).group(1)
            except:
                d = ""
            try:
                e = re.search(r'\(E\): (.+)', question).group(1)
            except:
                e = ""

            answers = [a, b, c]
            if d:
                answers.append(d)
            if e:
                answers.append(e)

            keyword = list(filter(lambda x: '全部' in x, answers))
            if len(keyword) > 0:
                choice_ans = keyword[0]
            else:
                choice_ans = random.choice(answers)

            print('我猜答案是: %s' % choice_ans)

            client.send('299082580532144', choice_ans)

            time.sleep(2)

            msg = client.getThreadInfo('299082580532144', last_n=5)
            msg.reverse()

            msg_list = [x.body for x in msg]
            answer_status = [x for x in msg_list if x != ''][-3:]

            if '答對對啦～' in answer_status or '答對了 ^^ 加油加油！' in answer_status:

                data = {
                    'question': question,
                    'answer': choice_ans
                }
                cur.execute(insert('pycon2017', data))
                s.commit()

                print('答案猜對了，記起來：%s' % choice_ans)
                answer_set[question] = choice_ans

        time.sleep(3)

def createdb():
    s = sqlite3.connect('sqlite3.db')
    c = s.cursor()
    c.execute('CREATE table pycon2017(question varchar(200), answer varchar(50))')
    s.commit()
    s.close()

if __name__ == '__main__':
    client = fbchat.Client(ID, PWD)

    if not os.path.isfile('sqlite3.db'):
        createdb()

    s = sqlite3.connect('sqlite3.db')
    c = s.cursor()

    answer(client, s, c)

