from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'supersecretkey'

GETRAENKE = {
    'Bier': {'preis': 4.00, 'pfand': 2.00},
    'Softdrink': {'preis': 3.50, 'pfand': 2.00},
    'Wasser': {'preis': 3.00, 'pfand': 2.00},
    'Wein': {'preis': 5.00, 'pfand': 2.00},
    'Longdrink': {'preis': 8.00, 'pfand': 2.00}
}

@app.route('/')
def index():
    if 'bestellung' not in session:
        session['bestellung'] = {getraenk: {'menge': 0, 'pfand': 0} for getraenk in GETRAENKE}
    return render_template('index.html', getraenke=GETRAENKE, bestellung=session['bestellung'])

@app.route('/hinzufuegen/<getraenk>/<art>', methods=['POST'])
def hinzufuegen(getraenk, art):
    if getraenk in GETRAENKE:
        if art == 'getraenk':
            session['bestellung'][getraenk]['menge'] += 1
        elif art == 'pfand':
            session['bestellung'][getraenk]['pfand'] += 1
        session.modified = True
    return jsonify(session['bestellung'])

@app.route('/entfernen/<getraenk>/<art>', methods=['POST'])
def entfernen(getraenk, art):
    if getraenk in GETRAENKE:
        if art == 'getraenk' and session['bestellung'][getraenk]['menge'] > 0:
            session['bestellung'][getraenk]['menge'] -= 1
        elif art == 'pfand' and session['bestellung'][getraenk]['pfand'] > 0:
            session['bestellung'][getraenk]['pfand'] -= 1
        session.modified = True
    return jsonify(session['bestellung'])

@app.route('/berechnen', methods=['GET'])
def berechnen():
    gesamtpreis = 0
    pfandpreis = 0

    for getraenk, daten in session['bestellung'].items():
        gesamtpreis += daten['menge'] * GETRAENKE[getraenk]['preis']
        pfandpreis += daten['pfand'] * GETRAENKE[getraenk]['pfand']

    gesamtpreis += pfandpreis
    return render_template('ergebnis.html', gesamtpreis=gesamtpreis, pfandpreis=pfandpreis)

@app.route('/neue_bestellung', methods=['GET'])
def neue_bestellung():
    session['bestellung'] = {getraenk: {'menge': 0, 'pfand': 0} for getraenk in GETRAENKE}
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)
