import requests, csv

#-------constants------
GET_BY_NAME = 1
GET_BY_ID = 2
GET_STORES = 3    
#----------------------    

def get_data(name_id_store, x):
    if x == GET_BY_NAME:
        response = requests.get(URL + "games?title=" + name_id_store)
        xdata = response.json()
        if xdata == []:
            return None     
        else:
            return  xdata
    elif x == GET_BY_ID:
        response = requests.get(URL + "games?id=" + game_id)
        xdata = response.json()
        return xdata
    else:  
        response = requests.get(URL + "stores")
        xdata = response.json()
        return xdata

def obtain_ID (data):
    for x in data:
        return x["gameID"]
    
def storesID_and_prices(deal_data):
    deal_info = []
    offers = deal_data["deals"]
    for offer in offers:
        deal_info.append({
            "store" : offer["storeID"], 
            "price" : offer["price"],
            "deal_id": offer["dealID"]
            })
    return deal_info

def search_store_link(offer_sites, stores):
    for store_id in offer_sites:
        for store_name in stores:
            if store_id["store"] == store_name["storeID"]:
                store_id["store"] = store_name["storeName"]
    return offer_sites

def return_information(offer_sites_with_name):
    print(f"------------ All available offer for: {data[0]["external"]} ------------")
    for offer in offer_sites_with_name:
        print(f"{offer["store"]}: ${offer["price"]}  https://www.cheapshark.com/redirect?dealID={offer["deal_id"]}  ")
    print("-------------------------------------------------")
    
def save_offers(offer_sites_with_names):
    while True:
        answer = input("Do you want to save this information on a .CSV archive ?\n-------------\nYes/No\n-").strip().lower()
        if answer == "no":
            break
        elif answer == "yes":
            with open ("offers.csv", mode="w", newline="") as file: 
                writer = csv.DictWriter(file, fieldnames=["name","store","price","link"])
                writer.writeheader()
                for i in offer_sites_with_names:
                    x = "https://www.cheapshark.com/redirect?dealID=" + i["deal_id"]
                    writer.writerow({"name": data[0]["external"], "store": i["store"], "price": i["price"], "link": x})
            break
        else:
            print("Please select one")

#-------------------------------MAIN BODY-------------------------------
URL = "https://www.cheapshark.com/api/1.0/"
while True:
    name = input("What game are you looking for? ")
    data = get_data(name, GET_BY_NAME)
    if data == None:
        print("No game found with that name, please check the spelling")
    else:
        break
game_id = obtain_ID(data)
deal_data = get_data(game_id, GET_BY_ID)
offer_sites_with_ID = storesID_and_prices(deal_data)
stores = get_data(game_id, GET_STORES)
offer_sites_with_names = search_store_link(offer_sites_with_ID, stores)
return_information(offer_sites_with_names)
save_offers(offer_sites_with_names)
#-----------------------------------------------------------------------
