# Utilise une image Python officielle comme image de base
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers de l'application dans le conteneur
COPY requirements.txt ./
COPY extroverse.py ./

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Expose le port
EXPOSE 8080

# Commande par défaut pour lancer l'application
CMD ["python", "extroverse.py"]
