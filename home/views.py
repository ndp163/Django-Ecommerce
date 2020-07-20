from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from home.models import Setting, ContactForm, ContactMessage
from django.contrib import messages
from product.models import Category, Product
# Create your views here.


class Index(View):
    def get(self, request):
        setting = Setting.objects.get(pk=1)
        category = Category.objects.all()
        page = 'home'
        context = {'setting':setting, 'page':page, 'category':category}
        return render(request, 'index.htm', context)


class AboutUs(View):
    def get(self, request):
        setting = Setting.objects.get(pk=1)
        context = {'setting':setting}
        return render(request, 'about.htm', context)


class ContactUs(View):
    def get(self, request):
        setting = Setting.objects.get(pk=1)
        form = ContactForm
        context = {'setting':setting, 'form':form}
        return render(request, 'contact.htm', context)
    
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name'] # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Your message has been sent. Thank you for your message!")
            return HttpResponseRedirect('/contact')
        return HttpResponse("Wrong!")


class ProductCategory(View):
    def get(self, request, id, slug):
        setting = Setting.objects.get(pk=1)
        products = Product.objects.filter(category_id=id)
        return HttpResponse(products)