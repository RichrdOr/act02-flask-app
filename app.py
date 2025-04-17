from flask import Flask
from datetime import datetime
import requests 
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    url = requests.get("https://gist.githubusercontent.com/reroes/502d11c95f1f8a17d300ece914464c57/raw/872172ebb60e22e95baf8f50e2472551" \
    "f49311ff/gistfile1.txt")
    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')

    table = soup.find('table')

    rows = table.find_all('tr')

    datos = []

    for i, row in enumerate(rows):
        columnas = row.find_all(['th', 'td'])
        fila = [col.text.strip() for col in columnas]
        datos.append(fila) 
    
    df = pd.DataFrame(datos[1:], columns=datos[0])

    df_filtrado = df[df['Cédula'].astype(str).str.startswith(('3', '4', '5', '7'))]

    tabla_html = df_filtrado.to_html(classes="table table-bordered", index=False)

    return render_template_string(f"""
        <html>
        <head>
            <title>Tabla desde BeautifulSoup</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        </head>
        <body class="p-4">
            <h2>Personas con ID que empiezan en 3, 4, 5 o 7 usando BeautifulSoup</h2>
            {tabla_html}
        </body>
        </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)