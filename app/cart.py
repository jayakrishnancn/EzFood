def addItemToCart(items,newItem, count = 1):
    count = int(count)
    if(count <= 0 ):
        return items
    if count > 0 :
        try:
            itemFoundInCart = False
            for item in items:
                try:
                    if item["id"] == newItem["id"]:
                        itemFoundInCart = True
                        if not item['quantity']:
                            item['quantity'] = 0
                        item['quantity'] = count
                except:
                    pass
            if not itemFoundInCart:
                newItem['quantity'] = count
                items.append(newItem)
        except:
            pass
    print(items)
    return items
