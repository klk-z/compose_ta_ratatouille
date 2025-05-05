
# 🍲 Compose ta ratatouille

Application web en Python permettant de composer sa ratatouille, de choisir la cuisson, de passer commande et de noter le plat.

---

## 📦 Contenu du projet

- **Service 1 : ratatouille/**
  - Choix des ingrédients 🥒🍆🌶️
  - Choix de la cuisson (gratinée, mijotée, vapeur)
  - Enregistrement des commandes (SQLite)
  - Interface web avec Flask

- **Service 2 : notation/**
  - Notation des commandes sur 5 ⭐
  - Affichage de toutes les notes
  - Stockage en base SQLite

- **Déploiement Kubernetes :** fichiers dans le dossier `k8s/`  
  (Ingress, Deployments, Services)

---

## 🚀 Lancer le projet

1. **Builder les images Docker :**

```bash
docker build -t klkz/ratatouille:v1 ./ratatouille
docker build -t klkz/notation:v1 ./notation
```

2. **Démarrer Minikube et activer Ingress :**

```bash
minikube start --driver=docker
minikube addons enable ingress
```

3. **Déployer les services :**

```bash
kubectl apply -f k8s/
minikube tunnel
```

4. **Accéder à l'app :**
- `http://127.0.0.1/` → Composer une ratatouille  
- `http://127.0.0.1/notation` → Noter une commande

---

## 👤 Auteur

Projet réalisé par [klk-z] et [maze-debug] dans le cadre d’un projet universitaire.
