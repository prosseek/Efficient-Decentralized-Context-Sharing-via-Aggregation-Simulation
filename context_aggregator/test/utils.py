__author__ = 'smcho'

def avg(set_of_single_contexts):
    sum = 0.0
    for i in set_of_single_contexts:
        sum += i.value
    return sum/len(set_of_single_contexts)

if __name__ == "__main__":
    import doctest
    doctest.testmod()