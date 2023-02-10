import sqlite3 as sl
import datetime

con = sl.connect('db//connection.db')
cur = con.cursor()


def add_new_person(id, problems):
    global con

    sql1, data1 = 'INSERT INTO Person (id, problems, sub_id) values(?, ?, ?)', []
    data1.append((id, problems, -1))

    with con:
        con.executemany(sql1, data1)


def if_register(id):
    cursor = con.cursor()
    sqlite_select_query = f"SELECT id from Person"
    cursor.execute(sqlite_select_query)
    persons = [int(i[0]) for i in cursor.fetchall()]
    print(persons)
    if int(id) in persons:
        return True
    return False


def if_check(id):
    global con
    date = str(datetime.datetime.today().date())
    cursor = con.cursor()
    sqlite_select_query = f"SELECT date from CheckUp where user_id='{id}'"
    cursor.execute(sqlite_select_query)
    last_date = cursor.fetchall()
    print(last_date, date)
    if last_date:
        if date == last_date[-1][0]:
            print('already check')
            return False
    return True


# TODO: сначала данные добавляются в базу, а только потом рисуется график
def check_up(id, points):
    global con

    points = points.split(' ')
    now = datetime.datetime.today().date()
    table_name = ['MOOD', 'ANXIETY', 'PROCRASTINATION', 'LONELINESS', 'DOUBT', 'CONDEMNING']

    for i in range(6):
        sql1, data1 = 'INSERT INTO CheckUp (user_id, type_of_graph, date, score) values(?, ?, ?, ?)', []
        data1.append((id, table_name[i], now, points[i]))
        with con:
            con.executemany(sql1, data1)


# with con:
# print(list(con.execute(f"SELECT id FROM Psychologist")))
# print(datetime.date(2022, 12, 30).isocalendar())
# print(datetime.datetime.today().isocalendar()[1])
# sql1, data1 = 'INSERT INTO CheckUp (user_id, type_of_graph, date, score) values(?, ?, ?, ?)', []
# data1.append((596752948, 'MOOD', '2022-12-19', 3))
# with con:
#     con.executemany(sql1, data1)

#     print(str(list(con.execute(f"SELECT time_for_check_up FROM PERSONS"))[0]))
# # check_up('111', '4 2 2 0 3')
# with con:
    # con.execute("DELETE from Person;")
#     con.execute("DELETE from Slot;")
#     con.execute("DELETE from Consultation;")
#     con.execute(f"UPDATE Slot SET is_free='0' WHERE date='2023-01-15' and time='22:30';")
#     print(list(con.execute(f"SELECT id FROM Psychologist;")))
#     print(list(con.execute(f"SELECT COUNT(*) FROM Psychologist")))
#     print(list(con.execute(f"SELECT problems FROM Person WHERE id={596752948}"))[0][0])
# with con:
#     range_date = 6 - datetime.datetime.today().weekday()
# print(list(con.execute(f"SELECT date FROM Slot Where psycho_id='{}';")))
# print(datetime.time.fromisoformat('04:23') > datetime.time.fromisoformat('14:58'))
# print(str(datetime.datetime.now().date()) + ' ' + str(datetime.datetime.now().time()))
# print(list(con.execute(f"SELECT id FROM Transactions WHERE "
#                                        f"user_id='{596752948}' and is_diagnostic='{True}'")))
# sql1, data1 = 'INSERT INTO Transactions (user_id, date, time, is_diagnostic) values(?, ?, ?, ?)', []
# data1.append(('42323424', str(datetime.datetime.now().date()),
#                       str(datetime.datetime.now().time()), True))
#
# with con:
#     con.executemany(sql1, data1)
# s = ['xx', 'yyy', 'aaaaa']
# print(max(s, key=len))

# maxa = 0
# for a in range(0, 100):
#     for x in range(0, 10000):
#         for y in range(0, 10000):
#             if (x > a) or (y > a) or (y - 2 * x + 12 != 0):
#                 maxa = max(maxa, a)
#             else:
#                 break
# print(maxa)
