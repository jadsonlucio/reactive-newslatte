import logging
from rx import of
import rx.operators as ops
from rx.core.pipe import pipe
from rx.scheduler import ThreadPoolScheduler
from GoogleNews import GoogleNews
from newspaper import Article


logger = logging.getLogger(__name__)
thread_pool_scheduler = ThreadPoolScheduler(4)


def op_email_operator(email_sender):
    def send_email(email):
        email_sender.send_email(email["destination"], email["message"])

    return pipe(
        ops.subscribe_on(thread_pool_scheduler),
        ops.map(lambda email: send_email(email))
    )


def op_fetch_news_content():
    def get_article_data(url):
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        return {
            "summary": article.summary,
            "keywords": article.keywords,
            "text": article.text,
            "authors": article.authors,
            "publish_date": article.publish_date,
            "top_image": article.top_image,
            "url": article.url,
            "title": article.title,
        }

    return pipe(
        ops.subscribe_on(thread_pool_scheduler),
        ops.map(lambda url: get_article_data(url)),
    )


def op_googlenews_fetch():
    def fetch_news(subject):
        googlenews = GoogleNews('pt')
        googlenews.get_news(subject)

        logger.info(f" fetch subject {subject} on google news")

        return googlenews.results()[:1]

    return pipe(
        ops.subscribe_on(thread_pool_scheduler),
        ops.flat_map(lambda subject: fetch_news(subject)),
    )


def op_news_from_topic():
    def get_link_from_single_news(single_news_link):
        if not single_news_link.startswith("http"):
            return f"https://{single_news_link}"
        
        return single_news_link

    def get_news_from_topic(topic):
        results = of(*topic["subjects"]).pipe(
            op_googlenews_fetch(),
            ops.filter(lambda single_news: single_news["link"]),
            ops.map(lambda single_news: get_link_from_single_news(single_news["link"])),
            op_fetch_news_content(),
            ops.to_list(),

        ).run()
        return topic, results

    return pipe(
        ops.subscribe_on(thread_pool_scheduler),
        ops.map(get_news_from_topic)
    )
