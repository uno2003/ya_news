from datetime import datetime, timedelta
from django.utils import timezone

import pytest
from django.contrib.auth.models import User
from django.conf import settings
from news.models import News, Comment


@pytest.fixture
def author(django_user_model) -> User:
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client) -> User:
    client.force_login(author)
    return client


@pytest.fixture
def news(author) -> News:
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(news, author) -> Comment:
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Comment',
    )
    return comment


@pytest.fixture
def slug_for_news(news) -> tuple:
    return (news.id,)


@pytest.fixture
def slug_for_comment(comment) -> tuple:
    return (comment.id,)


@pytest.fixture
def form_data() -> dict:
    return {
        'text': 'Новый текст'
    }


@pytest.fixture
def list_news(news):
    today = datetime.today()
    list_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        ) for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(list_news)


@pytest.fixture
def comments(news, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст {index}'
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return comments
