from AddressBook import *


class Bot:
    def __init__(self, user_interface):
        self.book = AddressBook()
        self.output = user_interface

    def handle(self, action):
        if action == 'add':
            name = Name(self.output.input("Name: ")).value.strip()
            phones = Phone().value
            birth = Birthday().value
            email = Email().value.strip()
            status = Status().value.strip()
            note = Note(self.output.input("Note: ")).value
            record = Record(name, phones, birth, email, status, note)
            return self.book.add(record)
        elif action == 'search':
            self.output.print("There are following categories: \nName \nPhones \nBirthday \nEmail \nStatus \nNote")
            category = self.output.input('Search category: ')
            pattern = self.output.input('Search pattern: ')
            result = (self.book.search(pattern, category))
            for account in result:
                if account['birthday']:
                    birth = account['birthday'].strftime("%d/%m/%Y")
                    result = "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {', '.join(account['phones'])} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50
                    self.output.print(result)
        elif action == 'edit':
            contact_name = self.output.input('Contact name: ')
            parameter = self.output.input('Which parameter to edit(name, phones, birthday, status, email, note): ').strip()
            new_value = self.output.input("New Value: ")
            return self.book.edit(contact_name, parameter, new_value)
        elif action == 'remove':
            pattern = self.output.input("Remove (contact name or phone): ")
            return self.book.remove(pattern)
        elif action == 'save':
            file_name = self.output.input("File name: ")
            return self.book.save(file_name)
        elif action == 'load':
            file_name = self.output.input("File name: ")
            return self.book.load(file_name)
        elif action == 'congratulate':
            self.output.print(self.book.congratulate())
        elif action == 'view':
            self.output.print(self.book)
        elif action == 'exit':
            pass
        else:
            self.output.print("There is no such command!")
