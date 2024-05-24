import os
import random
import hashlib

class Account:
    def __init__(self, account_number, password, account_type):
        self.account_number = account_number
        self.password = self.hash_password(password)
        self.account_type = account_type
        self.balance = 0.0

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.hash_password(password) == self.password

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def __str__(self):
        return f"Account Number: {self.account_number}, Type: {self.account_type}, Balance: {self.balance:.2f}"

    def save_to_file(self, filename="accounts.txt"):
        with open(filename, "a") as file:
            file.write(f"{self.account_number},{self.password},{self.account_type},{self.balance}\n")

class PersonalAccount(Account):
    def __init__(self, account_number, password):
        super().__init__(account_number, password, "Personal")

class BusinessAccount(Account):
    def __init__(self, account_number, password):
        super().__init__(account_number, password, "Business")

class Bank:
    def __init__(self, accounts_file="accounts.txt"):
        self.accounts_file = accounts_file
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = {}
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, "r") as file:
                for line in file:
                    account_number, password, account_type, balance = line.strip().split(",")
                    if account_type == "Personal":
                        account = PersonalAccount(account_number, password)
                    else:
                        account = BusinessAccount(account_number, password)
                    account.balance = float(balance)
                    accounts[account_number] = account
        return accounts

    def save_account(self, account):
        account.save_to_file(self.accounts_file)

    def create_account(self, account_type, password):
        account_number = str(random.randint(10000, 99999))
        if account_type == "Personal":
            account = PersonalAccount(account_number, password)
        else:
            account = BusinessAccount(account_number, password)
        self.accounts[account_number] = account
        self.save_account(account)
        return account

    def login(self, account_number, password):
        account = self.accounts.get(account_number)
        if account and account.check_password(password):
            return account
        else:
            raise ValueError("Invalid account number or password")

    def transfer(self, from_account, to_account_number, amount):
        to_account = self.accounts.get(to_account_number)
        if not to_account:
            raise ValueError("Receiving account does not exist")
        from_account.withdraw(amount)
        to_account.deposit(amount)
        self.save_account(from_account)
        self.save_account(to_account)

def main():
    bank = Bank()
    print("Welcome to the Terminal Bank Application")

    while True:
        print("\n1. Open Account\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            account_type = input("Enter account type (Personal/Business): ")
            password = input("Enter your password: ")
            account = bank.create_account(account_type, password)
            print(f"Account created successfully. Your account number is {account.account_number}")

        elif choice == '2':
            account_number = input("Enter your account number: ")
            password = input("Enter your password: ")
            try:
                account = bank.login(account_number, password)
                print(f"Welcome, {account.account_type} account holder!")
                while True:
                    print("\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Transfer\n5. Logout")
                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':
                        print(f"Your balance is: {account.balance:.2f}")

                    elif user_choice == '2':
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        bank.save_account(account)
                        print(f"Deposited successfully. New balance: {account.balance:.2f}")

                    elif user_choice == '3':
                        amount = float(input("Enter amount to withdraw: "))
                        try:
                            account.withdraw(amount)
                            bank.save_account(account)
                            print(f"Withdrawn successfully. New balance: {account.balance:.2f}")
                        except ValueError as e:
                            print(e)

                    elif user_choice == '4':
                        to_account_number = input("Enter account number to transfer to: ")
                        amount = float(input("Enter amount to transfer: "))
                        try:
                            bank.transfer(account, to_account_number, amount)
                            print(f"Transferred successfully. New balance: {account.balance:.2f}")
                        except ValueError as e:
                            print(e)

                    elif user_choice == '5':
                        print("Logged out successfully.")
                        break

                    else:
                        print("Invalid choice. Please try again.")

            except ValueError as e:
                print(e)

        elif choice == '3':
            print("Thank you for using Terminal Bank. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
