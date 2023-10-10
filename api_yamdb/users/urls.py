from django.urls import path


urlpatterns = [
    path('auth/signup/', ...),  # регистрируем уже лежащего в БД пользователя
    path('auth/token/', ...),  # даем зарегистрированному пользователю jwt-токен
]
