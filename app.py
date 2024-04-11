import csv
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    with open('subscribers.csv', 'a', newline='') as csvfile:
        fieldnames = ['email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'email': email})
    return 'Subscribed successfully!'

if __name__ == '__main__':
    app.run(debug=True)