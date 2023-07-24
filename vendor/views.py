from django.shortcuts import render, loader, get_object_or_404
from .models import Vendor
from django.http import HttpResponse, Http404
from .forms import VendorModelForm ,RawVendorForm
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView
# context 是我們從資料庫撈回來的資料，並使用 key 去指向這些資料
#rendor可以將我們要傳達的資料一併打包，再透過 HttpResponse 回傳到瀏覽器
# Create your views here.
def vendor_index(request):
    vendor_list = Vendor.objects.all() # 把所有 Vendor 的資料取出來
    context = {'vendor_list': vendor_list} # 建立 Dict對應到Vendor的資料，前方list對應html，後方的list為上面那排list
    return render(request, 'vendors/vendor_detail.html', context)
'''
# 針對 vendor_create.html
def vendor_create_view(request):
    form = VendorForm(request.POST or None)
    if form.is_valid(): #is_vaild : 建立在 form 底下的方法，可以用來驗證資料是否正確
        form.save()
        form = VendorForm() # 清空 form

    context = {
        'form' : form
    }
    return render(request, "vendors/vendor_create.html", context)
#透過From，針對使用者填入的內容做處理及判斷，最後再做出相對應的處理
'''
def vendor_create_view(request):
    form = RawVendorForm(request.POST or None)
    if form.is_valid():
        Vendor.objects.create(**form.cleaned_data)
        #因為 create 裡面所帶的參數為 **kwargs，故傳入 Dict 就必須加上 ** 來 unpack
        form = RawVendorForm()
    context = {
        'form' : form
    }
    return render(request, "vendors/vendor_create.html", context)

class VendorUpdateView(UpdateView):
    form_class = VendorModelForm # 使用的表單類別
    template_name = 'vendors/vendor_create.html'
    queryset = Vendor.objects.all() # 這很重要
    #加上 queryset 的原因是因為UpdateView 會呼叫 get_object()

def singleVendor(request, id):
    vendor_list = get_object_or_404(Vendor, id=id)#例外處理
    #try:
    #    vendor_list = Vendor.objects.get(id=id)
    # except Vendor.DoesNotExist:
    #    raise Http404
    context = {
        'vendor_list': vendor_list
    }
    return render(request, 'vendors/vendor_detail.html', context)
# 繼承 ListView
class VendorListView(ListView):
    model = Vendor #要使用哪一個資料庫
    template_name = 'vendors/vendor_list.html' #要使用哪一個 template，命名之後才能覆寫
# 繼承 DetailView
class VendorDetailView(DetailView):
    model = Vendor #與下行同義
    # queryset = Vendor.objects.all()
    template_name = 'vendors/vendor_detail.html'
# 繼承 CreateView
class VendorCreateView(CreateView):
    form_class = VendorModelForm # 使用的表單類別
    # model = Vendor
    # fields='__all__' #限制create介面
    template_name = 'vendors/vendor_create.html' #要導向的文檔

def render(request, template_name, context=None, content_type=None, status=None, using=None):
    """
    Return a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)
