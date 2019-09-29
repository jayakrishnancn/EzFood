def addItemToCart(items,newItem):
    try:
        itemFoundInCart = False
        for item in items:
            try:
                if item["id"] == newItem["id"]:
                    itemFoundInCart = True
                    item['quantity'] = item['quantity'] + newItem['quantity']
            except:
                pass
        if not itemFoundInCart:
            items.append(newItem)
    except:
        pass

    return items
