import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
# from django.db import models
from . import models
# Create your views here.


BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)    
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # print (final_url)
    # response = requests.get('https://losangeles.craigslist.org/search/bbb?query=python%20tutor&sort=rel')
    response = requests.get(final_url)
    data = response.text 
    soup = BeautifulSoup(data, features='html.parser')
    
    post_listings = soup.find_all('li', {'class': 'result-row'})
    # post_title = post_listings[0].find(class_='result-title').text
    # post_url =  post_listings[0].find('a').get('href')
    # post_price =  post_listings[0].find(class_='result-price').text
    # print('-----------------')
    # print (post_title)
    # print (post_url)
    # print (post_price )
    # print('-----------------')
    
    final_postings =[]

    for post in post_listings :
        post_title = post.find(class_='result-title').text
        post_url =  post.find('a').get('href')

        # this is about price
        if post.find(class_='result-price') :
            post_price =  post.find(class_='result-price').text
        else :
            post_price = 'NA'
        
        # and now time to look for images
        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
            'search': search,
            'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)