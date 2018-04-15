import pandas as pd
from difflib import SequenceMatcher

NAMES_CSV = "names.csv"
LAST_NAMES_CSV = "lastnames.csv"
NICKNAMES_CSV = "nicknames.csv"

STRICTNESS = 0.75


def is_name(name):
    return (name + "\n") in open(NAMES_CSV).read();


def is_last_name(name):
    return (name + "\n") in open(LAST_NAMES_CSV).read();


def is_nickname(name1, name2):
    nicknames_file = pd.read_csv(open(NICKNAMES_CSV), skipinitialspace=True)
    nicknames = list(nicknames_file["nickname"])
    names = list(nicknames_file["name"])


    if name1 in nicknames:
        names_indecies = [i for i, name in enumerate(names) if name == name2]
        nickname_indecies = [i for i, name in enumerate(nicknames) if name == name1]
        return len([i for i in names_indecies if i in nickname_indecies])

    elif name2 in nicknames:
        names_indecies = [i for i, name in enumerate(names) if name == name1]
        nickname_indecies = [i for i, name in enumerate(nicknames) if name == name2]
        return len([i for i in names_indecies if i in nickname_indecies])
    else:
        return False;



def is_typo(string1, string2):
    similarity = SequenceMatcher(None, string1, string2)
    return similarity.ratio() >= STRICTNESS


def count_first_names(names):
    same_names = []

    if len(names) > 1:
        if not is_unique_first_name(names[0], names[1]):
            same_names.append(names[0] + "1")
            same_names.append(names[1] + "2")
    if len(names) > 2:
        if not is_unique_first_name(names[1], names[2]):
            same_names.append(names[1] + "2")
            same_names.append(names[2] + "3")
        if not is_unique_first_name(names[0], names[2]):
            same_names.append(names[0] + "1")
            same_names.append(names[2] + "3")

    if len(same_names) == 0:
        same_names.append("")

    return 4 - len(set(same_names))



def count_last_names(name1, name2, name3):
    same_names = []
    if not is_unique_last_name(name1, name2):
        same_names.append(name1 + "1")
        same_names.append(name2 + "2")
    if not is_unique_last_name(name2, name3):
        same_names.append(name2 + "2")
        same_names.append(name3 + "3")
    if not is_unique_last_name(name1, name3):
        same_names.append(name1 + "1")
        same_names.append(name3 + "3")
    if len(same_names) == 0:
        same_names.append("")
    same_names = set(same_names)
    return same_names, 4 - len(same_names)


def is_unique_first_name(name1, name2):
    unique = False
    if name1 != name2:
        name1 = name1.split()
        name2 = name2.split()
        if len(name1) == len(name2) == 2:
            unique = not (name1[1] == name2[1]) and \
                      (not is_nickname(name1[0], name2[0]) and (is_name(name2[0]) or not is_typo(name1[0], name2[0])))
            unique = not unique
        elif not is_nickname(name1[0], name2[0]) and (is_name(name2[0]) or not is_typo(name1[0], name2[0])):
            unique = True;
    return unique


def is_unique_last_name(name1, name2):
    unique = False
    if name1 != name2:
        if is_last_name(name2) or not is_typo(name1, name2):
            unique = True
    return unique


def count_unique_names(bill_first_name, bill_last_name, ship_first_name, ship_last_name, bill_name_on_card):
    num_of_different_names = 1

    if len(bill_name_on_card.split()) == 3:
        bill_name_on_card_first_name = bill_name_on_card.split()[0] + " " + bill_name_on_card.split()[1]
        bill_name_on_card_last_name = bill_name_on_card.split()[2]
    else:
        bill_name_on_card_first_name = bill_name_on_card.split()[0]
        bill_name_on_card_last_name = bill_name_on_card.split()[1]


    same_last_names, num_of_different_names = count_last_names(bill_last_name, ship_last_name, bill_name_on_card_last_name)

    first_names_to_check = []
    if bill_last_name + "1" in same_last_names:
        first_names_to_check.append(bill_first_name)
    if ship_last_name + "2" in same_last_names:
        first_names_to_check.append(ship_first_name)
    if bill_name_on_card_last_name + "3" in same_last_names:
        first_names_to_check.append(bill_name_on_card_first_name)

    num_of_different_names += count_first_names(first_names_to_check) - 1


    return num_of_different_names


print count_unique_names("Deborah S", "Eglia", "Deborah A", "Egdi", "Deborah A Egli")

print count_unique_names("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli")

print count_unique_names("Deborah", "Egli", "Debbie", "Egli", "Deborah Egli")

print count_unique_names("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli")

print count_unique_names("Michele", "Egli", "Deborah","Egli", "Michele Egli")

print count_unique_names("Michele A", "Egli", "Deborah", "Egli", "Michele C Egli")

print count_unique_names("Michele A", "Egli", "Debby A", "Egli", "Michele Egli")

print count_unique_names("Deborah A", "Egli", "Debby A", "Egli", "Debbie Egli")



