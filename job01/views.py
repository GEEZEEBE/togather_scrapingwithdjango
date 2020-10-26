from django.shortcuts import render
from pymongo import MongoClient
from django.core.paginator import Paginator

# Create your views here.
def paging(request, datalist, num=10):
    page = request.GET.get('page', '1')
    paginator = Paginator(datalist, num)
    page_obj = paginator.get_page(page)
    page = int(page)
    maxpage = num*((page-1)//num)+10
    minpage = num*((page-1)//num)+1
    return page_obj, maxpage, minpage

def list_job01(request):
    with MongoClient('mongodb://127.0.0.1:27017')  as client:
        jobdb = client.jobdb
        datalist = list(jobdb.datalist.find())
    data = dict()
    page_obj, maxpage, minpage = paging(request, datalist)    
    data['page_obj'] = page_obj
    data['maxpage'] = maxpage
    data['minpage'] = minpage
    return render(request, 'job01/list_job01.html', context=data)