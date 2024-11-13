from application import app, db
from flask import render_template, flash, redirect, url_for
from application.form import UserInputForm
from application.models import IncomeExpenses
import json

@app.route("/")
@app.route("/home")
def home():
    print(url_for('static', filename='images/logo.webp'))
    return render_template('home.html')

@app.route("/reports")
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template("index.html", title='index', entries=entries)

@app.route("/layout")
def layout():
    form = UserInputForm()
    return render_template("layout.html", title='layout', form=form)

@app.route("/add", methods=["GET", "POST"])
def add_expense():
    form = UserInputForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type=form.type.data, amount=form.amount.data, category=form.category.data)
        db.session.add(entry)
        db.session.commit()
        flash("Successful entry", 'success')
        return redirect(url_for('index'))
    return render_template("add.html", title='add', form=form)

@app.route('/delete/<int:entry_id>')
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Deletion was success", 'success')
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    # Query for total income vs expenses
    income_vs_expenses = db.session.query(
        db.func.sum(IncomeExpenses.amount).label('total_amount'),
        IncomeExpenses.type
    ).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()

    # Query for expenditure over time
    dates = db.session.query(
        db.func.sum(IncomeExpenses.amount).label('total_amount'),
        IncomeExpenses.date
    ).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    # Prepare data for the charts
    income_expenses = [total_amount for total_amount, _ in income_vs_expenses]
    
    over_time_expenditure = [amount for amount, _ in dates]
    dates_labels = [date.strftime("%m-%d-%Y") for _, date in dates]

    # Pass the data to the template using json.dumps and |safe in the template
    return render_template("dashboard.html",
                           income_vs_expenses=json.dumps(income_expenses),
                           over_time_expenditure=json.dumps(over_time_expenditure),
                           dates_label=json.dumps(dates_labels))

