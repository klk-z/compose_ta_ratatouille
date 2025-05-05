# Utiliser une image officielle de Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Exposer le port utilisé par Flask
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]
