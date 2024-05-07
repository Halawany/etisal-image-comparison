import psycopg2 
from datetime import datetime

# conn = psycopg2.connect("dbname=image_comparison user=postgres password=eslam010")
# cur = conn.cursor()

# cur.execute("INSERT INTO image (sn, pre_saved_image, image, result, date_time_added) VALUES (%s, %s, %s, %s, %s)",
#  ("6223000", "pre_saved_image_path", "image_path", "PASS", datetime.date(2024, 5, 6)))

# cur.execute("SELECT * FROM image;")
# print(cur.fetchone())

# conn.commit()

# cur.close()
# conn.close()


class TestToolDB():
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None
    
    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.conn.commit()
        self.conn.close()
    
    def insert_data(self, sn, pre_saved_image, image, result):
        date_time_added = datetime.now()
        try:
            with self.conn.cursor() as curr:
                curr.execute("INSERT INTO image (sn, pre_saved_image, image, result, date_time_added) VALUES (%s, %s, %s, %s, %s)",
                    (sn, pre_saved_image, image, result, date_time_added)
                    )
        except psycopg2.Error as e:
            print(e)