import sqlite3, os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

companies = ["company_X", "company_Y", "company_Z"]
db = "/database.db"
seed_data = "/seed_data.sql"


def get_db_connection(company):
    try:
        connection = sqlite3.connect(company + db)
    except Exception as e:
        print("Error connecting to database: " + str(e))
    return connection


def query_db(company, query):
    cursor = get_db_connection(company).cursor()
    try:
        cursor.execute(query)
        result = [
            dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in cursor.fetchall()
        ]
        cursor.connection.commit()
    except Exception as e:
        result = {"error": str(e)}
        cursor.connection.rollback()
    finally:
        cursor.connection.close()
    return result

def db_setup(company):
    try:
        connection = get_db_connection(company)

        with open("schema.sql") as schema_f:
            connection.executescript(schema_f.read())
        schema_f.close()
        connection.commit()

        with open(company + seed_data) as seed_data_f:
            connection.executescript(seed_data_f.read())
        seed_data_f.close()
        connection.commit()

        print("Database setup for "+ company +" completed successfully.")

    except Exception as e:
        connection.rollback()
        print("Error setting up the database for "+ company +": " + str(e))
    finally:
        connection.close()


@app.route("/new_po", methods=["POST"])
def new_po():
    result = []
    post_data = request.get_json()

    # check if PO number exists
    query_poNo = "SELECT poNo FROM POs WHERE poNo = '{poNo}'".format(
        poNo=post_data["poNo"]
    )
    for company in companies:
        if query_db(company, query_poNo) != []:
            result = {"error": "PO number already exists!"}
            return jsonify(result)
        
    # check if client ID exists
    query_clientId = (
        "SELECT clientId FROM Clients WHERE clientId = '{clientId}'".format(
            clientId=post_data["clientId"]
        )
    )

    for company in companies:
        if query_db(company, query_clientId) != []:
            result = {"message": "success"}
            break

    if result == []:
        result = {"error": "Client ID " + post_data["clientId"] + " does not exist!"}
        return jsonify(result)
    
    # create PO
    query_createPO = "INSERT INTO POs VALUES ('{poNo}', '{clientId}', '{dateOfPO}', '{status}')".format(
                poNo=post_data["poNo"],
                clientId=post_data["clientId"],
                dateOfPO=post_data["dateOfPO"],
                status="Ordered",
            )
    query_db("company_Z", query_createPO)
   
    for line in post_data["lines"]:
        result = []

        # check if part number exists
        query_partNo = "SELECT partNo FROM Parts WHERE partNo = '{partNo}'".format(
            partNo=line["partNo"]
        )

        for company in companies:
            if query_db(company, query_partNo) != []:
                result = {"message": "success"}
                break

        if result == []:
            result = {"error": "Part number " + line["partNo"] + " does not exist!"}
            return jsonify(result)

        query = "INSERT INTO Lines VALUES ('{poNo}', '{partNo}', {qty}, {price})".format(
                poNo=post_data["poNo"],
                partNo=line["partNo"],
                qty=line["qty"],
                price=line["priceOrdered"],
            )
        query_db("company_Z", query)
        
    return jsonify({"message": "success"})


@app.route("/po_list", methods=["GET"])
def po_list():
    result = {}
    query = "SELECT * FROM POs"
    for company in companies:
        result[company] = query_db(company, query)
    return jsonify(result)


@app.route("/part_list", methods=["GET"])
def part_list():
    result = {}
    query = "SELECT * FROM Parts"
    for company in companies:
        result[company] = query_db(company, query)
    return jsonify(result)


@app.route("/part_lookup", methods=["GET"])
def part_lookup():
    partNo = request.args.to_dict().get("input")
    query = "SELECT * FROM Parts WHERE partNo = '{partNo}'".format(
        partNo=partNo
        )
    for company in companies:
        result = query_db(company, query)
        if result != []:
            return jsonify(result)

    result = {"error": "Part number does not exist!"}
    return jsonify(result)


@app.route("/po_lookup", methods=["GET"])
def po_lookup():
    poNo = request.args.to_dict().get("input")
    query = "SELECT * FROM Lines WHERE poNo = '{poNo}'".format(poNo=poNo)
    for company in companies:
        result = query_db(company, query)
        if result != []:
            return jsonify(result)

    result = {"error": "PO number does not exist!"}
    return jsonify(result)


if __name__ == "__main__":
    for company in companies:
        db_setup(company)
    app.run(host="0.0.0.0", port=5001)
