from flask import Flask, render_template, jsonify, request, redirect, url_for, session, make_response
import mysql.connector
import json
from server import VelibData
from flask_mysqldb import MySQL

app = Flask(__name__)
velib_data = VelibData()
app.secret_key = b"flyyoufools"

@app.route("/")
def accueil():
    return render_template("index.html")

#récupération des données à une autre route en important la variable depuis server.py, lancé en amont et qui aura récupéré les données de l'api
@app.route("/velib")
def velib():
    data = get_velib_data()
    response = jsonify(data)
    #ajout des headers pour les autorisations CORS
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def get_velib_data():
    data = velib_data.fetch_data()
    if data:
        return data
    else:
        return {"error": "Erreur lors de la récupération des données Velib."}

def get_database_connection():
    return mysql.connector.connect(
        user='root',
        password='',
        database='velib'
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

@app.route("/favoris", methods=["GET", "POST"])
def favoris():
    if request.method == "POST":
        id_user = request.form.get('id_user')
        nom = request.form.get('nom')
        data_json = json.dumps({
            "name": request.form.get('name'),
            "numbikesavailable": request.form.get('numbikesavailable'),
            "numdocksavailable": request.form.get('numdocksavailable'),
            "ebike": request.form.get('ebike'),
            "mechanical": request.form.get('mechanical')
        })

        connection = get_database_connection()
        query = "INSERT INTO favoris (id_user, nom, data_json) VALUES (%s, %s, %s)"
        execute_query(query, (id_user, nom, data_json))
        connection.close()

        return jsonify({"message": "Favori ajouté avec succès"})

    else:
        stationcode = request.args.get("stationcode")
        nom = request.args.get("nom")
        numbikesavailable = request.args.get("numbikesavailable")
        numdocksavailable = request.args.get("numdocksavailable")
        ebike = request.args.get("ebike")
        mechanical = request.args.get("mechanical")

        station = {
            "stationcode": stationcode,
            "name": nom,
            "numbikesavailable": numbikesavailable,
            "numdocksavailable": numdocksavailable,
            "ebike": ebike,
            "mechanical": mechanical
        }

        return render_template("ajouterfavoris.html", station=station)


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
    return render_template('favorites.html', favoris=favoris)


@app.route("/favorites")
def favorites():
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM favoris"
    cursor.execute(query,)
    favoris = cursor.fetchall()
    connection.close()
    return render_template('favorites.html', favoris=favoris)

    # Configuration MySQL à modifier avec vraie bdd
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_database_name'

mysql = MySQL(app)

ysql = MySQL(app)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Récupère données formulaire
        username = request.form.get["username"]
        password = request.form.get["password"]

        # Connexion à la bdd
        cur = mysql.connection.cursor()

        # Vérifie si user existe déjà
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user:
            return "Cet utilisateur existe déjà !"
        else:
            # Insertion dans la bdd
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            mysql.connection.commit()

            # Fermeture du curseur
            cur.close()

            return render_template("index.html")

    return render_template("register.html")

# Route de connexion
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        # Récupère données formulaire
        username = request.form.get["username"]
        password = request.form.get["password"]

        cur = mysql.connection.cursor()

        # Vérifie si user existe déjà
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username,password))
        user = cur.fetchone()
        
        if user:
            return redirect(url_for("accueil"))

        else:
            return "Username ou mot de passe inconnu"
      
    return render_template("connexion.html")

# Déconnexion
@app.route("/deconnexion")
def deconnexion():
    # Retire la clé prenom de la session
    session.pop("username", None)
    # Redirection
    return redirect(url_for("accueil"))


if __name__ == "__main__":
    app.run(debug=True)
