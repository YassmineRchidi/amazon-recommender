import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def __init__(self, max_users=500, max_items=500):
        self.df = pd.read_csv("amazon_reviews.csv", on_bad_lines='skip')

        # Nettoyage : garder seulement les colonnes utiles
        self.df = self.df[['userName', 'itemName', 'rating']]
        self.df.dropna(inplace=True)

        # Réduire la taille : ne garder que les max_users et max_items les plus fréquents
        top_users = self.df['userName'].value_counts().nlargest(max_users).index
        top_items = self.df['itemName'].value_counts().nlargest(max_items).index
        self.df = self.df[self.df['userName'].isin(top_users) & self.df['itemName'].isin(top_items)]

        self.prepare_matrix()
        self.compute_similarity()

    def prepare_matrix(self):
        self.user_item_matrix = self.df.pivot_table(index='userName', columns='itemName', values='rating').fillna(0)

    def compute_similarity(self):
        self.similarity_matrix = cosine_similarity(self.user_item_matrix)
        self.similarity_df = pd.DataFrame(self.similarity_matrix,
                                          index=self.user_item_matrix.index,
                                          columns=self.user_item_matrix.index)

    def recommend_items(self, user_name, num_recommendations=5):
        if user_name not in self.similarity_df.index:
            return []

        similar_users = self.similarity_df[user_name].sort_values(ascending=False)
        similar_users = similar_users.drop(user_name)  # Remove self
        top_user = similar_users.index[0]  # Most similar user

        user_ratings = self.user_item_matrix.loc[user_name]
        top_user_ratings = self.user_item_matrix.loc[top_user]

        # Find items rated by similar user but not yet rated by current user
        recommendations = top_user_ratings[user_ratings == 0].sort_values(ascending=False)
        return list(recommendations.head(num_recommendations).index)

    def get_users(self):
        return list(self.user_item_matrix.index)

    def get_items(self):
        return list(self.user_item_matrix.columns)
