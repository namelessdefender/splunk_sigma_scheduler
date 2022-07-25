import sqlite3
from contextlib import closing

class Tracker:

    def __init__(self):
        self.db_name = "data/sigma_tracker.db"

        with closing(sqlite3.connect(self.db_name)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("CREATE TABLE IF NOT EXISTS rules (id TEXT, title TEXT, description TEXT, rule TEXT, md5 TEXT, tags TEXT, url TEXT)")


    def update_db_entry(self, rule):
        with closing(sqlite3.connect(self.db_name)) as conn:
            with closing(conn.cursor()) as cursor:
                sql = "UPDATE rules SET md5 = ? WHERE id = ?"
                cursor.execute(sql,(rule.md5, rule.id))
                conn.commit()


    def add_db_entry(self, rule):
        with closing(sqlite3.connect(self.db_name)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("INSERT INTO rules VALUES (?, ?, ?, ?, ?, ?, ?)", (rule.id, rule.title, rule.description, rule.rule, rule.md5, rule.tags, rule.url))
                conn.commit()


    def process(self, rule):
        with closing(sqlite3.connect(self.db_name)) as conn:
            with closing(conn.cursor()) as cursor:
                rows = cursor.execute("SELECT md5 FROM rules WHERE id = ?", (rule.id,)).fetchall()

                if not rows:
                    self.add_db_entry(rule)

                else:
                    if rule.md5 != rows[0][0]:

                        self.update_db_entry(rule)


if __name__ == "__main__":
    pass

