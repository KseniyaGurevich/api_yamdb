from csv import DictReader
import sqlite3


with sqlite3.connect('api_yamdb/db.sqlite3') as db_conn:
    print(sqlite3.version)
    with open('api_yamdb/static/data/titles.csv', 'r',
              encoding='utf-8') as csvfile:
        csv_reader = DictReader(csvfile)
        for row in csv_reader:
            print(row)
            sql = f"INSERT INTO reviews_title ('id', 'name', 'year', 'category_id')" \
                  f" VALUES " \
                  f"({row['id']}, '{row['name']}', '{row['year']}', '{row['category']}')"
            print(sql)
            cur = db_conn.cursor()
            cur.execute(sql)
            db_conn.commit()
