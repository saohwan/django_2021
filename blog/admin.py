from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)


class CategoryAdmin(admin.ModelAdmin): # 위 항목만 입력해도 자동으로 아래 항목까지 써짐
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
