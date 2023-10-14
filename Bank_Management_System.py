class Account:
    account_number = 1000

    def __init__(self, name, email, address, account_type):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.transactions = []
        self.total_loan_amount = 0
        Account.account_number += 1
        self.account_number = Account.account_number

    def deposit(self, amount):
        self.balance += amount
        bank.total_balance_in_bank += amount
        self.transactions.append(f"Deposited: {amount}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded")
            return
        if bank.total_balance_in_bank < amount:
            print("Bank is bankrupt. Cannot process your request.")
            return
        self.balance -= amount
        bank.total_balance_in_bank -= amount
        self.transactions.append(f"Withdrew: {amount}")

    def check_balance(self):
        return self.balance

    def check_transactions(self):
        return self.transactions

    def take_loan(self, amount):
        if self.total_loan_amount >= 2 * amount:
            print("Loan limit reached!")
            return
        if bank.loan_feature is False:
            print("Loan feature is currently off.")
            return
        if bank.total_balance_in_bank < amount:
            print("Bank is bankrupt. Cannot provide the loan.")
            return
        self.balance += amount
        self.total_loan_amount += amount
        bank.total_loans_given += amount
        bank.total_balance_in_bank -= amount
        self.transactions.append(f"Loan Taken: {amount}")

    def transfer(self, amount, to_account):
        if amount > self.balance:
            print("Insufficient balance!")
            return
        if bank.total_balance_in_bank < amount:
            print("Bank is bankrupt. Cannot process your transfer request.")
            return
        if to_account not in bank.accounts.values():
            print("Account does not exist")
            return
        self.withdraw(amount)
        to_account.deposit(amount)


class Bank:
    def __init__(self):
        self.accounts = {}
        self.total_balance_in_bank = 0
        self.total_loans_given = 0
        self.loan_feature = True

    def create_account(self, name, email, address, account_type):
        account = Account(name, email, address, account_type)
        self.accounts[account.account_number] = account
        return account.account_number

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
        else:
            print("Account does not exist")

    def list_accounts(self):
        for acc in self.accounts.values():
            print(
                f"Account No: {acc.account_number}, Name: {acc.name}, Balance: {acc.balance}")

    def total_balance(self):
        return self.total_balance_in_bank

    def check_total_loans(self):
        return self.total_loans_given

    def toggle_loan_feature(self):
        self.loan_feature = not self.loan_feature
        print("Loan feature is now:", "ON" if self.loan_feature else "OFF")


def user_interface(account):
    while True:
        print("\nUser Menu")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Check Transaction History")
        print("5. Take Loan")
        print("6. Transfer Money")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            amount = float(input("Enter amount to deposit: "))
            account.deposit(amount)
        elif choice == '2':
            amount = float(input("Enter amount to withdraw: "))
            account.withdraw(amount)
        elif choice == '3':
            print(f"Available balance: {account.check_balance()}")
        elif choice == '4':
            for trans in account.check_transactions():
                print(trans)
        elif choice == '5':
            if bank.loan_feature:
                amount = float(input("Enter loan amount: "))
                account.take_loan(amount)
            else:
                print("Loan feature is currently disabled.")
        elif choice == '6':
            amount = float(input("Enter amount to transfer: "))
            to_acc_num = int(input("Enter account number to transfer to: "))
            if to_acc_num in bank.accounts:
                account.transfer(amount, bank.accounts[to_acc_num])
            else:
                print("Account does not exist")
        elif choice == '7':
            break
        else:
            print("Invalid Choice")


def admin_interface():
    while True:
        print("\nAdmin Menu")
        print("1. Create Account")
        print("2. Delete Account")
        print("3. List All Accounts")
        print("4. Check Total Bank Balance")
        print("5. Check Total Loans")
        print("6. Toggle Loan Feature")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            account_type = input("Enter account type (Savings/Current): ")
            acc_num = bank.create_account(name, email, address, account_type)
            print(f"Account created with Account Number: {acc_num}")
        elif choice == '2':
            acc_num = int(input("Enter account number to delete: "))
            bank.delete_account(acc_num)
        elif choice == '3':
            bank.list_accounts()
        elif choice == '4':
            print(f"Total Bank Balance: {bank.total_balance()}")
        elif choice == '5':
            print(f"Total Loans: {bank.check_total_loans()}")
        elif choice == '6':
            bank.toggle_loan_feature()
        elif choice == '7':
            break
        else:
            print("Invalid Choice")


bank = Bank()

while True:
    print("\nMain Menu")
    print("1. User")
    print("2. Admin")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        acc_num = int(input("Enter your account number: "))
        if acc_num in bank.accounts:
            user_interface(bank.accounts[acc_num])
        else:
            print("Account does not exist")
    elif choice == '2':
        admin_interface()
    elif choice == '3':
        break
    else:
        print("Invalid Choice")
