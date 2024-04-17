import pandas as pd 
import os

class Person:
    def __init__(self, name, phone):
        self.name, self.phone = name, phone

    def save_and_convert_data_to_dataframe(self, file_path, file_name):

        # Make a csv to easier save file between program runs and parse into the dataframe
        csv = (self.convert_to_csv())


        # Create a directory for the csv file if it does not already exist. 
        try:
            os.makedirs(file_path)
            os.close(0)
                
        except FileExistsError:
            pass

        # Write the csv to products.csv under a directory with the sellers name.
        # We do this by making an empty dataframe and writing it (which will create the file) and then opening it and writing the csv. 
        file_path += file_name
        dataframe = pd.DataFrame()
        dataframe.to_csv(file_path)

        file = open(file_path, "w", encoding="utf-8")
        file.write(csv)
        file.close()

        # Finally we open the file and return the dataframe. This process ensures progress is saved in a file. 
        dataframe = pd.read_csv(file_path)
        return dataframe

    def convert_to_csv(self):
        # Meant to be overriden
        pass

class Product:
    def __init__(self, type, name, price, attr={}):
        """
        Takes in what type of product it is, the name of this spesific product along with a price. 
        Optionally you can also pass in a dictionary og additional attributes where the key is 
        the attribute of the product and the value is the value for this product. For example if an apple is red you might do the following: attr={color: "red"}
        """
        self.type,self.name, self.price, self.attr = type, name, price, attr

class Seller(Person):
    def __init__(self, products=[], name="", phone=""):
        super().__init__(name, phone)

        self.customers = []
        self.products = products

    def convert_to_csv(self, headers=["Type", "Name", "Price"]):
        values = []
        
        for product in self.products:
            formatted_product = {}
            
            for header in headers:
                formatted_product[header] = ""

            formatted_product["Name"] = product.name
            formatted_product["Type"] = product.type
            formatted_product["Price"] = product.price

            for key in product.attr.keys():
                value = product.attr[key]

                if (not key in headers):
                    headers.append(key)

                formatted_product[key] = value
        
            values.append(formatted_product)

        csv = ""
        for i in range(len(headers)):
            header = headers[i]
            csv += f"{header}," if (not i == len(headers)-1) else f"{header}"
        csv += "\n"
        
        for value in values:
            for i in range(len(headers)):
                header = headers[i]

                csv += "," if (not i == len(headers) and not i == 0) else ""

                try:
                    csv += f"{value[header]}"
                except KeyError:
                    csv += ""

            csv += "\n"
        
        return csv
    
    def add_customer(self, customer):
        self.customers.append(customer)

    def display_customers(self):
        for customer in self.customers:
            print(f"\n{customer.name} (Mobil: {customer.phone})\n")
            print(customer.save_and_convert_data_to_dataframe(f"\\REKO\\Customer\\{customer.name}", "order.csv"))
            print(f"\nTotal: {customer.get_total()}kr\n")
        pass

    def display_products(self):
        print(self.save_and_convert_data_to_dataframe(f"\\REKO\\Seller\\{self.name}", "products.csv"))


    def display_total_ordered(self):
        products = {}
        for customer in self.customers:
            for product in customer.order:
                try:
                    products[product.name] = {"amount": products[product.name] + product.amount, "total": (products[product.name] + product.amount)*product.price}
                except KeyError:
                    products[product.name] ={"amount":  product.amount, "total": product.amount*product.price}

        for product in products:
            print(f"{product} has {products[product]['amount']} orders for a total of {products[product]['total']}kr")


class Customer(Person):
    def __init__(self, name, phone, order=[]):
      self.name, self.phone = name, phone
      self.order = order

    def add_product(self, product, amount):
        product.amount = amount
        self.order.append(product)

    def get_total(self):
        price = 0

        for product in self.order:
            price += product.price*product.amount

        return price
    
    def display_order(self):
        print(self.save_and_convert_data_to_dataframe(f"\\REKO\\Customer\\{self.name}", "order.csv"))
    
    def convert_to_csv(self):
        values = []
        headers = ["Name", "Amount", "Price", "Sub Total"]
        
        for product in self.order:
            formatted_product = {}

            formatted_product["Name"] = product.name
            formatted_product["Amount"] = product.amount
            formatted_product["Price"] = product.price
            formatted_product["Sub Total"] = product.amount * product.price
        
            values.append(formatted_product)

        csv = ""
        for i in range(len(headers)):
            header = headers[i]
            csv += f"{header}," if (not i == len(headers)-1) else f"{header}"
        csv += "\n"
        
        for value in values:
            for i in range(len(headers)):
                header = headers[i]

                csv += "," if (not i == len(headers) and not i == 0) else ""

                try:
                    csv += f"{value[header]}"
                except KeyError:
                    csv += ""

            csv += "\n"
        
        return csv
    





products = [
    Product("Mel", "Landhvete", 34, {"Best Før": "01.03.2025"}),
    Product("Mel", "Spelt", 44, {"Best Før": "01.03.2025"}),
    Product("Mel", "Emmer", 52, {"Best Før": "01.03.2025"}),
    Product("Eple", "Gravensten", 56, {"Farge": "Rød"}),
    Product("Eple", "Granny Smith", 45, {"Farge": "Grønn"}),
    Product("Eple", "Aroma", 42, {"Farge": "Rød"}),
]

seller = Seller(products, name="Magne Auke", phone="44 55 44 55")
print(seller.save_and_convert_data_to_dataframe(f"\\REKO\\Seller\\{seller.name}", "products.csv"))

customer = Customer("Trine Skare", "43 25 54 32",)
customer.add_product(products[0],2)
seller.add_customer(customer)

seller.display_customers()
seller.display_total_ordered()