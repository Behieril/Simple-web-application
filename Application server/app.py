from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite база даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        city = request.form['city']
        birth_year = request.form['birth_year']

        new_user = User(first_name=first_name, last_name=last_name, city=city, birth_year=birth_year)

        with app.app_context():
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_user.html')

@app.route('/search_user', methods=['GET', 'POST'])
def search_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        user = User.query.filter_by(first_name=first_name, last_name=last_name).first()

        if user:
            return render_template('user_info.html', user=user)
        else:
            return render_template('user_not_found.html')

    return render_template('search_user.html')



@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.city = request.form['city']
        user.birth_year = request.form['birth_year']

        try:
            with app.app_context():
                db.session.merge(user)
                db.session.commit()
        except Exception as e:
            print(f"Error: {str(e)}")
            db.session.rollback()

        return redirect(url_for('index'))

    return render_template('edit_user.html', user=user)



@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    return redirect(url_for('index'))

@app.route('/all_users')
def all_users():
    users = User.query.all()
    return render_template('all_users.html', users=users)

@app.route('/user_info/<int:user_id>')
def user_info(user_id):
    user = User.query.get(user_id)
    return render_template('user_info.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
