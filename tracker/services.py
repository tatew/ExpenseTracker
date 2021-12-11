from collections import namedtuple
from .models import BalanceChange, Category, Method
import datetime

def importBalanceChangeCsv(reader, request):
    reader.__next__()
    header = ['date', 'vendor', 'reason', 'method', 'category', 'amount']
    line = 1
    num_imported = 0
    num_failed = 0
    results = {
        'errors': [],
        'numSuccess': '',
        'numFail': ''
    }
    for row in reader:
        row = {header[i]: row[i] for i in range(len(row))}
        if len(row) != 6:
            results['errors'].append(f"Error creating balance change on line {line}: Incorrect number of columns")
            num_failed += 1
        else:
            try:
                balanceChange = BalanceChange(
                    date=datetime.datetime.strptime(row['date'].strip(), "%m/%d/%Y"),
                    reason=row['reason'].strip(),
                    vendor=row['vendor'].strip(),
                    method=lookupMethod(row['method'].strip()),
                    category=lookupCategory(row['category'].strip()),
                    amount=float(row['amount'].strip()),
                    user=request.user
                )
                balanceChange.save()
                num_imported += 1
            except:
                results['errors'].append(f"Error creating balance change on line {line}. This balance change was not created")
                num_failed += 1
            line += 1


            # balanceChange = BalanceChange(
            #     date=datetime.datetime.strptime(row['date'].strip(), "%m/%d/%Y"),
            #     reason=row['reason'].strip(),
            #     vendor=row['vendor'].strip(),
            #     method=lookupMethod(row['method'].strip()),
            #     category=lookupCategory(row['category'].strip()),
            #     amount=float(row['amount'].strip()),
            #     user=request.user
            # )
            # balanceChange.save()
            # num_imported += 1
            # line += 1


    if num_imported > 0:
        results['numSuccess'] = f"{num_imported} balance changes successfully imported"
    if num_failed > 0:
        results['numFail'] = f"{num_failed} balance changes failed to import"
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