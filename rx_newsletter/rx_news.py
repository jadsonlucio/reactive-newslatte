from jinja2 import Template
from rx_newsletter.operators import op_news_from_topic
from rx_newsletter.settings import NEWLETTER_TEMPLATE_PATH


def googlenews_fetch_observable(news_feed_observable):
    return news_feed_observable.pipe(
        op_news_from_topic()
    )


def format_to_html(articles):
    template = Template(open(NEWLETTER_TEMPLATE_PATH).read())
    return template.render(articles=articles)


def format_to_message(articles):
    return str(articles)


def get_emails(articles_data, users):
    html = format_to_html(articles_data)
    message = format_to_message(articles_data)

    emails = []
    for user in users:
        emails.append({
            "destination": user["email"],
            "message": message.encode("utf-8"),
            "html": html
        })

    return emails


def send_newslatter_emails(database, email_sender, data):
    topic, articles_data = data
    users = database.get_topic_users(topic["topic_id"])
    emails = get_emails(articles_data, users)

    for email in emails:
        email_sender.send_email_with_html(
            email["destination"], f"Newsletter {topic['topic']}", email["message"], email["html"]
        )
