from django.shortcuts import render
from pymongo import MongoClient
from django.core.paginator import Paginator

# Create your views here.
from django.shortcuts import render		# add
def home(request):
    return render(request, 'home/home.html')

def startup(req):
    db_url = 'mongodb://192.168.0.171:27017'
    data = {}
    with MongoClient(db_url) as clien:
        startupdb = clien.startupdb
        result = list(startupdb.startup.find({}))
    # 
    page = req.GET.get('page',1)
    result_page = Paginator(result,10)
    data['page_obj'] = result_page.get_page(page)    
    # 
    return render(req, 'home/startup.html',context=data)
