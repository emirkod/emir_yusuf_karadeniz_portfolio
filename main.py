# Import
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    message = db.Column(db.Text)

# ✅ Veritabanı tablosu (silmeden oluşturur)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def process_form():
    name = request.form.get('name', 'Anonim')
    email = request.form.get('email')
    message = request.form.get('message') or request.form.get('text')

    if email and message:
        new_entry = FormData(name=name, email=email, message=message)
        db.session.add(new_entry)
        db.session.commit()

    return redirect('/')

# Kayıtlı form verilerini gösterecek sayfa
@app.route('/data')
def show_data():
    all_data = FormData.query.all()  # Tüm verileri getirir
    return render_template('data.html', data=all_data)

if __name__ == "__main__":
    app.run(debug=True)