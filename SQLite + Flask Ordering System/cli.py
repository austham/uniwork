import requests

# 1. list all parts

def list_all_parts():
    url = "http://localhost:5001/part_list"
    response = requests.get(url)
    for company in response.json():
        for part in response.json()[company]:
            print(
                "\nPart number: {partNo}\nPart name: {partName}\nPart Description: {partDesc}\nCurrent price: ${currentPrice}".format(
                    partNo=part["partNo"],
                    partName=part["partName"],
                    partDesc=part["partDescription"],
                    currentPrice=part["currentPrice"])
            )

# 2. list all POs

def list_all_POs():
    url = "http://localhost:5001/po_list"
    response = requests.get(url)
    for company in response.json():
        for po in response.json()[company]:
            print(
                "\nPO number: {poNo}\nClient ID: {clientId}\nDate of PO: {dateOfPO}\nStatus: {status}".format(
                    poNo=po["poNo"],
                    clientId=po["clientId"],
                    dateOfPO=po["dateOfPO"],
                    status=po["status"])
            )

# 3. lookup part by part number

def lookup_part():
    partNo = input("Enter part number: ").upper()
    url = "http://localhost:5001/part_lookup?input={partNo}".format(partNo=partNo)
    response = requests.get(url)

    try:
        for part in response.json():
            print(
                "\nPart number: {partNo}\nPart name: {partName}\nPart Description: {partDesc}\nCurrent price: ${currentPrice}".format(
                    partNo=part["partNo"],
                    partName=part["partName"],
                    partDesc=part["partDescription"],
                    currentPrice=part["currentPrice"])
            )
    except TypeError:
        print(response.json()["error"])

# 4. lookup PO lines by PO number

def lookup_PO():
    poNo = input("Enter PO number: ").upper()
    url = "http://localhost:5001/po_lookup?input={poNo}".format(poNo=poNo)
    response = requests.get(url)
    print("\nPO number: {poNo}".format(poNo=poNo))
    try:
        for line in response.json():
            print(
                "\nPart number: {partNo}\nQuantity: {quantity}\nPrice: ${price}\nTotal: ${total}".format(
                    partNo=line["partNo"],
                    quantity=line["qty"],
                    price=line["priceOrdered"],
                    total=line["qty"] * line["priceOrdered"])
            )
    except TypeError:
        print(response.json()["error"])

# 5. create new PO  

def create_PO():
    poNo = input("\nEnter PO number: ").upper()
    clientId = input("Enter client ID: ").upper()
    dateOfPO = input("Enter date of PO: ")
    url = "http://localhost:5001/new_po"
    data = {
        "poNo": poNo,
        "clientId": clientId,
        "dateOfPO": dateOfPO
    }
    lines = []
    print("\nAdd lines to PO:")
    # loop until the user says "no" when prompted to add a line
    while True:
        partNo = input("Enter part number: ").upper()
        qty = input("Enter quantity: ")
        priceOrdered = input("Enter price: ")
        line = {
            "partNo": partNo,
            "qty": qty,
            "priceOrdered": priceOrdered
        }
        lines.append(line)
        choice = input("Add another line? (y/n): ")
        if choice != "y":
            break
    data["lines"] = lines
    response = requests.post(url, json=data)
    try:
        print("\nError creating PO: " + response.json()["error"])
    except KeyError:
        print("\nPO created successfully!")

# menu 

def menu():
    print("\nMenu:")
    print("1. List all parts")
    print("2. List all POs")
    print("3. Lookup part by part number")
    print("4. Lookup PO details by PO number")
    print("5. Create new PO")
    print("6. Exit")
    choice = input("Enter choice: ")
    print("\n==================================")
    if choice == "1":
        list_all_parts()
    elif choice == "2":
        list_all_POs()
    elif choice == "3":
        lookup_part()
    elif choice == "4":
        lookup_PO()
    elif choice == "5":
        create_PO()
    elif choice == "6":
        exit()
    else:
        print("Invalid choice!")

# main

if __name__ == "__main__":
    print("\nWelcome to the Company Z CLI!")
    while True:
        menu()
        input("\nPress Enter to continue...")
        print("\n==================================")


