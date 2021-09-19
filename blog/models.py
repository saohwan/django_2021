import os
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)  # 글자로 url 을 구분하기 위한 작업 slug

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Post(models.Model):
    title = models.CharField(max_length=50)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()  # 텍스트 필드는 길이를 정의할 필요 없다

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/',
                                   blank=True)  # 파일을 업로드할때 형식 지정 , blank=True는 비워있어도 된다는 뜻
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # models.CASCADE 를 하면 작성자가 작성한 게시글 까지 같이 삭제.
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)  # 카테고리 삭제되더라도 post가 사라지지 않게 SET NULL

    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'  # 고유의 url 정의

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
        # 파이썬에서 제공하는 os라이브러라 패키지를 이용하고,경로 설정후 basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
