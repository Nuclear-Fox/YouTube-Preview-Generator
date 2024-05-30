import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

# Фикстура для клиента API
@pytest.fixture
def api_client():
    return APIClient()

# Тест успешного получения заголовка видео
@pytest.mark.django_db
def test_get_video_title_success():
    video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Пример URL
    title = get_video_title(video_url)
    assert title is not None, "Должен вернуть заголовок видео"

# Тест ошибки при получении заголовка видео
@pytest.mark.django_db
def test_get_video_title_error():
    video_url = 'https://www.youtube.com/watch?v=invalid'  # Неверный URL
    title = get_video_title(video_url)
    assert title is None, "Должен вернуть None при ошибке"

# Тест перевода текста
@pytest.mark.django_db
def test_translate_text():
    text = 'Привет мир'
    translated_text = translate_text(text, 'en')
    assert translated_text.lower() == 'hello world', "Должен корректно перевести текст"

# Тест создания изображения
@pytest.mark.django_db
def test_make_img_success(api_client):
    video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'  # Пример URL
    response = api_client.post(reverse('make_img'), {'video_url': video_url}, format='json')
    assert response.status_code == 200
    assert 'image_url' in response.data, "Должен вернуть URL изображения"

# Тест ошибки создания изображения
@pytest.mark.django_db
def test_make_img_error(api_client):
    response = api_client.post(reverse('make_img'), {'video_url': ''}, format='json')
    assert response.status_code == 400
    assert 'error' in response.data, "Должен вернуть ошибку при неверном URL"
