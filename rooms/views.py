# from math import ceil
from django.core.paginator import Paginator  # , EmptyPage
from django.shortcuts import render, redirect

# from django.http import Http404
# from django.urls import reverse # template name 을 url로 변환할 때
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

# from django_countries import countries
from . import models, forms

### Class Based Views


class HomeView(ListView):

    """HomeView Definition"""

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

    """RoomDetail Definition"""

    model = models.Room
    # pk_url_kwarg = "pk"
    # url.py 에서 argument(pk)를 찾고 Model Name(Room)을 소문자로 변환해서 context로 pk에 맞는 object와 room을 준다.


class SearchView(View):

    """SearchView Definition"""

    def get(self, request):

        country = request.GET.get("country")

        if country:
            form = forms.SearchForm(request.GET)

            if form.is_valid():
                print(form.cleaned_data)

                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                beds = form.cleaned_data.get("beds")
                bedrooms = form.cleaned_data.get("bedrooms")
                baths = form.cleaned_data.get("baths")
                superhost = form.cleaned_data.get("host")
                instant_book = form.cleaned_data.get("instant_book")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")
                house_rules = form.cleaned_data.get("house_rules")
                room_type = form.cleaned_data.get("room_type")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("-created")
                paginator = Paginator(qs, 10, orphans=5)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)

                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms},
                )
        else:
            form = forms.SearchForm()

        return render(
            request,
            "rooms/search.html",
            {"form": form},
        )


#############################################################################################################################


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
