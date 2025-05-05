from flask import Flask, render_template, request, jsonify, redirect
import uuid
import sqlite3
import os

app = Flask(__name__)
DATABASE = "/data/commandes.db"

# 🎲 Emoji des ingrédients et cuissons
EMOJIS_INGREDIENTS = {
    "aubergine": "🍆",
    "courgette": "🥒",
    "poivron": "🌶️",
    "tomate": "🍅",
    "ail": "🧄",
    "oignon": "🧅",
    "huile d'olive": "🫒",
    "herbes de Provence": "🌿"
}

EMOJIS_CUISSONS = {
    "gratinée": "🧀🔥",
    "mijotée": "🍲",
    "vapeur": "💨🍽️"
}

def ajouter_emoji(nom, dictionnaire):
    return f"{dictionnaire.get(nom, '')} {nom}"

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE commandes (
                id TEXT PRIMARY KEY,
                ingredients TEXT,
                cuisson TEXT
            )
        ''')
        conn.commit()
        conn.close()

init_db()

ingredients = list(EMOJIS_INGREDIENTS.keys())
cuissons = list(EMOJIS_CUISSONS.keys())

@app.route('/')
def home():
    return render_template('index.html',
        ajouter_emoji=ajouter_emoji,
        EMOJIS_INGREDIENTS=EMOJIS_INGREDIENTS,
        EMOJIS_CUISSONS=EMOJIS_CUISSONS
    )

@app.route('/compose', methods=['GET', 'POST'])
def compose_ratatouille():
    if request.method == 'POST':
        data = request.form
        if not data or "ingredients" not in data:
            return render_template('compose.html',
                ingredients=ingredients,
                erreur="Merci de sélectionner des ingrédients.",
                ajouter_emoji=ajouter_emoji,
                EMOJIS_INGREDIENTS=EMOJIS_INGREDIENTS
            ), 400

        invalides = [ing for ing in data.getlist("ingredients") if ing not in ingredients]
        if invalides:
            return render_template('compose.html',
                ingredients=ingredients,
                erreur=f"Ingrédients invalides : {', '.join(invalides)}",
                ajouter_emoji=ajouter_emoji,
                EMOJIS_INGREDIENTS=EMOJIS_INGREDIENTS
            ), 400

        selected_ingredients = data.getlist("ingredients")
        return render_template('cuisson.html',
            ingredients=selected_ingredients,
            cuissons=cuissons,
            ajouter_emoji=ajouter_emoji,
            EMOJIS_CUISSONS=EMOJIS_CUISSONS
        )

    return render_template('compose.html',
        ingredients=ingredients,
        ajouter_emoji=ajouter_emoji,
        EMOJIS_INGREDIENTS=EMOJIS_INGREDIENTS
    )

@app.route('/cuisson', methods=['POST'])
def choisir_cuisson():
    data = request.form
    ingredients_choisis = data.getlist("ingredients")
    cuisson = data.get("cuisson")

    if cuisson not in cuissons:
        return render_template("cuisson.html",
            cuissons=cuissons,
            ingredients=ingredients_choisis,
            erreur="Méthode de cuisson invalide.",
            ajouter_emoji=ajouter_emoji,
            EMOJIS_CUISSONS=EMOJIS_CUISSONS
        ), 400

    commande_id = str(uuid.uuid4())
    liste_ingredients = ", ".join(ingredients_choisis)

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO commandes (id, ingredients, cuisson) VALUES (?, ?, ?)",
              (commande_id, liste_ingredients, cuisson))
    conn.commit()
    conn.close()

    return render_template("confirmation.html",
        id=commande_id,
        ingredients=ingredients_choisis,
        cuisson=cuisson,
        ajouter_emoji=ajouter_emoji,
        EMOJIS_INGREDIENTS=EMOJIS_INGREDIENTS,
        EMOJIS_CUISSONS=EMOJIS_CUISSONS
    )

@app.route('/commande/<commande_id>')
def get_commande(commande_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT ingredients, cuisson FROM commandes WHERE id = ?", (commande_id,))
    result = c.fetchone()
    conn.close()

    if result:
        ingredients_list = result[0].split(", ")
        return jsonify({"id": commande_id, "ingredients": ingredients_list, "cuisson": result[1]})
    return jsonify({"error": "Commande non trouvée."}), 404

@app.route('/commandes')
def afficher_commandes():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, ingredients, cuisson FROM commandes")
    results = c.fetchall()
    conn.close()
    return render_template("commandes.html",
        commandes=results,
        ajouter_emoji=ajouter_emoji,
        EMOJIS_INGREDIENTS=EMOJIS_INGREDIENTS,
        EMOJIS_CUISSONS=EMOJIS_CUISSONS
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
