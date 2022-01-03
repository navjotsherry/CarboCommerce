import json
from .models import *

def cookieCart(request):
    try:
        cart=json.loads(request.COOKIES['cart'])
    except:
        cart={}
    items= []
    order={'get_cart_total':0, 'cart_list':0,'shipping':False}
    cartItems = order['cart_list']
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = product.price * cart[i]["quantity"]
            order['get_cart_total'] += total
            order['cart_list'] += cart[i]["quantity"]
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)
            
            if product.digital == False:
                order['shipping']=True
        except:
            pass
    return {'cartItems':cartItems,'order':order,'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items= order.orderitem_set.all()
        cartItems = order.cart_list
        
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems,'order':order,'items':items}