# a helper script to load faction names/data into the election doc on firestore

import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('bigworld-e4cf4-firebase-adminsdk-g6v6y-8cf756ec6c.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

ELECTION_ID = 'r9nizviywIETk3k0t5t2'  # Document ID on Firestore

regions = [
    "The Steps",
    "The Fangs",
    "Vinegar Spire",
    "Tony's Bonefields",
    "Tony's Eighth Base",
    "Zazu's Hideaway",
    "BigDaddy's Beachfront Property",
    "Tone-A-Lago",
    "Krakenhold",
    "The Tip",
    "Wraith-Smith Forge",
    "Spyre",
    "Solace",
    "Paradox Cliffs",
    "Danny's Fishing Outpost",
    "Valor Cliffs",
    "Dinglebop Plains",
    "Stellar Reach",
    "Zenith",
    "Aumasson",
    "Highlands",
    "Lowlands",
    "Kalos",
    "Hoobler's Alley",
    "Mahoney Mountain Pass",
    "Lake Zibbler",
    "Twisted Forest",
    "The Canadian Department",
    "Raven's Haven",
    "Tony's Trading Outpost",
    "Shroomwood Forest",
    "Monjarnhoe",
    "Mount Twilight",
    "Svathwelier Peninsula",
    "Northreach",
    "Zaros",
    "Maer",
    "Galizea",
    "Even Newer Jersey",
    "Ashor",
    "Pleebletopia",
    "Meronos",
    "Whitefang",
    "Royal Bay",
    "Kyrenis",
    "Zalvaris",
    "Isle of Knawlhorn",
    "Adventurer's Gateway",
    "Kingsroad",
    "Merchant's Lane",
    "Araluen",
    "Canisgard",
    "Aelysium",
    "Big Town",
    "Moru",
    "Teras",
    "Scora",
    "Prifddinas",
    "Nalkua",
    "Nosaer",
    "Shneibler Mainland",
    "Roruna",
    "Zazulania"
]

bigdaddy_bias = [
    "Tony's Eighth Base",
    "Tone-A-Lago",
    "Tony's Trading Outpost",
    "Tony's Bonefields",
    "Zazu's Hideaway",
    "Aumasson",
    "The Steps",
    "Danny's Fishing Outpost",
    "Northreach",
    "Maer",
    "Canisgard",
    "Moru",
    "Svathwelier Peninsula",
    "Zenith",
    "Spyre",
    "The Fangs",
    "Ashor",
    "Solace",
    "Whitefang",
    "Zaros",
    "Prifddinas",
    "Nosaer",
    "Roruna",
    "Shneibler Mainland",
    "Kalos",
    "Hoobler's Alley",
    "Dinglebop Plains",
    "Aelysium",
    "Scora",
    "Wraith-Smith Forge",
    "Mahoney Mountain Pass",
    "Lake Zibbler",
    "Monjarnhoe",
    "Highlands",
    "Mount Twilight",
    "Paradox Cliffs",
    "Stellar Reach",
    "Teras",
    "Krakenhold",
    "Vinegar Spire",
    "Adventurer's Gateway",
    "Isle of Knawlhorn",
    "Raven's Haven",
    "Shroomwood Forest",
    "Araluen",
    "The Tip",
    "Valor Cliffs",
    "Lowlands",
    "Meronos",
    "Royal Bay",
    "Twisted Forest",
    "Zalvaris",
    "Pleebletopia",
    "Kyrenis",
    "Galizea",
    "Merchant's Lane",
    "Nalkua",
    "Kingsroad",
    "Zazulania",
    "Big Town",
    "The Canadian Department",
    "Even Newer Jersey",
    "BigDaddy's Beachfront Property"
]

tony_bias = [
    "BigDaddy's Beachfront Property",
    "The Canadian Department",
    "Even Newer Jersey",
    "Big Town",
    "Zazulania",
    "Kingsroad",
    "Nalkua",
    "Kyrenis",
    "Pleebletopia",
    "Zalvaris",
    "Royal Bay",
    "Meronos",
    "Valor Cliffs",
    "The Tip",
    "Galizea",
    "Araluen",
    "Shroomwood Forest",
    "Raven's Haven",
    "Adventurer's Gateway",
    "Vinegar Spire",
    "Krakenhold",
    "Twisted Forest",
    "Teras",
    "Stellar Reach",
    "Paradox Cliffs",
    "Mount Twilight",
    "Monjarnhoe",
    "Lake Zibbler",
    "Mahoney Mountain Pass",
    "Wraith-Smith Forge",
    "Scora",
    "Aelysium",
    "Dinglebop Plains",
    "Hoobler's Alley",
    "Kalos",
    "Lowlands",
    "Zenith",
    "Roruna",
    "Prifddinas",
    "Isle of Knawlhorn",
    "Whitefang",
    "Solace",
    "Ashor",
    "Zaros",
    "The Fangs",
    "Spyre",
    "Svathwelier Peninsula",
    "Highlands",
    "Nosaer",
    "Canisgard",
    "Maer",
    "Northreach",
    "Merchant's Lane",
    "Danny's Fishing Outpost",
    "The Steps",
    "Aumasson",
    "Zazu's Hideaway",
    "Moru",
    "Shneibler Mainland",
    "Tony's Bonefields",
    "Tony's Trading Outpost",
    "Tone-A-Lago",
    "Tony's Eighth Base",
]

tnp_bias = [
    "Tony's Eighth Base",
    "Tony's Trading Outpost",
    "Tone-A-Lago",
    "Tony's Bonefields",
    "BigDaddy's Beachfront Property",
    "Zazu's Hideaway",
    "Roruna",
    "Moru",
    "Whitefang",
    "Northreach",
    "Wraith-Smith Forge",
    "Shneibler Mainland",
    "Lake Zibbler",
    "Ashor",
    "Even Newer Jersey",
    "Nosaer",
    "Canisgard",
    "Shroomwood Forest",
    "Krakenhold",
    "Prifddinas",
    "Mahoney Mountain Pass",
    "Maer",
    "The Fangs",
    "Zaros",
    "Lowlands",
    "Solace",
    "Svathwelier Peninsula",
    "Aelysium",
    "The Tip",
    "Big Town",
    "The Steps",
    "Kalos",
    "Hoobler's Alley",
    "Scora",
    "Meronos",
    "Zalvaris",
    "Adventurer's Gateway",
    "Kyrenis",
    "Spyre",
    "Vinegar Spire",
    "Twisted Forest",
    "Dinglebop Plains",
    "Monjarnhoe",
    "Zenith",
    "Nalkua",
    "Isle of Knawlhorn",
    "Danny's Fishing Outpost",
    "Pleebletopia",
    "Araluen",
    "Aumasson",
    "Galizea",
    "Highlands",
    "Teras",
    "Merchant's Lane",
    "Raven's Haven",
    "Mount Twilight",
    "Stellar Reach",
    "Paradox Cliffs",
    "Royal Bay",
    "Zazulania",
    "Valor Cliffs",
    "Kingsroad",
    "The Canadian Department",
]

regions_by_bias = {
    "BigDaddy": bigdaddy_bias,
    "Tony": tony_bias,
    "TheNightPatrol": tnp_bias
}

candidates = ["BigDaddy", "Tony", "TheNightPatrol"]

simvotes = {key: {region: 0 for region in regions} for key in candidates}


def load_data(candidate_list, region_list, regions_by_bias = None):
    if (regions_by_bias == None):
        fbb = {c: region_list for c in candidate_list }
    else:
        fbb = regions_by_bias

    try:
        db.collection('elections').document(ELECTION_ID).update({
            'regions': region_list,
            'regions_by_bias': fbb,
            'simvotes': simvotes
        })
    except Exception as e:
        print(f"Failed to store data: {e}")

if __name__ == '__main__':
    load_data(candidates, regions, regions_by_bias)
    print(simvotes)