from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# Página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    rows = cols = None

    if request.method == 'POST':
        rows = int(request.form.get('rows'))
        cols = int(request.form.get('cols'))

    return render_template('index.html', rows=rows, cols=cols)

# Ruta para manejar las operaciones
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Obtener las dimensiones de las matrices
        rows = int(request.form['rows'])
        cols = int(request.form['cols'])

        # Crear la primera matriz
        matrix1 = np.zeros((rows, cols))

        for i in range(rows):
            for j in range(cols):
                matrix1[i, j] = float(request.form[f'matrix1_{i}_{j}'])

        # Determinar si se ha enviado una segunda matriz
        matrix2 = None
        if request.form.get(f'matrix2_0_0') is not None:  # Chequea si hay un valor en la segunda matriz
            matrix2 = np.zeros((rows, cols))
            for i in range(rows):
                for j in range(cols):
                    matrix2[i, j] = float(request.form.get(f'matrix2_{i}_{j}', 0))

        operation = request.form['operation']

        # Realizar la operación seleccionada
        if operation == 'sum':
            if matrix2 is not None:
                result = matrix1 + matrix2
            else:
                result = "Error: No se ha añadido la segunda matriz para realizar la suma."
        elif operation == 'subtraction':
            if matrix2 is not None:
                result = matrix1 - matrix2
            else:
                result = "Error: No se ha añadido la segunda matriz para realizar la resta."
        elif operation == 'multiplication':
            if matrix2 is not None and rows == cols:  # Multiplicación de matrices solo si son cuadradas
                result = np.dot(matrix1, matrix2)
            else:
                result = "Error: Para multiplicar matrices, deben ser cuadradas y debe haber dos matrices."
        elif operation == 'determinant':
            if rows == cols:  # El determinante solo es válido para matrices cuadradas
                result = np.linalg.det(matrix1)
            else:
                result = "El determinante solo se puede calcular para matrices cuadradas."
        else:
            result = "Operación no válida"

        return render_template('index.html', result=result, rows=rows, cols=cols)

    except Exception as e:
        return render_template('index.html', result="Error: " + str(e))

if __name__ == '__main__':
    app.run(debug=True)
