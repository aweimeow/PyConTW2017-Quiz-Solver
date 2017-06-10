import sys
from mosql.query import insert
import sqlite3

if __name__ == '__main__':
    q = input('Question: ')
    a = input('Answer: ')

    data = {
        'question': q,
        'answer': a
    }

    query = insert('pycon2017', data)

    s = sqlite3.connect('sqlite3.db')
    c = s.cursor()

    c.execute(query)
    s.commit()
    s.close()
