from amazon.api import AmazonAPI
from SecretConfigs import *

amazon = AmazonAPI(SecretConfigs.awsAccessKey(), SecretConfigs.awsSecretKey(), SecretConfigs.awsAssociateTag())
products = amazon.search(Keywords='Orange Zest', SearchIndex='All')

for i, product in enumerate(products):
   print (i, product.title)
