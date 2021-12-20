from collections import namedtuple
from .models import Transaction, Category, Method
import datetime

def importTransactionsCsv(reader, request):
    reader.__next__()
    header = ['date', 'vendor', 'reason', 'method', 'category', 'amount']
    line = 1
    num_imported = 0
    num_failed = 0
    results = {
        'errors': [],
        'numSuccess': '',
        'numFail': '',
        'showErrorButton': False
    }
    for row in reader:
        row = {header[i]: row[i] for i in range(len(row))}
        if len(row) != 6:
            results['errors'].append(f"Error creating transaction on line {line}: Incorrect number of columns")
            num_failed += 1
        else:
            try:
                transaction = Transaction(
                    date=datetime.datetime.strptime(row['date'].strip(), "%m/%d/%Y"),
                    reason=row['reason'].strip(),
                    vendor=row['vendor'].strip(),
                    method=lookupMethod(row['method'].strip()),
                    category=lookupCategory(row['category'].strip()),
                    amount=float(row['amount'].strip()),
                    user=request.user
                )
                transaction.save()
                num_imported += 1
            except:
                results['errors'].append(f"Error on line {line}. This transaction was not created")
                num_failed += 1
            line += 1

    if num_imported > 0:
        results['numSuccess'] = f"{num_imported} transactions successfully imported"
    if num_failed > 0:
        results['numFail'] = f"{num_failed} transactions failed to import"
        results['showErrorButton'] = True
    return results

def lookupMethod(methodStr):
    try:
        existingMethod = Method.objects.get(name=methodStr)
    except:
        firstLetter = methodStr[0].upper()
        methodStr = methodStr[1:]
        methodStr = firstLetter + methodStr
        method = Method(name=methodStr)
        method.save()
        return method
    return existingMethod


def lookupCategory(categoryStr):
    try:
        existingCategory = Category.objects.get(name=categoryStr)
    except:
        firstLetter = categoryStr[0].upper()
        categoryStr = categoryStr[1:]
        categoryStr = firstLetter + categoryStr
        category = Category(name=categoryStr)
        category.save()
        return category
    return existingCategory