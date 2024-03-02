import random


class BillSpliter:
    def __init__(self):
        self.bill_dict = {}
        number_of_people = int(input("Enter the number of friends joining (including you):\n"))

        if number_of_people <= 0:
            print("No one is joining for the party")
            return

        print("Enter the name of every friend (including you), each on a new line:")
        for _ in range(number_of_people):
            name = input()
            self.bill_dict[name] = 0.0

    def is_successfully_created(self):
        if not self.bill_dict:
            return False
        else:
            return True

    def print_dict(self):
        if not self.is_successfully_created():
            return

        print(self.bill_dict)

    def bill_arrived(self):
        if not self.is_successfully_created():
            return

        print("Enter the total bill value:")
        bill_value = float(input())

        is_true, lucky_name = self.lucky_person()
        if is_true:
            for name in self.bill_dict.keys():
                self.bill_dict[name] = round(bill_value / (len(self.bill_dict) - 1), 2)
            self.bill_dict[lucky_name] = 0.0
        else:
            for name in self.bill_dict.keys():
                self.bill_dict[name] = round(bill_value / len(self.bill_dict), 2)

    def lucky_person(self):
        print("Do you want to use the \"Who is lucky?\" feature? Write Yes/No:")
        answer = input().lower()

        if answer == "yes":
            random_name = random.choice(list(self.bill_dict.keys()))
            print(random_name + " is the lucky one!")
            return True, random_name
        else:
            print('No one is going to be lucky')
            return False, None


new_bill = BillSpliter()
new_bill.bill_arrived()
new_bill.print_dict()
