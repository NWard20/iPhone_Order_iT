class IPhoneOrder:
    def __init__(self, customer, address):
        self.__customer = customer
        self.__address = address
        self.__model = ""
        self.__storage = ""
        self.__color = ""
        self.__applecare = "No"
        self.__charger = "No"

    # setters
    def set_model(self, model):
        self.__model = model

    def set_storage(self, storage):
        self.__storage = storage

    def set_color(self, color):
        self.__color = color

    def set_applecare(self, applecare):
        self.__applecare = applecare

    def set_charger(self, charger):
        self.__charger = charger

    # getters
    def get_model(self):
        return self.__model

    def get_storage(self):
        return self.__storage

    def get_color(self):
        return self.__color

    def get_applecare(self):
        return self.__applecare

    def get_charger(self):
        return self.__charger

    def get_customer(self):
        return self.__customer

    def get_address(self):
        return self.__address

    def display_order(self):
        print("\nOrder:")
        print(f"Model: {self.__model}")
        print(f"Storage: {self.__storage}")
        print(f"Color: {self.__color}")
        print(f"AppleCare+: {self.__applecare}")
        print(f"Charger: {self.__charger}")