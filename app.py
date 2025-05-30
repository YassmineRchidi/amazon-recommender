from flask import Flask, render_template, request
from recommender import Recommender

app = Flask(__name__)
rec = Recommender()

@app.route('/', methods=['GET', 'POST'])
def index():
    users = rec.get_users()
    recommendations = []

    if request.method == 'POST':
        user_name = request.form['user']
        recommendations = rec.recommend_items(user_name)

    return render_template('index.html', users=users, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
