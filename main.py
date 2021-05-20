import asyncio
from rx_newsletter.email_sender import EmailSender
from rx_newsletter.rx_fetchers import RedisFetchSubject
from rx_newsletter.redis_queue import RedisNewsLetterQueue
from rx_newsletter.rx_news import googlenews_fetch_observable, send_newslatter_emails
from rx_newsletter.db_mock import DBMock


def start_fetchers():
    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # start service to verify if new data is in redis queue
    redis_fetch_subject = RedisFetchSubject(redis_news_queue=RedisNewsLetterQueue.get_default_queue())
    redis_fetch_subject.start()

    # create observable that reads the topic data fetched by redis and output the news articles data
    news_fetch = googlenews_fetch_observable(redis_fetch_subject)


    # create email sender and database objects to send email to users
    email_sender = EmailSender.base()
    database = DBMock()
    news_fetch.subscribe(
        lambda data: send_newslatter_emails(database, email_sender, data)
    )

    input("press ctrl+c key to exit\n")
    loop.run_forever()
