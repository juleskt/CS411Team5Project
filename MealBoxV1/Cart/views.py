from django.shortcuts import render
from amazon.api import AmazonAPI
from SecretConfigs import *

amazon = AmazonAPI(SecretConfigs.awsAccessKey(), SecretConfigs.awsSecretKey(), SecretConfigs.awsAssociateTag())


def index(request):
    if request.session.get('cartID') is not None or request.session.get('carhmac') is not None:
        purchaseURL = 'https://www.amazon.com/gp/cart/aws-merge.html?cart-id=' + str(request.session['cartID']) + '%26associate-id=' + str(SecretConfigs.awsAssociateTag()) + '%26hmac=' + str(request.session['carthmac']) + '%26AWSAccessKeyId=' + str(SecretConfigs.awsAccessKey())
        return render(request, 'cart.html', {'purchase_url': purchaseURL})


def addtocart(request):
    offerID = request.POST.get('offerID')
    ASIN = request.POST.get('ASIN')
    print("INCOMING OFFER ID:", offerID)
    print("INCOMING ASIN:", ASIN)
    item = {'offer_id': offerID, 'quantity': 1}

    if request.session.get('cartID') is None and request.session.get('carhmac') is None:
        cart = amazon.cart_create(item)

        request.session['cartID'] = cart.cart_id
        request.session['carthmac'] = cart.hmac
        print(str(request.session['cartID']), "cart", str(request.session['carthmac']))
        print("MAKING CART")
    else:
        cart = amazon.cart_get(request.session['cartID'], request.session['carthmac'])
        if item not in cart:
            amazon.cart_add(item, request.session['cartID'], request.session['carthmac'])
        print(str(request.session['cartID']), "cart", str(request.session['carthmac']))
        print("ADDING TO CART")
