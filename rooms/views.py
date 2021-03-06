# from math import ceil
# from django.core.paginator import Paginator, EmptyPage
# from django.shortcuts import render, redirect
# from django.http import Http404
# from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from . import models

### Class Based Views


class HomeView(ListView):

    """ HomeView Definition """

    context_object_name = "rooms"
    model = models.Room
    paginate_by = 10
    ordering = "created"
    paginate_orphans = 5
    page_kwarg = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


class RoomDetail(DetailView):

    """ RoomDetail Definition"""

    model = models.Room
    # pk_url_kwarg = "pk"
    # url.py 에서 argument(pk)를 찾고 Model Name(Room)을 소문자로 변환해서 context로 pk에 맞는 object와 room을 준다.


# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", context={"room": room})
#     except models.Room.DoesNotExist:
#         # error object를 만들어서 return 하는 것이 아니니 raise 사용
#         # tempalte 안의 404.html 찾음. 없으면 기본 404 페이지
#         raise Http404()


# def all_rooms(request):

### 수동적인 방법

# page = request.GET.get("page", 1)
# try:
#     page = int(page or 1)
#     if page < 1:
#         page = 1
# except ValueError:
#     page = 1
# page_size = 10
# limit = page_size * page
# offset = limit - page_size
# all_rooms = models.Room.objects.all()[offset:limit]
# page_count = ceil(models.Room.objects.count() / page_size)  # 전체 페이지 계산

# return render(
#     request,
#     "rooms/home.html",
#     context={
#         "rooms": all_rooms,
#         "page": page,
#         "page_count": page_count,
#         "page_range": range(1, page_count + 1),
#     },
# )

### Django paginator의 도움을 받는 방법

# def all_rooms(request):

# page = request.GET.get("page", 1)
# room_list = models.Room.objects.all()  # QuerySet are lazy. 쿼리셋만 있고 데이터는 호출할 때 불러온다.
# paginator = Paginator(room_list, 10, orphans=5)
# try:
#     rooms = paginator.page(int(page))
#     return render(request, "rooms/home.html", {"rooms": rooms})
# except EmptyPage:
#     # rooms = paginator.page(1) url 개판 되는 걸 막기 위해 이거 대신 redirect 할거임
#     return redirect("/")
# except ValueError:
#     return redirect("/")
