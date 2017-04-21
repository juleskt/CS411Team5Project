from django.shortcuts import render
from amazon.api import AmazonAPI
from SecretConfigs import *

amazon = AmazonAPI(SecretConfigs.awsAccessKey(), SecretConfigs.awsSecretKey(), SecretConfigs.awsAssociateTag())


def index(request):
    purchaseURL = 'https://www.amazon.com/gp/cart/aws-merge.html?cart-id=' + str(request.session['cartID']) + '%26associate-id=' + str(SecretConfigs.awsAssociateTag()) + '%26hmac=' + str(request.session['carthmac']) + '%26AWSAccessKeyId=' + str(SecretConfigs.awsAccessKey())
    return render(request, 'cart.html', {'purchase_url': purchaseURL})


def addtocart(request):
    print("INSIDE ADD TO CART")
    offerID = request.POST.GET('offerID')
    print("INSIDE ADD TO CART")
    print("INCOMING OFFER ID:", offerID)
    item = {'offer_id': offerID, 'quantity': 1}
    if 'cartID' not in request.session or 'carthmac' not in request.session:
        cart = amazon.cart_create(item)
        request.session['cartID'] = cart.cart_id
        request.session['carthmac'] = cart.hmac
        print(str(request.session['cartID']) + "cart" + str(request.session['carthmac']))
    else:
        cart = amazon.cart_get(request.session['cartID'], request.session['carthmac'])
        if item not in cart:
            amazon.cart_add(newitem, request.session['cartID'], request.session['carthmac'])
        print(str(request.session['cartID']) + "cart" + str(request.session['carthmac']))

