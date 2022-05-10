import psycopg2
import lib.db_util as db_util

def init_db():
    db = db_util.DbUtil()
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            username VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(50) NOT NULL,
            created_at TIMESTAMP NOT NULL)
        """,
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id serial PRIMARY KEY,
            name VARCHAR(20) UNIQUE NOT NULL,
            user_id INT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            CONSTRAINT fk_user_id
            FOREIGN KEY (user_id)
            REFERENCES users(id))
        """,
        """
        CREATE TABLE IF NOT EXISTS conversation_users (
            conversation_id INT NOT NULL,
            user_id INT NOT NULL,
            last_accessed_at TIMESTAMP NOT NULL,
            CONSTRAINT fk_conversation_id
            FOREIGN KEY (conversation_id)
            REFERENCES conversations(id),
            CONSTRAINT fk_user_id
            FOREIGN KEY (user_id)
            REFERENCES users(id))
        """
    ]

    for command in commands:
        db.execute(command)
    db.close()

if __name__ == '__main__':
    init_db()