from django import template

register = template.Library()

@register.filter
def calculatePrice(items,output='total'):
    priceDetails = {}
     
    total_price = 0

    for item in items:
        if not item['quantity']:
            item['quantity'] = 1
        total_price = total_price + item['price'] * item['quantity'] 
    
    total_delevery = total_price*0.08

    grad_total = total_price + total_delevery

    priceDetails['payable'] = round(grad_total,2)
    priceDetails['total_delevery'] = round(total_delevery,2)
    priceDetails['total'] = round(total_price,2)

    return priceDetails[output]

@register.filter
def calculateTotalQuantity(items):
    total = 0
    for item in items:
        if not item['quantity']:
            item['quantity'] = 1
        total = total + item['quantity']

    return total