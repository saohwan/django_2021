from django.urls import path
from . import views

urlpatterns = [
    path('category/<str:slug>/', views.category_page), # 소문자로 category_page한 이유는 함수로 만들겠다는 뜻.
    path('<int:pk>/', views.PostDetail.as_view()),
    path('', views.PostList.as_view()),
]
