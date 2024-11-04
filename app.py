from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Cambia el backend a Agg para evitar problemas de tkinter
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    summary_html = None  # Inicializar summary_html
    graph_url = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_excel(file)
            df.columns = df.columns.str.strip()  # Elimina espacios en blanco de los nombres de las columnas

            # Imprimir los nombres de las columnas para verificación
            print(df.columns)

            # Filtramos las primeras 3 columnas y convertimos a HTML
            data = df.iloc[:, :3].head().to_html(classes='data', header="true", index=False)

            # Agrupar por 'FECHA DE LA FACTURA' y sumar 'IMPORTE TOTAL DE LA VENTA'
            if 'FECHA DE LA FACTURA' in df.columns and 'IMPORTE TOTAL DE LA VENTA' in df.columns:
                df_grouped = df.groupby('FECHA DE LA FACTURA')['IMPORTE TOTAL DE LA VENTA'].sum().reset_index()

                # Generar resumen estadístico
                summary = df_grouped['IMPORTE TOTAL DE LA VENTA'].describe().to_frame().T  # Transponemos para mejor visualización
                summary_html = summary.to_html(classes='data', header="true", index=False)  # Convertimos a HTML

                plt.figure(figsize=(10, 5))
                plt.plot(df_grouped['FECHA DE LA FACTURA'], df_grouped['IMPORTE TOTAL DE LA VENTA'], marker='o', linestyle='-', color='#FF6F61', linewidth=2, markersize=5)
                plt.title('Ventas por Día', fontsize=16, color='#D45D79')
                plt.xlabel('Fecha', fontsize=12, color='#6CA0B2')
                plt.ylabel('Importe Total de la Venta', fontsize=12, color='#6CA0B2')
                plt.xticks(rotation=45, fontsize=10)
                plt.yticks(fontsize=10)
                plt.grid(color='#E2E2E2', linestyle='--', linewidth=0.5)
                plt.fill_between(df_grouped['FECHA DE LA FACTURA'], df_grouped['IMPORTE TOTAL DE LA VENTA'], color='#FFABAB', alpha=0.3)
                plt.tight_layout()

                # Guardamos la gráfica en un archivo
                graph_path = os.path.join('static', 'grafica.png')
                plt.savefig(graph_path)
                plt.close()

                graph_url = graph_path  # URL de la gráfica

    return render_template('index.html', data=data, summary=summary_html, graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True)
