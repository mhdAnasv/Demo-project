from django.shortcuts import render,redirect
from shop.models import Category, Products
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def allcategories(request):
    c = Category.objects.all()
    return render(request, 'category.html', {'c': c})


def allproducts(request, p):
    c = Category.objects.get(name=p)
    p = Products.objects.filter(category=c)
    return render(request, 'products.html', {'c': c, 'p': p})


def detail(request, p):
    p = Products.objects.get(name=p)
    return render(request, 'detail.html',{'p':p})

def user_login(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('shop:allcat')
        else:
            return HttpResponse("Invalid Credentials")
    return render(request, "login.html")

# @login_required
def user_logout(request):
    logout(request)
    return redirect('shop:login')


def register(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST["p"]
        cp = request.POST["cp"]
        fname = request.POST["f"]

        lname = request.POST["l"]
        e = request.POST["e"]


        if (p == cp):
            u = User.objects.create_user(username=u, password=p, first_name=fname, last_name=lname, email=e)
            u.save()
            return redirect("shop:allcat")
        else:
            return HttpResponse("password are not same")
    return render(request, "register.html")



