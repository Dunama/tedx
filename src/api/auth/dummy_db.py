class DummyDB:
    def __init__(self):
        self.users = [
            {'id': 1, 'email': 'user1@example.com'},
            {'id': 2, 'email': 'user2@example.com'},
            {'id': 3, 'email': 'user3@example.com'},
        ]

dummy_db = DummyDB()
