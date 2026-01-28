from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from datetime import datetime
from hii.models import Contact,Product
from django.contrib import messages

# Create your views here.
def index(request):
    products = Product.objects.all()

    return render(request, 'index.html',{"products":products})

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html',{"products":products})

    # return HttpResponse("new arrival")

def about(request):
    return render(request, 'about.html')

    # return HttpResponse("this is about")

def contact(request):
    if request.method == "POST":
        first = request.POST.get('first')
        last = request.POST.get('last')
        service = request.POST.get('service')
        email = request.POST.get('email')
        commnt = request.POST.get('commnt')
        contact = Contact(first=first,last=last,service=service,email=email,commnt=commnt,date=datetime.today())
        contact.save()
        messages.success(request, "Your Account has been Created!.")
        return redirect('contact')
    return render(request, 'contact.html')

def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, "product.html", {"product": product})
