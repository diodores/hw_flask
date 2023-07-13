from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = 'ads.db'

def create_ads_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT NOT NULL,
                        created_date TEXT NOT NULL,
                        owner TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.route('/ads', methods=['GET'])
def get_all_ads():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ads")
    ads = cursor.fetchall()
    conn.close()
    return jsonify(ads)

@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ads WHERE id=?", (ad_id,))
    ad = cursor.fetchone()
    conn.close()
    if ad:
        return jsonify(ad)
    else:
        return jsonify({'error': 'Ad not found'}), 404

@app.route('/ads', methods=['POST'])
def create_ad():
    if not request.json or 'title' not in request.json or 'description' not in request.json or 'owner' not in request.json:
        return jsonify({'error': 'Invalid request'}), 400

    ad = {
        'title': request.json['title'],
        'description': request.json['description'],
        'created_date': request.json.get('created_date', ''),
        'owner': request.json['owner']
    }

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ads (title, description, created_date, owner) VALUES (?, ?, ?, ?)",
                   (ad['title'], ad['description'], ad['created_date'], ad['owner']))
    conn.commit()
    ad_id = cursor.lastrowid
    conn.close()

    ad['id'] = ad_id
    return jsonify(ad), 201

@app.route('/ads/<int:ad_id>', methods=['PUT'])
def update_ad(ad_id):
    if not request.json:
        return jsonify({'error': 'Invalid request'}), 400

    ad = {
        'title': request.json.get('title', ''),
        'description': request.json.get('description', ''),
        'created_date': request.json.get('created_date', ''),
        'owner': request.json.get('owner', '')
    }

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE ads SET title=?, description=?, created_date=?, owner=? WHERE id=?",
                   (ad['title'], ad['description'], ad['created_date'], ad['owner'], ad_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Ad updated successfully'})

@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ads WHERE id=?", (ad_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Ad deleted successfully'})

if __name__ == '__main__':
    create_ads_table()
    app.run(debug=True)
