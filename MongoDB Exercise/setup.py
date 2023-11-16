import pymongo

'''
Setup the MongoDB database with data per the assignment instructions
'''

dbClient = pymongo.MongoClient("mongodb://localhost:27017/")
db = dbClient["a3DataBase"]

# if the collections already exist, drop them
if "players" in db.list_collection_names():
    db.drop_collection("players")
if "teams" in db.list_collection_names():
    db.drop_collection("teams")

db.create_collection("players")
db.create_collection("teams")

playerCollection = db["players"]
teamsCollection = db["teams"]

playerCollection.insert_many([
  {
    "lastName" : 'Smith',
    "firstName" : 'Joe',
    "phoneNo" : '436-3215',
    "teamPref" : [ 'Tigers', 'Sharks', 'Eagles' ]
  },
  {
    "lastName": 'Doe',
    "firstName": 'John',
    "phoneNo": '465-6949',
    "teamPref": [ 'Sharks', 'Eagles', 'Tigers' ]
  },
  {
    "lastName": 'Fritz',
    "firstName": 'Rebecca',
    "phoneNo": '541-8543',
    "teamPref": [ 'Eagles', 'Tigers', 'Sharks' ]
  },
  {
    "lastName": 'MacDonald',
    "firstName": 'Greg',
    "phoneNo": '764-5624',
    "teamPref": [ 'Tigers', 'Eagles', 'Sharks' ]
  },
  {
    "lastName": 'Johnson',
    "firstName": 'Lucy',
    "phoneNo": '824-7790',
    "teamPref": [ 'Eagles', 'Sharks', 'Tigers' ]
  },
  {
    "lastName": 'Moore',
    "firstName": 'Carl',
    "phoneNo": '534-9572',
    "teamPref": [ 'Sharks', 'Tigers', 'Eagles' ]
  },
  {
    "lastName": 'Leblanc',
    "firstName": 'Bob',
    "phoneNo": '694-1948',
    "teamPref": [ 'Tigers', 'Sharks', 'Eagles' ]
  }
])

teamsCollection.insert_many([
  {
    "name" : 'Tigers',
    "managerLastName" : 'Jones',
    "managerFirstName" : 'David',
    "managerPhoneNo" : '945-3215',
    "players" : []
  },
  {
    "name" : 'Sharks',
    "managerLastName" : 'Henderson',
    "managerFirstName" : 'Dana',
    "managerPhoneNo" : '692-6426',
    "players" : []
  },
  {
    "name" : 'Eagles',
    "managerLastName" : 'Wilson',
    "managerFirstName" : 'Joseph',
    "managerPhoneNo" : '703-5963',
    "players" : []
  }
])



