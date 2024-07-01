from flask import Flask, request, render_template
app = Flask(__name__)
from logic.data_managment import PartyOrganizer

organizer = PartyOrganizer()

@app.route('/')
def index():
    return render_template('index.html', organizer=organizer)

@app.route('/add_guest', methods=['POST'])
def add_guest():
    name = request.form['name']
    id_number = request.form['id_number']
    message = organizer.add_guest(name, id_number)
    return render_template('index.html', organizer=organizer, message=message)

@app.route('/mark_entered', methods=['POST'])
def mark_entered():
    id_number = request.form['id_number']
    message = organizer.mark_as_entered(id_number)
    return render_template('index.html', organizer=organizer, message=message)

@app.route('/confirm_attendance', methods=['POST'])
def confirm_attendance():
    id_number = request.form['id_number']
    message = organizer.confirm_attendance(id_number)
    return render_template('index.html', organizer=organizer, message=message)

@app.route('/generate_report')
def generate_report():
    report = organizer.generate_report()
    return render_template('report.html', report=report)

if __name__ == '__main__':
    app.run(debug=True, port=1231)