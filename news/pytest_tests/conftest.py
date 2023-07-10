from datetime import datetime

import pytest

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
        date=datetime.today,
    )
    return news

@pytest.fixture
def comment(author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Comment',
        created=datetime.now()
    )
    return comment

# @pytest.fixture
# def form_data():
#     return {
#         'title': 'Новый заголовок',
#         'text': 'Новый текст',
#     }