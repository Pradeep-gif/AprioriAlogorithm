from itertools import chain, combinations
from csv import reader


def apriori_algorithm(transaction_list, min_sup):
    """
    Find frequent itemsets using an iterative level-wise approach based
    on candidate generation

    :param :
    *d: a database of transactions
    *min_sup: the minimum support count threshold

    :return:
    final_rules: frequent itemsets in transaction_list.
    """
    # frequent_list: Set of frequent itemset satisfies the min_sup
    frequent_list = set()
    supported_rules = []

    # Create the first candidate list of single set element
    itemset = set()
    for transaction in transaction_list:
        for item in transaction:
            itemset.add(frozenset([item]))
    candidate_list = list(itemset)

    # Check all candidates' support count and create candidate list
    for item in candidate_list:
        if is_frequent(item, transaction_list, min_sup):
            if item not in frequent_list:
                frequent_list.add(item)
    frequent_list = list(frequent_list)

    while frequent_list:
        supported_rules = frequent_list
        candidate_list = apriori_generate(
            frequent_list,
            transaction_list,
            min_sup
        )
        frequent_list = []
        for itemset in candidate_list:
            if is_frequent(itemset, transaction_list, min_sup):
                if itemset not in frequent_list:
                    frequent_list.append(itemset)

    return supported_rules


def is_frequent(_subset, _list, min_sup):
    if sum([int(_subset.issubset(_set)) for _set in _list]) >= min_sup:
        return True
    else:
        return False


def apriori_generate(itemset_list, transaction_list, min_sup):
    """
    Generate the next frequent candidate_list.
    :param itemset_list: list of itemset to use for the next iteration.
    :return:
    """
    new_candidate_list = []
    _l = join(itemset_list)
    for item in _l:
        if has_frequent_subsets(item, transaction_list, min_sup):
            if item not in new_candidate_list:
                new_candidate_list.append(item)
    return new_candidate_list


def join(lst):
    """
    Return all possible candidates after joining the list with itself
    :param lst: list of sets
    :return: candidate
    """
    candidate = []
    length = len(lst)
    for i in range(length-1):
        for row in range(i+1, length):
            candidate.append(lst[i].union(lst[row]))
    return candidate


def has_frequent_subsets(c, prev_candidates, min_sup):
    """
    Checks if this itemset has an infrequent subset.
    True if all elements are a success or False if one element is infrequent.

    :param c: an itemset to be checked for infrequent members
    :param prev_candidates: candidate_list from the previous step.
    :return: bool
    """
    # Get all subsets of this itemset
    subsets = get_subsets(c)
    # Go through all subsets and check support
    for item in subsets:
        item = set(item)
        if not is_frequent(item, prev_candidates, min_sup):
            return False

    return True


def get_subsets(powerset):
    return list(
        chain.from_iterable(
            combinations(powerset, r)
            for r in range(1, len(powerset))
        )
    )


def get_rules(transaction_data: list, min_sup: int) -> list:
    """
    A function that applies the algorithm and return the final rules.

    :param transaction_data: list of transactions to work on.
    :param min_sup: the minimum acceptable support.
    :return: list of supported rules
    """
    # Apply the algorithm
    supported_rules = apriori_algorithm(transaction_data, min_sup)

    # make final calculations over all the rules
    associated_rules = []
    for rule in supported_rules:
        sub_rules = get_subsets(rule)
        for s in sub_rules:
            s = set(s)
            if s not in associated_rules:
                associated_rules.append(s)
    associated_rules.sort(key=len)
    associated_rules.extend([set(i) for i in supported_rules])

    return associated_rules


def get_transaction_data(fpath: str) -> list:
    """
    A function that opens a csv file and extract all transactions
    from it.

    :param fpath: path of the csv file
    :return: list of transactions
    """
    transaction_data = []
    with open(fpath, 'r') as file:
        csv_reader = reader(file, skipinitialspace=True)
        for row in csv_reader:
            record = set(row[1:])
            transaction_data.append(record)
    return transaction_data
