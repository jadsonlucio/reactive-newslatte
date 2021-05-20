import logging
import rx
from rx.subject import Subject

logger = logging.getLogger(__name__)


class RedisFetchSubject(Subject):
    def __init__(self, redis_news_queue) -> None:
        super().__init__()
        self._news_queue = redis_news_queue

    def fetch_redis_changes(self, *args):
        obj = self._news_queue.pop()
        if obj is not None:
            logger.info(f" redis queue recieve news {obj}")
            self.on_next(obj)

    def start(self):
        logger.info(f" start redis subject on {self._news_queue}")
        rx.interval(1).subscribe(self.fetch_redis_changes)
