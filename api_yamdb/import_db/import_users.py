from csv import DictReader
import sqlite3


with sqlite3.connect('api_yamdb/db.sqlite3') as db_conn:
    print(sqlite3.version)
    with open('api_yamdb/static/data/users.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = DictReader(csvfile)
        for row in csv_reader:
            print(row)
            sql = f"INSERT INTO users_user ('id', 'username', 'role', 'bio'," \
                  f"'first_name', 'last_name', 'email')" \
                  f" VALUES " \
                  f"({row['id']}, '{row['username']}', '{row['role']}', '{row['bio']}'," \
                  f" '{row['first_name']}', '{row['last_name']}', '{row['email']}' )"
            print(sql)
            cur = db_conn.cursor()
            cur.execute(sql)
            db_conn.commit()




