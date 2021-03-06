import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

BASE_CRAIGLIST_URL = "https://bangalore.craigslist.org/search/sss?query={}"
BASE_IMAGE_URL= "https://images.craigslist.org/{}_300x300.jpg"
# Create your views here.
def home(request):
    context={}
    return render(request,'base.html',context)

def new_search(request):
    search=request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url=BASE_CRAIGLIST_URL.format(quote_plus(search))
    response=requests.get(final_url)
    data=response.text
    print(data)
    soup=BeautifulSoup(data,features='html.parser')
    post_listings =soup.find_all('li',{'class':'result-row'})
    print("hi there")
    print(post_listings)
    print("the end of listing")
    # post_title=post_listings[0].find(class_='result-title').text
    # post_url=post_listings[0].find('a').get('href')
    # post_price=post_listings[0].find(class_='result-price').text
    # print(post_listings[0].get('href'))
    # print(post_title)
    # print(post_url)
    # print(post_price)
    final_posting=[]
    for post in post_listings:

        post_title=post.find(class_='result-title').text
        post_url=post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price=post.find(class_='result-price').text
        else:
            post_price='NA'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id=post.find(class_='result-image gallery').get('data-ids').split(':')[1]
            post_image_url=BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        # else:
        #     post_image_url="http://criagslist.org/images/peace.jpg"

        final_posting.append((post_title, post_url, post_price,post_image_url))



    context_from_frontend={
        "search":search,
        "final_postings": final_posting,
    }


    return render (request,'my_app/new_search.html',context_from_frontend)
