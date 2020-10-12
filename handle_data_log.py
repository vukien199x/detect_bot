import argparse

import psycopg2
import os

action_types = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 100, 101,
                103, 104, 106, 107, 200, 201, 202, 203, 204, 205, 206, 207, 208, 1000]
files = ['data_ber.py', 'data_mul.py', 'label.py']

bot_ban_query = "SELECT DISTINCT m.npsn FROM msm_log m WHERE m.type = 0 "
bot_not_ban_query = "SELECT DISTINCT m1.npsn FROM msm_log m1 EXCEPT " \
                    "SELECT DISTINCT m2.npsn FROM msm_log m2 WHERE m2.type = 0 "


def bot_ban_query_with_limit(limit):
    return bot_ban_query + " LIMIT " + str(limit)


def bot_not_ban_query_with_limit(limit):
    return bot_not_ban_query + " LIMIT " + str(limit)


def get_action_of_bot_query(npsn):
    return "SELECT m.type, COUNT(m.type) FROM msm_log m WHERE m.npsn = " + \
           str(npsn) + " GROUP BY m.type ORDER BY m.type"


def delete_file_if_exist():
    for file in files:
        if os.path.exists(file):
            os.remove(file)


def get_data_train(dict_action, type_train):
    result = []
    for action_type in action_types:
        if action_type in dict_action:
            if type_train == 'Mul':
                result.append(dict_action[action_type])
            else:
                result.append(1)
        else:
            result.append(0)
    return result


def convert_list_to_dict(actions):
    dictionary = {}
    for action in actions:
        action_type = action[0]
        count = action[1]
        dictionary[action_type] = count
    return dictionary


def get_query_bot(bot_type, limit):
    if bot_type == 'Ban':
        print("Handling log with bot ban")
        if limit < 1:
            query = bot_ban_query
        else:
            query = bot_ban_query_with_limit(limit)
    else:
        print("Handling log with bot not ban")
        if limit < 1:
            query = bot_not_ban_query
        else:
            query = bot_not_ban_query_with_limit(limit)
    return query


def get_bot_by_type(cursor, bot_type, limit, f_data_mul, f_data_ber, f_label):
    cursor.execute(get_query_bot(bot_type, limit))
    bots = cursor.fetchall()
    print("Number of bot: " + str(len(bots)))
    get_action_bot(cursor, bot_type, bots, f_data_mul, f_data_ber, f_label)


def get_action_bot(cursor, bot_type, bots, f_data_mul, f_data_ber, f_label):
    print("Get action of bot")
    index = 1
    for bot in bots:
        npsn = bot[0]
        cursor.execute(get_action_of_bot_query(npsn))
        dict_action = convert_list_to_dict(cursor.fetchall())
        write_data_train(bot_type, dict_action, f_data_mul, f_data_ber, f_label)
        print(str(index) + ": Handing data action log of bot -> npsn: " + str(npsn))
        index += 1


def write_data_train(bot_type, dict_action, f_data_mul, f_data_ber, f_label):
    data_mul = '    ' + str(get_data_train(dict_action, "Mul")) + ', \n'
    data_ber = '    ' + str(get_data_train(dict_action, "Ber")) + ', \n'
    data_label = '\'Y\'' if bot_type == 'Ban' else '\'N\''
    f_data_mul.write(data_mul)
    f_data_ber.write(data_ber)
    f_label.write('    ' + data_label + ', \n')


def handle_data_log():
    print("Handling log")
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user=opt.user, password=opt.password,
                                      host=opt.host, port=opt.port, database=opt.database)
        limit = opt.limit
        cursor = connection.cursor()
        f_data_mul = open('data_mul.py', 'a')
        f_data_ber = open('data_ber.py', 'a')
        f_label = open('label.py', 'a')
        f_data_mul.write("data = [\n")
        f_data_ber.write("data = [\n")
        f_label.write("label = [\n")
        # Get actions bot ban
        get_bot_by_type(cursor, 'Ban', limit, f_data_mul, f_data_ber, f_label)
        # Get actions bot not ban
        get_bot_by_type(cursor, 'Not_Ban', limit, f_data_mul, f_data_ber, f_label)
        f_data_mul.write("]")
        f_data_ber.write("]")
        f_label.write("]")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', type=str, default='postgres')
    parser.add_argument('--password', type=str, default='postgres')
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=str, default='5432')
    parser.add_argument('--database', type=str)
    parser.add_argument('--limit', type=int, default='0')
    opt = parser.parse_args()
    print("Starting handle data")
    delete_file_if_exist()
    handle_data_log()
    print("Done")
