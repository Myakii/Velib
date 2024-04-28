from flask import Flask, request, jsonify, render_template, redirect
import mysql.connector
import json

app = Flask(__name__)

def get_database_connection():
    return mysql.connector.connect(
        user='root',
        password='',
        database='velib',
    )

def execute_query(query, data=None):
    connection = get_database_connection()
    cursor = connection.cursor()
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    connection.commit()
    connection.close()

@app.route('/')
def index():
    return "<p>Bienvenue</p>"

@app.route('/favoris', methods=['POST'])
def add_favorite():
    connection = get_database_connection()
    data = request.json
    id_favoris = data.get('id_favoris')
    id_user = data.get('id_user')
    nom = data.get('nom')
    data_json = json.dumps(data.get('data_json'))

    query = "INSERT INTO favoris (id_favoris, id_user, nom, data_json) VALUES (%s, %s, %s, %s)"
    execute_query(query, (id_favoris, id_user, nom, data_json))
    connection.close()

    return jsonify({"message": "Favori ajouté avec succès"})

@app.delete('/favoris/<int:id_favoris>')
def delete_favorite(id_favoris):
    connection = get_database_connection()
    query = "DELETE FROM favoris WHERE id_favoris = %s"
    execute_query(query, (id_favoris,))
    connection.close()

    return jsonify({"message": "Favori supprimé avec succès"})

@app.route('/favoris/modification/<int:id_favoris>', methods=['GET', 'POST'])
def update_favorites(id_favoris):
    if request.method == 'POST':
        nom = request.form.get('nom')
        connection = get_database_connection()
        cursor = connection.cursor()
        query = "UPDATE favoris SET nom = %s WHERE id_favoris = %s"
        cursor.execute(query, (nom, id_favoris))
        connection.commit()
        connection.close()

        return redirect('/favoris/lire/{}'.format(id_favoris))
    else:
        connection = get_database_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM favoris WHERE id_favoris = %s"
        cursor.execute(query, (id_favoris,))
        favoris = cursor.fetchone()
        connection.close()

        return render_template('modification.html', favoris=favoris)


@app.route('/favoris/lire/<int:id_favoris>')
def afficher_favoris(id_favoris):
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM favoris WHERE id_favoris = %s"
    cursor.execute(query, (id_favoris,))
    favoris = cursor.fetchone()
    connection.close()
    return render_template('favoris.html', favoris=favoris)

if __name__ == "__main__":
    app.run(debug=True)

