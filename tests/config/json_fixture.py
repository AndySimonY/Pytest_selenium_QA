class JSONFixture:

    @staticmethod
    def for_create_post(text):
        json = {
            "title": text,
            "body": text,
            "userId": 1,
        }
        return json