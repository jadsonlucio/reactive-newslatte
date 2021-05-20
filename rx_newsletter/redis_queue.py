import json
import redis
from rx_newsletter.settings import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_NEWS_LIST_ID


class RedisNewsLetterQueue:
    instance = None

    def __init__(self, host, port, db, queue_name):
        self._host = host
        self._port = port
        self._db = db
        self._queue_name = queue_name

        self._redis = redis.Redis(host=host, port=port, db=db)

    def enqueue(self, topic_id, topic, subjects):
        dict_news_query = {
            "subjects": subjects,
            "topic": topic,
            "topic_id": topic_id
        }
        self._redis.lpush(self._queue_name, json.dumps(dict_news_query))

    def pop(self):
        response = self._redis.lpop(self._queue_name)

        if response is not None:
            response = json.loads(response)

        return response

    @classmethod
    def get_default_queue(cls):
        if cls.instance is None:
            cls.instance = cls(host=REDIS_HOST, db=REDIS_DB, port=REDIS_PORT, queue_name=REDIS_NEWS_LIST_ID)

        return cls.instance

    def __str__(self) -> str:
        return f"redis://{self._host}:{self._port}/{self._db} on queue {self._queue_name}"
