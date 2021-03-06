from django.urls import path
from rooms import views as room_views

app_name = "core"

# path는 오로지 url 그리고 함수만 갖는다.
urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]
