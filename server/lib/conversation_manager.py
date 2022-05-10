import json

from .db_util import DbUtil

class ConversationManager:
    def __init__(self):
        self.db = DbUtil()

    def add_conversation(self, conv_name, user_id):
        self.insert_conversation(conv_name, user_id)

    def insert_conversation(self, conv_name, user_id):
        self.db.execute(f"INSERT INTO conversations(name, user_id, created_at) VALUES ('{conv_name}', '{user_id}', NOW())")

    def conversation(self, conversation_name):
        return self.db.select("conversations", "name", conversation_name)

    def all_conversations(self):
        return self.db.select_all("conversations")

    def __del__(self):
        print("conversation_manager destroyed")
        self.db.close()

# if __name__ == '__main__':
#     conv_manager = ConversationManager()
#     #conv_manager.add_conversation("test", 4)

#     conversations = json.dumps(conv_manager.conversations(), default=str)
#     print(f"{conversations}")