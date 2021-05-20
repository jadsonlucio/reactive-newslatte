users = [{"id": "dsa23a", "email": "jadsonaluno@hotmail.com", "newsletter_topics_id": ["asd1a"]}]
topics = [{"id": "asd1a", "name": "Animes", "subjects": ["atack on titan", "naruto", "yugioh"]}]


class DBMock():
    def __init__(self) -> None:
        pass

    def get_topic_users(self, topic_id):
        response = []
        for user in users:
            if topic_id in user["newsletter_topics_id"]:
                response.append(user)

        return response
