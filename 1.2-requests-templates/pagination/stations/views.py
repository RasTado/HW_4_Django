import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    with open('data-398-2018-08-30.csv', mode='r', encoding='utf-8') as csvfile:
        content = list(csv.DictReader(csvfile))
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(content, 10)
    page = paginator.get_page(page_number)

    context = {
        'bus_stations':  page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
