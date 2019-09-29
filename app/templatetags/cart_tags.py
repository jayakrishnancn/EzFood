from django import template

register = template.Library()

@register.filter
def calculatePrice(items,output='total'):
    priceDetails = {}
     
    total_price = 0
    for item in items:
        total_price = total_price + item['price'] 
    
    total_delevery = total_price*0.08
    grad_total = total_price + total_delevery

    priceDetails['payable'] = grad_total
    priceDetails['total_delevery'] = total_delevery
    priceDetails['total'] = total_price

    return priceDetails[output]