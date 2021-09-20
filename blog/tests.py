from django.test import TestCase, Client  # Client 가 하는 역할 : 장고에서 재공하는 것이며 웹사이트의 방문자를 말함?
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User  # 장고에서 기본적으로 제공하는 User 임.


class TestView(TestCase):
    def setUp(self):  # DB에 들어갈 내용을 여기서 테스트 적용
        self.client = Client()
        self.user_trump = User.objects.create_user(
            username='trump',
            password='somepassword',
        )
        self.user_obama = User.objects.create_user(
            username='obama',
            password='somepassword',
        )

        self.category_programming = Category.objects.create(
            name='programming', slug='programming'
        )
        self.category_music = Category.objects.create(
            name='music', slug='music'
        )

        self.post_001 = Post.objects.create(
            title='첫번째 포스트 입니다.',
            content='Hello, World. we are the World',
            category=self.category_programming,
            author=self.user_trump
        )
        self.post_002 = Post.objects.create(
            title='두번째 포스트 입니다.',
            content='저는 쌀국수를 좋아합니다.',
            category=self.category_music,
            author=self.user_obama
        )
        self.post_003 = Post.objects.create(
            title='세번째 포스트 입니다.',
            content='Category가 없나유.',
            author=self.user_obama
        )

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Saohwan')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me')

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)  # 카테고리스라는 문구가 categories_card 에 있는지 확인하는 테스트
        self.assertIn(
            f'{self.category_programming} ({self.category_programming.post_set.count()})',
            categories_card.text
        )
        self.assertIn(
            f'{self.category_music} ({self.category_music.post_set.count()})',
            categories_card.text
        )  # 이렇게 하는 이유는 유지 보수성을 위해
        self.assertIn(
            f'미분류 ({Post.objects.filter(category=None).count()})',
            categories_card.text
        )

    def test_post_list_with_posts(self):
        self.assertEqual(Post.objects.count(), 3)  # 시작하자마자 포스트가 3개있다.

        # 1.1 포스트 목록 페이지 (post list)를 연다.
        response = self.client.get('/blog/')  # 블로그 페이지가서 읽고
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)  # 에러 코드가 200이면 정상임
        # 1.3 페이지의 타이틀에 Blog 라는 문구가 있다.
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertIn('Blog', soup.title.text)  # soup.title.text에 'blog' 라는 문구가 있어야한다. soup 으로 접근

        self.navbar_test(soup)  # 블로그라는게 헤더 타이틀에 있는지 확인\
        self.category_card_test(soup)

        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        # 3.4 "아직 게시물이 없습니다" 라는 문구가 없어야 한다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)

        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)  # upper 대문자로 나왔으면 좋겠을 때.

    def test_post_list_without_posts(self):
        Post.objects.all().delete()

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)  # 에러 코드가 200이면 정상임

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.assertIn('Blog', soup.title.text)

        self.assertEqual(Post.objects.count(), 0)  # Post 모델에 레코드가 몇개 있는지 아무 겄도 없을때

        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        self.assertEquals(Post.objects.count(), 3)  # 테스트는 생성할때마다 DB가 초기화되서 0이다.
        # 1.2 그 포스트의 url은 '/blog/1/' 이다.
        self.assertEquals(self.post_001.get_absolute_url(), '/blog/1/')

        # 2 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번쨰 포스트의 url로 접근하면 정상적으로 response가 온다..(status code: 200).
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        # 2.2 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        self.navbar_test(soup)


        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)
        # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        # 2.5 첫 번째 포스트의 작성자(author)가 포스트 영역에 있다.(아직 구현할 수 없음).
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(self.post_001.content, post_area.text)
