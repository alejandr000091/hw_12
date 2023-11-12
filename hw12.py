import os
import re
import pickle


from collections import UserDict
from datetime import date, datetime


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value


    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = value


    def __str__(self):
        return str(self.value)


class Name(Field):
    ...

class Location(Field):
    ...


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value
        

    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, new_value):
        if len(new_value) != 10 or not new_value.isdigit():
            raise ValueError("Invalid phone number, should contain 10 digits")
        else:
            self.__value = new_value


    def __str__(self):
        return f"Phone: {self.value}"


class Mail(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str) -> None:
        patern_mail = r"[A-z.]+\w+@[A-z]+\.[A-z]{2,}"
        try:
            if bool(re.match(patern_mail, value)):
                self.__value = value
            else:
                raise ValueError("Mail should have the following format nickname@domen.yy")
        except ValueError as e:
            raise ValueError("Mail should have the following format nickname@domen.yy") from e


    # def __str__(self):
    #     return f"Mail: {self.__value}"
    def __str__(self) -> str:
        return f"Mail: {self.__value}"

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value
        

    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, new_value):
        try:
            chek_data = datetime.strptime(new_value, "%Y-%m-%d")
            if chek_data:
                self.__value = new_value
        except:
            raise ValueError("Invalid data format")


class Record:
    def __init__(self, name, phone = None, mail = None, location = None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.mails = [Mail(mail)] if mail else []
        self.location = Location(location)

    def add_location(self, location = None):
        self.location = Location(location)

    def add_phone(self, phone):
        # new_phone = ''.join(filter(str.isdigit, phone))
        self.phones.append(Phone(phone))


    def add_mail(self, value):
        self.mails.append(Mail(value))

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
        if not found:
            raise ValueError(f"The phone {old_phone} is not found.")
            # return f"The phone {old_phone} is not found."

    
    def edit_mail(self, old_mail, new_mail):
        found = False
        for mail in self.mails:
            if mail.value == old_mail:
                mail.value = new_mail
                found = True
        if not found:
            raise ValueError(f"The mail {old_mail} is not found.")
            # return f"The phone {old_phone} is not found."


    def find_phone(self, phone:str):
        for ph in self.phones:
            if ph.value == phone:
                return ph
        return None
    

    def remove_phone(self, phone):
        del_phone = None
        for ph in self.phones:
            if ph.value == phone:
                del_phone = ph
        self.phones.remove(del_phone)


    def add_birthday(self, birthday = None):
        self.birthday = Birthday(birthday)


    def days_to_birthday(self):
        today = date.today()
        d_bd = datetime.strptime(self.birthday.value, "%Y-%m-%d")
        if d_bd.month - today.month < 0:
            next_bd = date(2024,d_bd.month, d_bd.day)
            delta_days = next_bd - today
            return delta_days.days
        else:
            if d_bd.day - today.day < 0:
                next_bd = date(2024,d_bd.month, d_bd.day)
                delta_days = next_bd - today
                return delta_days.days
            else:
                next_bd = date(2023,d_bd.month, d_bd.day)
                delta_days = next_bd - today
                if delta_days.days == 0:
                    return "today"
                else:
                    return delta_days.days


    def __str__(self):
        return_res = f"Contact name: {self.name.value}"

        if hasattr(self, 'phones') and self.phones:
            return_res += f", phones: {'; '.join(p.value for p in self.phones)}"

        if hasattr(self, 'birthday') and self.birthday:
            return_res += f", birthday: {self.birthday}"

        if hasattr(self, 'mails') and self.mails:
            return_res += f", mail: {'; '.join(m.value for m in self.mails)}"

        if hasattr(self, 'location') and self.location:
            return_res += f", location: {self.location}"

        return return_res
        

class AddressBook(UserDict):
    def add_record(self,new_contact:Record) -> None:
        self.data[new_contact.name.value] = new_contact
        return f"Contact {new_contact.name.value} added succefully"


    def find(self, name):
        for rec in self.data:
            if rec == name:
                return self.data[rec]
        if not self.data.get(name):
            return None
        

    def search(self, arg):
        return_str = "didn'd find number or characters"
        for rec, phone in self.data.items():
            # print(rec, phone)
            if arg in str(phone):
                if return_str ==  "didn'd find number or characters":
                    return_str = ""
                return_str += str(self.data[rec]) + "\n"
            # else:
            #     return "didn'd find number or characters"
        return return_str
        

    def delete(self, name):
        if not self.data.get(name):
            return f"did't delete contact {name}, not exsist"
        else:
            del self.data[name]
            return f"Contact {name} delete succsefull"
        

    def iterator(self, n=2):
        self.counter = 0
        self.list = []
        #self.data_list = list(self.data.items())
        if len(self.data) >=1:
            for _, val in self.data.items():
                self.list.append(str(val ))
            while self.counter < len(self.list):
                yield self.list[self.counter: self.counter + n]
                self.counter += n
            raise StopIteration("End of list")
        else:
            raise StopIteration("Empty list")
        
     
    def save_address_book(self):
        self.file_name = 'address_book.bin'
        with open(self.file_name , "wb") as file:
            pickle.dump(self, file)

    
    def load_address_book(self):
        self.file_name = 'address_book.bin'
        if os.path.exists(self.file_name):
            with open(self.file_name, "rb") as file:
                unpacked = pickle.load(file)
            return unpacked
        else:
            return "File not found"


records = AddressBook()


def search(*args):
    return records.search(*args)


def save_ab(*args):
    records.save_address_book()
    return "Address book saved successful"


def load_ab(*args):
    global records
    load_records = records.load_address_book()
    records = load_records
    return "Address book loaded successful"


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Give me name and phone please"
        except KeyError:
            return "Enter correct user name"
        except RuntimeError:
            return "Nothing more. End of list"
        except StopIteration as e:
            if str(e) == "End of list":
                return "End of list"
            if str(e) == "Empty list":
                return "Empty list"
            else:
                raise e
        except ValueError as e:
            if str(e) == "Not enough number":
                return "Not enought number"
            if str(e) == "Invalid data format":
                return "Invalid data format"
            if str(e) == "Invalid phone number, should contain 10 digits":
                return "Invalid phone number, should contain 10 digits"
            if str(e) == "Mail should have the following format nickname@domen.yy":
                return "Mail should have the following format nickname@domen.yy"
            if str(e) == "wrong name, try again":
                return "wrong name, try again"
            else:
                raise e  # Піднімаэмо помилку наверх, якщо вона іншого типу
    return inner


def sanitize_phone_number(phone):
    collected_phone = ""
    for ch in phone:
        collected_phone += ch
    new_phone = (
        collected_phone.strip()
            .removeprefix("+38")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    return new_phone
    

def sanitize_db(db):
    collected_db = ""
    for ch in db:
        collected_db += ch
    new_db = (
        collected_db.strip()
            .replace(" ", "-")
            .replace("(", "")
            .replace(")", "")
            .replace(".", "-")
            .replace(",", "-")
            .replace("/", "-")
            .replace("\\", "-")
    )
    return (new_db)
    

@user_error
def add_record(*args):
    name = args[0]
    phone_number = sanitize_phone_number(args[1:])
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_phone(phone_number)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_phone(phone_number)
    return f"Add record {name = }, {phone_number = }"


@user_error 
def bd_add(*args):
    name = args[0]
    bd = sanitize_db(args[1:])
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_birthday(bd)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_birthday(bd)
    return f"Add record {name = }, {bd = }"


def loc_add(*args):
    name = args[0]
    loc = args[1:]
    location = ""
    for ch in loc:
        location +=  " " + ch
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_location(location)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_location(location)
    return f"Add record {name = }, {location = }"

@user_error 
def mail_add(*args):
    name = args[0]
    mail = str(args[1])
    if not records.data.get(name):
        name_record = Record(name)
        name_record.add_mail(mail)
        records.add_record(name_record)
    else:
        name_record = records.data.get(name)
        name_record.add_mail(mail)
    return f"Add record {name = }, {mail = }"


@user_error
def mail_change(*args):
    name = args[0]
    old_mail = str(args[1])
    new_mail = str(args[2])
    if not records.data.get(name):
        raise ValueError("wrong name, try again")
    else:
        try:
            name_record = records.data.get(name)
            try:
                name_record.edit_mail(old_mail, new_mail)
                return f"Change record {name = }, {new_mail = }"
            except:
                return f"The mail {new_mail} is not valid."
        except:
            return f"The mail {old_mail} is not found."


def days_to_bd(*args):
    try:
        name = args[0]
        if name:
            if records.data.get(name):
                name_record = records.data.get(name)
                try:
                    result = name_record.days_to_birthday()
                    if result:
                        if result == "today":
                            return f"To {name } birthday today"
                        else:
                            return f"To {name } birthday,  left {result} days"
                    else:
                        return f"To {name } no data birthday"
                except:# AttributeError as e:
                    return(f"No birthday date for {name}")
            else:
                return(f"No contact find {name}")
    except:# AttributeError as e:
        return("No contact input")


@user_error
def change_record(*args):
    name = args[0]
    old_phone_number = sanitize_phone_number(args[1])
    new_phone_number = sanitize_phone_number(args[2])
    if not records.data.get(name):
        raise ValueError("wrong name")
    else:
        try:
            name_record = records.data.get(name)
            try:
                name_record.edit_phone(old_phone_number, new_phone_number)
                return f"Change record {name = }, {new_phone_number = }"
            except:
                return f"The phone {new_phone_number} is not valid."
        except:
            return f"The phone {old_phone_number} is not found."


def delete_record(*args):
    name = args[0]
    records.delete(name)
    return f"Contact name: {name}, delete successfull"


def unknown_cmd(*args):
    return "Unknown command. Try again. Or use 'help'"


def hello_cmd(*args):
    return "How can I help you?"


def help_cmd(*args):
    return_str = "\n"
    cmd_list = ["avalible command:",
            "hello - just say hello",
            "help - show avalible cmd",
            "add - add record - format 'name phone'",
            "mail_add - add mail - format 'name nickname@domen.yy'",
            "mail_change - change mail - format 'name old mail new mail'",
            "bd_add - add birthday/or replace, if data olready exist - format 'name date birthday (YYYY-MM-DD)'",
            "location_add - add location/or replace, if data olready exist "
            "days_to_bd - days to birthday",
            "change - change record - format 'name old phone new phone'",
            "delete - delete record - format 'name'",
            "phone - get phone by name - format 'phone name'",
            "show_all - show all phone book",
            "save_ab - save address book",
            "search - search by characters in name, or by digits in phone"
            "load_ab - load address book",
            "good bye/close/exit - shotdown this script"]
    for ch in cmd_list:
        return_str += ch + "\n"
    return return_str


@user_error
def get_phone(*args):
    name = args[0]
    rec = records.find(name)
    if rec:
        return rec
    

# @user_error 
def show_all(*args):
    n = None
    try:
        n = int(args[0])
        if n is not None:
            return_lst_result = []
            if len(records) >= 1:
                for cont in records.iterator(n):
                    return_lst = []
                    for ch in cont:
                        new_ch = (str(ch).strip()
                                        .replace("(", "")
                                        .replace(")", "")
                                        .replace("'", "")
                                )
                        return_lst.append(new_ch)
                    return_lst_result.append(return_lst)
                return return_lst_result
            else:
                return "Empty"
    except:
        if n is  None:
            return_str = "\n"
            if len(records.data) >=1:
                for _, numbers in records.data.items() :
                    return_str += str(numbers) + "\n"
                return return_str
            else:
                return "Empty"
        else:
            return return_lst_result #"No records to show"
        

def close_cmd(*args):
    return "Good bye!"

COMMANDS = {add_record: "add",
            # add_phone: "add phone",
            # edit_phone: "edit phone",
            mail_add: "mail_add",
            loc_add: "location_add",
            mail_change: "mail_change",
            bd_add: "bd_add",
            days_to_bd: "days_to_bd",
            delete_record: "delete",
            change_record: "change",
            hello_cmd: "hello",
            get_phone: "phone",
            show_all: "show_all",
            save_ab: "save_ab",
            load_ab: "load_ab",
            search: "search",
            help_cmd: "help",
            close_cmd: ("good bye", "close", "exit")}


def parser(text: str):
    for func, kw in COMMANDS.items():
        if text.lower().startswith(kw):
            return func, text[len(kw):].strip().split()
    return unknown_cmd, []


def main():
    while True:
        user_input = input(">>>")
        func, data = parser(user_input)
        if func == show_all and data:
            result1 = show_all(*data)
            if result1 != "Empty":
                for el in result1:
                    input("Press Enter for see next records")
                    for cont in el:
                        print(cont)
                input("Press Enter to exit, and input new command")
            else:
                print(func(*data))
        else:
            print(func(*data))
        if func == close_cmd:
            break


if __name__ == "__main__":
    main()
    # # Створення нової адресної книги
    # book = AddressBook()

    # # Створення запису для John
    # john_record = Record("John")
    # john_record.add_phone("1234567890")
    # john_record.add_phone("5555555555")
    # john_record.add_birthday("1991-04-21")
    # john_record.add_mail("alejandr@gmail.c")
    # print(john_record.mails)

    # # Додавання запису John до адресної книги
    # book.add_record(john_record)

    # # Створення та додавання нового запису для Jane
    # jane_record = Record("Jane")
    # jane_record.add_phone("9876543210")
    # book.add_record(jane_record)

    # # Виведення всіх записів у книзі
    # for name, record in book.data.items():
    #     print(record)

    # # Знаходження та редагування телефону для John
    # john = book.find("John")
    # john.edit_phone("1234567890", "1112223333")

    # print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # # Пошук конкретного телефону у записі John
    # found_phone = john.find_phone("5555555555")
    # print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # # Видалення запису Jane
    # book.delete("Jane")
