from collections import namedtuple
from .models import BalanceChange, Category, Method
import datetime

def importBalanceChangeCsv(reader, request):
    reader.__next__()
    header = ['Date', 'Vendor', 'Reason', 'Method', 'Category', 'Amount']
    line = 1
    num_imported = 0
    num_failed = 0
    results = {
        'errors': [],
        'resultMessages': []
    }
    for row in reader:
        row = {header[i]: row[i] for i in range(len(row))}
        if len(row) != 6:
            results['errors'].append(f"Error creating balance change on line {line}. This balance change was not created")
            num_failed += 1
        else:
            try:
                balanceChange = BalanceChange(
                    date=datetime.datetime.strptime(row['date'], "%m/%Y/%d"),
                    reason=row['reason'],
                    vendor=row['vendor'],
                    method=lookupMethod(row['method']),
                    category=lookupCategory(row['category']),
                    amount=float(row['amount']),
                    user=request.user
                )
                balanceChange.save()
                num_imported += 1
            except:
                results['errors'].append(f"Error creating student on line {line}. This student was not created")
                num_failed += 1
            line += 1
    if num_imported > 0:
        results['resultMessages'].append(f"{num_imported} students successfully imported")
    if num_failed > 0:
        results['resultMessages'].append(f"{num_failed} students failed to import")
    return results

def lookupMethod(methodStr):
    existingMethod = Method.objects.get(name=methodStr)
    if existingMethod is None:
        method = Method(methodStr)
        method.save()
        return method
    else:
        return existingMethod


def lookupCategory(categoryStr):
    existingCategory = Category.objects.get(name=categoryStr)
    if existingCategory is None:
        category = Method(categoryStr)
        category.save()
        return category
    else:
        return existingCategory