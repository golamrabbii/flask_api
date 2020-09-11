from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import pandas as pd
import sqlite3


app = Flask(__name__)
CORS(app)
app.config['JSON_SORT_KEYS'] = False


@app.route("/covid",methods=["GET"])
def home():
    key = request.args.get("key")
    ptype = request.args.get("ptype")
    country,code=[],[]
    connection = sqlite3.connect('covidDB.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT country FROM COVID")
    
    for name in cursor.fetchall():
        country.append(name[0])
    
    cursor.execute("SELECT country_code FROM COVID")
    
    for name in cursor.fetchall():
        code.append(name[0])
    
    if ptype == 'Country Code' and key in code:

        cursor.execute("SELECT * FROM COVID where country_code like '%'||?||'%';",(key,))
        for name in cursor.fetchall():
            data = {
                'ID' : name[0],
                'Country Name' : name[1],
                'Country Code' : name[2],
                'Total Cases'  : name[3],
                'Recovered Cases' : name[4],
                'Death Cases' : name[5]
            }
        connection.close()
    elif ptype == 'Country' and key in country:

        cursor.execute("SELECT * FROM COVID where country like '%'||?||'%';",(key,))
        for name in cursor.fetchall():
            data = {
                'ID' : name[0],
                'Country Name' : name[1],
                'Country Code' : name[2],
                'Total Cases'  : name[3],
                'Recovered Cases' : name[4],
                'Death Cases' : name[5]
            }
        connection.close()
    else:
        data = {
            "message":"Invalid Country Name/Country Code"
        }
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1',port=8027)
    
