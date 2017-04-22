from django.shortcuts import render
from amazon.api import AmazonAPI
from SecretConfigs import *
from .cartsql import *

amazon = AmazonAPI(SecretConfigs.awsAccessKey(), SecretConfigs.awsSecretKey(), SecretConfigs.awsAssociateTag())


def index(request):
    purchaseURL = 'https://www.amazon.com/gp/cart/aws-merge.html?cart-id=' + str(request.session['cartID']) + '%26associate-id=' + str(SecretConfigs.awsAssociateTag()) + '%26hmac=' + str(request.session['carthmac']) + '%26AWSAccessKeyId=' + str(SecretConfigs.awsAccessKey())
    return render(request, 'cart.html', {'purchase_url': purchaseURL})


def addtocart(request):
    offerID = request.POST.get('offerID')
    ASIN = request.POST.get('ASIN')
    print("INCOMING OFFER ID:", offerID)
    print("INCOMING ASIN:", ASIN)
    item = {'offer_id': offerID, 'quantity': 1}
    if searchDBForCartID(request.session['user']['user_amazon_id']) is None:
        cart = amazon.cart_create(item)
        request.session['cartID'] = cart.cart_id
        request.session['carthmac'] = cart.hmac
        addCartID(cart.cart_id, request.session['user']['user_amazon_id'])
        print(str(request.session['cartID']) + "cart" + str(request.session['carthmac']))
    else:
        print("Success")
        cart = amazon.cart_get(searchDBForCartID(request.session['user']['user_amazon_id']), request.session['carthmac'])
        if item not in cart:
            amazon.cart_add(item, request.session['cartID'], request.session['carthmac'])
        print(str(request.session['cartID']) + "cart" + str(request.session['carthmac']))
    request.session.modified = True
