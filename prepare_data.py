import pandas as pd

# Charger le fichier CSV brut
df = pd.read_csv("amazon_reviews.csv", encoding="utf-8", on_bad_lines='skip')

# Vérifier les premières colonnes disponibles
print("Colonnes détectées :", df.columns.tolist())

# Renommer les colonnes nécessaires si elles existent
# Exemple : 'reviewerName' -> 'userName', 'title' ou 'name' -> 'itemName', 'rating' ou 'overall' -> 'rating'
df_clean = df.rename(columns={
    'Amazon Customer': 'userName',
    'Toblerone Swiss Milk Chocolate Bar, Crunchy Salted Almond, 3.52 Ounce': 'itemName',
    '5.0': 'rating'  # à adapter si la colonne n'a pas ce nom
})

# Sélectionner seulement les colonnes utiles
try:
    df_small = df[['reviewerName', 'title', 'rating']].dropna()
    df_small.columns = ['userName', 'itemName', 'rating']
except:
    # Si les noms sont différents
    df_small = df.iloc[:, [0, 2, 10]]  # À adapter selon l'ordre réel : utilisateur, produit, note
    df_small.columns = ['userName', 'itemName', 'rating']

# Optionnel : réduire à un sous-ensemble
df_small = df_small.head(500)

# Sauvegarder dans un fichier simplifié
df_small.to_csv("ratings.csv", index=False)
print("✅ Fichier ratings.csv généré avec succès.")
