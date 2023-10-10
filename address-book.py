###
#   address-book.py
#
# Requirements:
#   1. Add a new contact with a name, phone number, and email address
#   2. View a list of all contacts in the address book
#   3. Search for a contact by name and display their information
#   4. Update contact information (phone number and email) based on the name
#   5. Delete a contact name

import json
import uuid

class AddressBook():
    def __init__(self):
        self.address_book = {}
        
    def loadAddressBook(self, file:str):
        """Load existing address book from file."""
        with open(file, "r") as f:
            self.address_book = json.load(f)
            
    def saveAddressBook(self, file:str):
        """Save address book to file."""
        with open(file, "w") as f:
            json.dump(self.address_book, f, indent=4)
    
    def addNewContact(self, name:str, addr:str, phone:str):
        """Add a contact to the address book."""
        self.address_book[str(uuid.uuid1())] = {"name": name, "address": addr, "phone": phone}

    def viewAll(self):
        """Get all contact information in the address book."""
        if self.address_book != {}:
            return self.address_book
        else:
            return None

    def searchByName(self, name:str) -> dict:
        """Search for a contact in address book by name."""
        for i, contact in enumerate(self.address_book):
            if name.lower() in self.address_book[contact]['name'].lower():
                return self.searchById(contact)
    
    def updateById(self, cid:str, name:str, addr:str, phone:str):
        """Update and existing contact with a given name."""
        self.address_book[cid] = {
            'name': name,
            'address': addr,
            'phone': phone
        }

    def deleteById(self, cid:str):
        """Delete a contact with a given name."""
        if cid in self.address_book.keys():
            del self.address_book[cid]
            
    def searchById(self, cid) -> dict:
        """Given an id, return a contact dict"""
        if cid in self.address_book:
            return self.address_book[cid]
        else:
            return None
        
    def getIdByName(self, name:str) -> str:
        """Given a name, return a contact ID"""
        for i, contact in enumerate(self.address_book):
            if name.lower() in self.address_book[contact]['name'].lower():
                return contact
        return None        

def app():
    book = AddressBook()
    book_file = "./address-book.json"
    try:
        # Attempt to load file
        book.loadAddressBook(book_file)
    except:
        # Create the address file.
        open(book_file, "w").close()
    
    text_menu = """
            Address Book            
    ----------------------------
    1. View All Contacts
    2. Add New Contact
    3. Update Contact
    4. Search For Contact
    5. Delete Contact
    0. Exit Application"""
    exit_app = False
    while not exit_app:
        print(text_menu)
        ins = input("> ")
        match ins:
            case "0":
                exit_app = True
            case "1": # View All Contacts
                contacts = book.viewAll()
                if contacts != None:
                    print(f"{'Name':<15} {'Address':<40} {'Phone #':<15}")
                    for contact in contacts:
                        print(f"{contacts[contact]['name']:<15} {contacts[contact]['address']:<40} {contacts[contact]['phone']:<15}")
                    input("Press any key to continue... ")
                del contacts
            case "2": # Add New Contact
                name = input("Enter name of contact: ")
                addr = input("Enter address of contact: ")
                phone = input("Enter phone # of contact: ")
                print(f"\n{'Name':<15} {'Address':<40} {'Phone #':<15}")
                print(f"{name:<15} {addr:<40} {phone:<15}")
                confirm = input("Does this look right? (y/n)> ")
                if confirm.lower() == "y" or confirm.lower() == "yes":
                    book.addNewContact(name, addr, phone)
                del name, addr, phone, confirm
            case "3": # Update A Contact
                ins = input("Enter the name of the contact you would like to update: ")
                contact = book.searchByName(ins)
                if contact:
                    cid = book.getIdByName(contact['name'])
                    print(f"{'Name':<15} {'Address':<40} {'Phone #':<15}")
                    print(f"{contact['name']:<15} {contact['address']:<40} {contact['phone']:<15}")
                    name = input("Enter name of contact: ")
                    addr = input("Enter address of contact: ")
                    phone = input("Enter phone # of contact: ")
                    print(f"\n{'Name':<15} {'Address':<40} {'Phone #':<15}")
                    print(f"{name:<15} {addr:<40} {phone:<15}")
                    confirm = input("Does this look right? (y/n)> ")
                    if confirm.lower() == "y" or confirm.lower() == "yes":
                        book.updateById(cid, name, addr, phone)
                        print(f"{name} has been added to contacts.")
                        input("Press any key to continue... ")
                    del contact, name, addr, phone, confirm
                else:
                    del contact
            case "4": # Search For Contact by Name
                ins = input("Enter the contact name: ")
                contact = book.searchByName(ins)
                if contact:
                    print(f"{'Name':<15} {'Address':<40} {'Phone #':<15}")
                    print(f"{contact['name']:<15} {contact['address']:<40} {contact['phone']:<15}")
                else:
                    print("That contact was not found.")
                input("Press any key to continue... ")
                del contact
            case "5": # Delete Contact by Name
                ins = input("enter the contact name: ")
                contact = book.searchByName(ins)
                if contact:
                    cid = book.getIdByName(contact['name'])
                    print(f"{'Name':<15} {'Address':<40} {'Phone #':<15}")
                    print(f"{contact['name']:<15} {contact['address']:<40} {contact['phone']:<15}")
                    confirm = input("Are you sure you want to delete this contact? (y/n): ")
                    if confirm.lower() == "y" or confirm.lower() == "yes":
                        book.deleteById(cid)
                        print("Contact has been deleted.")
                    del contact, confirm
                else:
                    print("That contact was not found.")
                    del contact
            case _: # Invalid Inputs
                print("Please Choose A Valid Option")
        
        book.saveAddressBook(book_file)
        
if __name__ == "__main__":
    app()