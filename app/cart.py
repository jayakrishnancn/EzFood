def addItemToCart(items,newItem):
    try:
        itemFoundInCart = False
        for item in items:
            try:
                if item["id"] == newItem["id"]:
                    itemFoundInCart = True
                    if not item['quantity']:
                        item['quantity'] = 0
                    item['quantity'] = item['quantity'] + 1
            except:
                pass
        if not itemFoundInCart:
            newItem['quantity'] = 1
            items.append(newItem)
    except:
        pass
    print(items)
    return items
