import psycopg2
import lib.db_util as db_util

def init_db():
    db = None
    try:
        db = db_util.DbUtil()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id serial PRIMARY KEY,
                username VARCHAR(20) UNIQUE NOT NULL,
                password VARCHAR(50) UNIQUE NOT NULL,
                created_at TIMESTAMP NOT NULL)
            """)
        db.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if db is not None:
            db.close()

if __name__ == '__main__':
    init_db()