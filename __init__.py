from flask import Flask, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import requests  # Ajouter l'import pour faire la requête à l'API GitHub
import sqlite3


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html') 

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion de Kelvin en °C
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route("/donut/")
def mondonut():
    return render_template("donut.html")

# Route pour récupérer les commits depuis l'API GitHub
@app.route('/get-commits/')
def get_commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    # Extraire les minutes de chaque commit
    commits_by_minute = {}
    for commit in commits_data:
        commit_date_str = commit['commit']['author']['date']
        commit_date = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')
        minute = commit_date.minute

        if minute in commits_by_minute:
            commits_by_minute[minute] += 1
        else:
            commits_by_minute[minute] = 1

    return jsonify(commits_by_minute=commits_by_minute)

# Route pour afficher le graphique des commits
@app.route("/commits/")
def commits():
    return render_template("commits.html")

if __name__ == "__main__":
    app.run(debug=True)
