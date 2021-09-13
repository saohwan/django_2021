from django.test import TestCase, Client  # Client 가 하는 역할 : 장고에서 재공하는 것이며 웹사이트의 방문자를 말함?
from bs4 import BeautifulSoup
from .models import Post


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 1.1 포스트 목록 페이지 (post list)를 연다.
        response = self.client.get('/blog/')
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)  # 에러 코드가 200이면 정상임
        # 1.3 페이지의 타이틀에 Blog 라는 문구가 있다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('Blog', soup.title.text)  # soup.title.text에 'blog' 라는 문구가 있어야한다. soup 으로 접근
        # 1.4 NavBar 가 있다.
        navbar = soup.nav
        # 1.5 Blog, About me 라는 문구가 Navbar 에 있다.
        self.assertIn('Blog', navbar.text)
        self.assertIn('About', navbar.text)

        # 2.1 게시물이 하나도 없을 때
        self.assertEqual(Post.objects.count(), 0)  # Post 모델에 레코드가 몇개 있는지 아무 겄도 없을때
        # 2.2 메인 영역에 "아직 게시물이 없습니다" 라는 문구가 나온다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 3.1 만약 게시물이 2개 있다면,
        post_001 = Post.objects.create(
            title='첫번째 포스트 입니다.',
            content='Hello, World. we are the World',
        )
        post_002 = Post.objects.create(
            title='두번째 포스트 입니다.',
            content='저는 쌀국수를 좋아합니다.',
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3.2 포스트 목록 페이지를 새로 고침했을 때.
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        # 3.4 "아직 게시물이 없습니다" 라는 문구가 없어야 한다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

