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
        'looks like something went wrong on out end. please check after sometime or contact admin ',
        'something went wrong',
    ])
 
def toId(id,default=-1):
    try:
        return int(id)
    except:
        return -1