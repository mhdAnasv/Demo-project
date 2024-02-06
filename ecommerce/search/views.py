# from django.shortcuts import render
# from shop.models import Product
# from django.db.models import Q
#
# def search(request):
#     query = ""
#     b = None
#     if request.method == "POST":
#         query = request.POST.get('q', '')
#         if query:
#             b = Product.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
#     return render(request, "search.html", {'query': query, 'b': b})