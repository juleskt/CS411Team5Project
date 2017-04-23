from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from amazon.api import AmazonAPI
from SecretConfigs import *
#from cartsql import *
from django.core.urlresolvers import reverse

amazon = AmazonAPI(SecretConfigs.awsAccessKey(), SecretConfigs.awsSecretKey(), SecretConfigs.awsAssociateTag())


def index(request):
    if request.session.get('cartID') is not None or request.session.get('cartHMAC') is not None:
        purchaseURL = 'https://www.amazon.com/gp/cart/aws-merge.html?cart-id=' + str(request.session['cartID']) + '%26associate-id=' + str(SecretConfigs.awsAssociateTag()) + '%26hmac=' + str(request.session['cartHMAC']) + '%26AWSAccessKeyId=' + str(SecretConfigs.awsAccessKey())
        cart = amazon.cart_get(request.session['cartID'], request.session['cartHMAC'])
        cart_item_id = None
        for item in cart:
            cart_item_id = item.cart_item_id
        cartitems = []
        for item in cart:
            ingredient = amazon.lookup(ItemId=item.asin)
            dict = {
                "product_title":        ingredient.title,
                "product_medium_image": ingredient.large_image_url,
                "product_price":        ingredient.formatted_price,
                "product_brand":        ingredient.brand,
                "cart_item_id":         item.cart_item_id,
            }
            cartitems.append(dict)
        return render(request, 'cart.html', {'purchase_url': purchaseURL, 'cartproducts': cartitems})


def addtocart(request):
    if request.method == 'POST':
        offerID = request.POST.get('offerID')
        ASIN = request.POST.get('ASIN')
        print("INCOMING OFFER ID:", offerID)
        print("INCOMING ASIN:", ASIN)
        item = {'offer_id': offerID, 'ASIN': ASIN, 'quantity': 1}

        if request.session.get('cartID') is None or request.session.get('cartHMAC') is None:
            cart = amazon.cart_create(item)

            request.session['cartID'] = cart.cart_id
            request.session['cartHMAC'] = cart.hmac
            print(str(request.session['cartID']), "cart", str(request.session['cartHMAC']))
            print("MAKING CART")
        else:
            cart = amazon.cart_get(request.session['cartID'], request.session['cartHMAC'])
            if item not in cart:
                amazon.cart_add(item, request.session['cartID'], request.session['cartHMAC'])
            print(str(request.session['cartID']), "cart", str(request.session['cartHMAC']))
            print("ADDING TO CART")

        print("CART:", request.session['cartID'])
        print("CART:", request.session['cartHMAC'])
        return HttpResponse()
    else:
        return Http404()

    # offerID = request.POST.get('offerID')
    # ASIN = request.POST.get('ASIN')
    # print("INCOMING OFFER ID:", offerID)
    # print("INCOMING ASIN:", ASIN)
    # item = {'offer_id': offerID, 'quantity': 1}
    # if searchDBForCartID(request.session['user']['user_amazon_id']) is None:
    #     cart = amazon.cart_create(item)
    #     request.session['cartID'] = cart.cart_id
    #     request.session['cartHMAC'] = cart.hmac
    #     addCartID(cart.cart_id, request.session['user']['user_amazon_id'])
    #     print(str(request.session['cartID']) + "cart" + str(request.session['cartHMAC']))
    # else:
    #     print("Success")
    #     cart = amazon.cart_get(searchDBForCartID(request.session['user']['user_amazon_id']), request.session['cartHMAC'])
    #     if item not in cart:
    #         amazon.cart_add(item, request.session['cartID'], request.session['cartHMAC'])
    #     print(str(request.session['cartID']) + "cart" + str(request.session['cartHMAC']))
    # request.session.modified = True

def removefromcart(request):
    if request.method == 'POST':
        print("got to remove from cart")
        cart = amazon.cart_get(request.session['cartID'], request.session['cartHMAC'])
        cart_item_id = request.POST.get('cart_item_id')
        item = {'cart_item_id': cart_item_id, 'quantity': 0}
        cart = amazon.cart_modify(item, cart.cart_id, cart.hmac)
        url = reverse('cart')
        return HttpResponseRedirect(url)
    else:
        return Http404()


def clearcart(request):
    return amazon.cart_clear(request.session['cartID'], request.session['carthmac'])

