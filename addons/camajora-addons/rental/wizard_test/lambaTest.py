from random import randrange

costIsBetween = (lambda r: (r.getCreditCost() > minPrice) and (r.getCreditCost() <= maxPrice))


class Resource:
    credit_cost = 2

    def __init__(self, cost):
        self.credit_cost = cost

    def getCreditCost(self):
        return self.credit_cost

    def setCreditCost(self, cost):
        self.credit_cost = cost

    def __str__(self):
        return f'Cost is {self.credit_cost}'


def checkPriceInput(price):
    priceInt = None
    if not price:
        return None
    else:
        priceInt = int(price) if price.isdigit() else None
    print('Resolved int ' + str(priceInt))
    return priceInt


def filterResource(resources_ids, minPrice, maxPrice):
    if not minPrice and not maxPrice:
        return resources_ids
    elif minPrice and maxPrice:
        return list(filter(lambda r: (r.credit_cost > minPrice) and (r.credit_cost <= maxPrice),
                           resources_ids))
    elif not minPrice and maxPrice:
        return list(filter(lambda r: (r.credit_cost <= maxPrice),
                           resources_ids))
    elif minPrice and not maxPrice:
        return list(filter(lambda r: (r.credit_cost >= minPrice),
                           resources_ids))


if __name__ == '__main__':
    minPrice = '12'
    maxPrice = '15'

    resources = []
    for i in range(10):
        resources.append(Resource(randrange(100)))
    for r in resources:
        print(r)
    print('Now print filtered list')
    filtered = filterResource(resources, checkPriceInput(minPrice),
                              checkPriceInput(maxPrice))
    for f in filtered:
        print(f)
        ##print((f.getCreditCost() > minPrice) and (f.getCreditCost() <= maxPrice))
