from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import smtplib
import os

MY_EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("EMAIL_PASS")
CHOICES = ("Yes", "No")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL",  'sqlite:///cafes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Bootstrap(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Cafe Location on Google Maps(URL)', validators=[DataRequired(), URL()])
    img_url = StringField('Cafe Place Picture(URL)', validators=[DataRequired(), URL()])
    location = StringField('Cafe Location', validators=[DataRequired()])
    seats = StringField('Total Seats Available', validators=[DataRequired()])
    coffee_price = StringField('Average Coffee Price', validators=[DataRequired()])
    has_sockets = SelectField('Power Sockets Availability', choices=CHOICES, validators=[DataRequired()])
    has_wifi = SelectField('Wifi Availability', choices=CHOICES, validators=[DataRequired()])
    has_toilet = SelectField('Toilet Availability', choices=CHOICES, validators=[DataRequired()])
    can_take_calls = SelectField('Calls Availability', choices=CHOICES, validators=[DataRequired()])
    submit = SubmitField('Submit')


cafes = Cafe.query.all()


@app.route("/")
def home():
    return render_template("index.html", all_cafes=cafes)


@app.route("/cafe/<int:index>")
def cafe(index):
    requested_cafe = None
    for cafe_review in cafes:
        if cafe_review.id == index:
            requested_cafe = cafe_review
    return render_template("cafe.html", cafe=requested_cafe)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        print(f"{name}\n{email}\n{message}")

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=f"Subject:New Message\n\n"
                                    f"Name: {name}\n"
                                    f"Email address: {email}\n"
                                    f"Message: {message}")
        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/add-cafe', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if request.method == "POST":
        name = request.form['name']
        map_url = request.form['map_url']
        img_url = request.form['img_url']
        location = request.form['location']
        seats = request.form['seats']
        coffee_price = request.form['coffee_price']
        has_sockets = request.form['has_sockets']
        has_wifi = request.form['has_wifi']
        has_toilet = request.form['has_toilet']
        can_take_calls = request.form['can_take_calls']

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=MY_EMAIL,
                                msg=f"Subject:Cafe Suggestion\n\n"
                                    f"Name: {name}\n"
                                    f"Map: {map_url}\n"
                                    f"Location: {location}\n"
                                    f"Image: {img_url}\n"
                                    f"Seats: {seats}\n"
                                    f"Ave. Coffee Price: {coffee_price}\n"
                                    f"Socket Availability: {has_sockets}\n"
                                    f"Wi-Fi Availability: {has_wifi}\n"
                                    f"Toilet Availability: {has_toilet}\n"
                                    f"Calls Availability: {can_take_calls}\n".encode('utf-8'))
        return render_template("add-cafe.html", form=form, suggested=True)

    return render_template("add-cafe.html", form=form, suggested=False)


# @app.route('/delete/<int:index>')
# def delete(index):
#     cafe_to_delete = Cafe.query.get(index)
#     db.session.delete(cafe_to_delete)
#     db.session.commit()
#     return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()