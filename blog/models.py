from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()  # 텍스트 필드는 길이를 정의할 필요 없다

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # author : 추후 작성 예정

    def __str__(self):
        return f'[{self.pk}] {self.title}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'  # 고유의 url 정의
