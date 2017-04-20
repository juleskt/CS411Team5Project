from django.shortcuts import render
from amazon.api import AmazonAPI
from SecretConfigs import *

amazon = AmazonAPI(SecretConfigs.awsAccessKey(), SecretConfigs.awsSecretKey(), SecretConfigs.awsAssociateTag())

def index(request):
#    ingredientID = request.session['product_asin']
    product = amazon.lookup(ItemId="0316067938")
    item = {'offer_id': product.offer_id, 'quantity': 1}
    if 'cartID' not in request.session or 'carthmac' not in request.session:
        cart = amazon.cart_create(item)
        request.session['cartID'] = cart.cart_id
        request.session['carthmac'] = cart.hmac
        print(str(request.session['cartID']) + "cart" + str(request.session['carthmac']))
    else:
        print(str(request.session['carthmac']))
        print(request.session['cartID'])
    purchaseURL = 'https://www.amazon.com/gp/cart/aws-merge.html?cart-id=' + str(request.session['cartID']) + '%26associate-id=' + str(SecretConfigs.awsAssociateTag()) + '%26hmac=' + str(request.session['carthmac']) + '%26AWSAccessKeyId=' + str(SecretConfigs.awsAccessKey())
    return render(request, 'cart.html', {'purchase_url': purchaseURL})