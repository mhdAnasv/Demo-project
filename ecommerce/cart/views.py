from django.shortcuts import render
from shop.models import Products
from cart.models import Cart, account, placeorder
from django.contrib.auth.decorators import login_required
# @login_required
def cartview(request):
    u = request.user
    cart = Cart.objects.filter(user=u)
    total = 0
    for i in cart:
        total += i.quantity * i.product.price

    return render(request, 'cartview.html', {'c': cart, 'total': total})

# @login_required
def addtocart(request, n):
    p = Products.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity < cart.product.stock):
            cart.quantity += 1
            cart.save()

    except:
        if (p.stock > 0):
            cart = Cart.objects.create(product=p, user=u, quantity=1)
            cart.save()
    return cartview(request)

# @login_required
def cartremove(request, n):
    p = Products.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()
    except:
        pass
    return cartview(request)

# @login_required
def carttrash(request, n):
    p = Products.objects.get(name=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
    except:
        pass
    return cartview(request)

# @login_required
def orderview(request):
    u = request.user
    o = placeorder.objects.filter(user=u)

    return render(request, 'orderview.html', {'o': o, 'u': u.username})

# @login_required
def orderform(request):
    if request.method == "POST":  # data from orderform
        a = request.POST['a']
        p = request.POST['p']
        n = request.POST['n']  # convert into num (after try)

        u = request.user  # login user
        cart = Cart.objects.filter(user=u)  # user cart items

        total = 0
        for i in cart:
            total += i.quantity * i.product.price  # user total amount

        try:  # check account balance
            num = int(n)
            ac = account.objects.get(acc_num=num)  # verifying account number

            if ac.amount >= total:  # checking balance for payment
                ac.amount = ac.amount - total
                ac.save()
                for i in cart:
                    o = placeorder.objects.create(
                        user=u,
                        product=i.product,
                        address=a,
                        phone=p,
                        no_of_items=i.quantity,
                        order_status="paid"
                    )  # adding details from cart to placeorder table
                    o.save()

                cart.delete()
                msg = "Your order has been placed successfully."
                return render(request, 'orderdetails.html', {'msg': msg})
            else:
                msg = "Insufficient balance. Cannot place your order."
                return render(request, 'orderdetails.html', {'msg': msg})

        except account.DoesNotExist:
            msg = "Invalid account number."
            return render(request, 'orderdetails.html', {'msg': msg})

        except ValueError:
            msg = "Invalid account number. Please enter a valid number."
            return render(request, 'orderdetails.html', {'msg': msg})

    return render(request, 'orderform.html')
