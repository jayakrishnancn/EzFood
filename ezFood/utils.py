import random 
def processData(request=None,data=None):
    img = {
        'logo' : 'logo.svg'
    }  
     
    cartItemsFromSession = request.session.get('items', {})
    appData = {'companyName':'Ez Food','errorQuote':randomErrorQuotes(),'img':img,'cartItems':cartItemsFromSession }

    if(data is None):
        data = {}    
    appData.update(data)

    return appData 

def randomErrorQuotes():
    return random.choice([
        'We are doing a car.',
        'Car engine out completely.'
    ])
 