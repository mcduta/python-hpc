
""" A function to calculate the median of a list"""

def my_median(years):
    ages = []
    for y in years:
        ages.append(y - 1900)

    ages.sort()
    mid = len(ages)/2

    return ages[mid-1:mid+2]

years = [1989, 1955, 2011, 1943, 1975]
print my_median(years)
