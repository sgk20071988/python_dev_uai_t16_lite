from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import PostForm
from .models import Post


class PostModelTest(TestCase):
    def setUp(self):
        # Создаем тестовый пост (выполняется перед каждым тестом)
        self.post = Post.objects.create(
            title="Тестовый заголовок",
            content="Тестовое содержание поста."
        )

    def test_post_creation(self):
        """Проверяем, что пост создается и строковое представление работает"""
        self.assertEqual(self.post.title, "Тестовый заголовок")
        self.assertEqual(str(self.post), "Тестовый заголовок")
        self.assertIsNotNone(self.post.created_at) # Проверяем, что дата записи автоматически заполнилась

    def test_get_absolute_url(self):
        """Проверяем, что метод get_absolute_url возвращает правильный URL"""
        # Если вы добавили get_absolute_url в модель (Способ 2 из прошлого шага)
        if hasattr(self.post, 'get_absolute_url'):
            expected_url = reverse('blog:post_detail', kwargs={'pk': self.post.pk})
            self.assertEqual(self.post.get_absolute_url(), expected_url)


class UrlsTest(TestCase):
    def test_post_list_url(self):
        """Тест главной страницы (список постов)"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url(self):
        """Тест детальной страницы поста"""
        post = Post.objects.create(title="Пост для URL", content="Текст")
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_create_url(self):
        """Тест страницы создания поста (GET запрос)"""
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 200)

    def test_about_url(self):
        """Тест страницы 'О нас'"""
        response = self.client.get(reverse('about')) # Или 'blog:about', в зависимости от вашего urls.py
        self.assertEqual(response.status_code, 200)


class PostViewsTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title="Существующий пост",
            content="Какой-то текст"
        )

    def test_post_list_view(self):
        """Проверяем, что ListView передает правильный контекст и использует правильный шаблон"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')
        self.assertContains(response, "Существующий пост")
        # Проверяем имя переменной в контексте (зависит от вашего view)
        self.assertIn('posts', response.context) 

    def test_post_detail_view(self):
        """Проверяем детальную страницу"""
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)

    def test_post_detail_view_404(self):
        """Проверяем, что несуществующий пост возвращает 404"""
        response = self.client.get(reverse('blog:post_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_post_create_view_post(self):
        """Проверяем, что POST-запрос создает новый пост"""
        data = {
            'title': 'Новый пост через тест',
            'content': 'Текст, созданный программой.'
        }
        response = self.client.post(reverse('blog:post_create'), data)
        self.assertEqual(response.status_code, 302) # 302 - это редирект после успешного создания
        self.assertEqual(Post.objects.count(), 2) # Был 1 (в setUp) + 1 новый = 2
        self.assertTrue(Post.objects.filter(title='Новый пост через тест').exists())

    def test_post_update_view(self):
        """Проверяем, что PUT/POST-запрос обновляет пост"""
        url = reverse('blog:post_edit', kwargs={'pk': self.post.pk})
        data = {
            'title': 'Обновленный заголовок',
            'content': 'Новый текст'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Редирект после успеха
        self.post.refresh_from_db() # Обновляем данные из базы
        self.assertEqual(self.post.title, 'Обновленный заголовок')
        self.assertEqual(self.post.content, 'Новый текст')

    def test_post_delete_view(self):
        """Проверяем удаление поста"""
        url = reverse('blog:post_delete', kwargs={'pk': self.post.pk})
        response = self.client.post(url) # Отправляем POST для подтверждения удаления
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0) # Пост удален, база пуста