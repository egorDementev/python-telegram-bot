import datetime

from data_provider import get_data_base_object

con = get_data_base_object()
cur = con.cursor()


def add_new_person(person_id):
    global con

    sql1, data = 'INSERT INTO Person (id, date) values(?, ?)', []
    data.append((person_id, str(datetime.datetime.now().date())))
    print(data)

    with con:
        con.executemany(sql1, data)


def if_register(person_id) -> bool:
    cursor = con.cursor()

    cursor.execute(f"SELECT id from Person")
    persons = [int(i[0]) for i in cursor.fetchall()]

    return int(person_id) in persons


def if_check(person_id):
    global con
    date = str(datetime.datetime.today().date())
    cursor = con.cursor()
    sqlite_select_query = f"SELECT date from CheckUp where user_id='{person_id}'"
    cursor.execute(sqlite_select_query)
    last_date = cursor.fetchall()
    print(last_date, date)
    if last_date:
        if date == last_date[-1][0]:
            print('already check')
            return False
    return True


def count_today_check_ups(person_id) -> int:
    global con
    date = str(datetime.datetime.today().date())
    cursor = con.cursor()
    sqlite_select_query = f"SELECT date from CheckUp where user_id='{person_id}'"
    cursor.execute(sqlite_select_query)
    last_date = cursor.fetchall()
    print(last_date)
    if last_date:
        count = 0
        while len(last_date) > 0 and date == last_date[-1][0]:
            count += 1
            del last_date[-1]
        return count
    return 0


# TODO: сначала данные добавляются в базу, а только потом рисуется график
def write_check_up(person_id, point, number):
    global con

    now = datetime.datetime.today().date()
    table_name = ['MOOD', 'CALMNESS', 'PRODUCTIVITY', 'ENVIRONMENT', 'SELF_CONFIDENCE', 'PACIFICATION',
                  'SELF_SATISFACTION']

    sql1, data1 = 'INSERT INTO CheckUp (user_id, type_of_graph, date, score) values(?, ?, ?, ?)', []
    data1.append((person_id, table_name[number], now, point))
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
#     con.execute("DELETE from Person;")
#     con.execute("DELETE from Slot;")
#     con.execute("DELETE from Consultation;")
#     con.execute("DELETE from CheckUp;")
#     con.execute("DELETE from Psychologist;")
#     con.execute("DELETE from Transactions;")
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
