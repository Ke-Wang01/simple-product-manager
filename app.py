from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    price = db.Column(db.Float)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET"])
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    category = request.form["category"]
    price = float(request.form["price"])

    p = Product(name=name, category=category, price=price)
    db.session.add(p)
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    p = Product.query.get(id)
    db.session.delete(p)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)