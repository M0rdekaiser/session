from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'


# Función para inicializar la lista de seminarios si no existe
def inicializar_sesion():
    if 'seminarios' not in session:
        session['seminarios'] = []


# Función para generar un nuevo ID para el inscrito
def generar_id():
    inicializar_sesion()
    seminarios = session['seminarios']
    if seminarios:
        return max(item['id'] for item in seminarios) + 1
    return 1


# Función auxiliar para obtener un inscrito por ID
def obtener_inscrito(id):
    seminarios = session.get('seminarios', [])
    return next((c for c in seminarios if c['id'] == id), None)


# Ruta principal (index), lista de inscritos
@app.route("/")
def index():
    inicializar_sesion()
    seminarios = session['seminarios']
    return render_template('index.html', seminarios=seminarios)


# Ruta para agregar un nuevo inscrito
@app.route("/nuevo", methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        # Obtener datos del formulario
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        turno = request.form['turno']
        disponibles = request.form.getlist('disponibles')
        disponibles_texto = ', '.join(disponibles)

        # Crear un nuevo inscrito
        nuevo_inscrito = {
            'id': generar_id(),
            'fecha': fecha,
            'nombre': nombre,
            'apellidos': apellidos,
            'turno': turno,
            'disponible': disponibles_texto
        }

        # Añadir el inscrito a la sesión
        session['seminarios'].append(nuevo_inscrito)
        session.modified = True
        return redirect(url_for('index'))

    return render_template("nuevo.html")


# Ruta para editar un inscrito existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    inscrito = obtener_inscrito(id)
    if not inscrito:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Actualizar datos del inscrito
        inscrito['fecha'] = request.form['fecha']
        inscrito['nombre'] = request.form['nombre']
        inscrito['apellidos'] = request.form['apellidos']
        inscrito['turno'] = request.form['turno']
        disponibles = request.form.getlist('disponibles')
        inscrito['disponible'] = ', '.join(disponibles)

        session.modified = True
        return redirect(url_for('index'))

    return render_template('editar.html', inscrito=inscrito)


# Ruta para eliminar un inscrito
@app.route("/eliminar/<int:id>", methods=['POST'])
def eliminar(id):
    inscrito = obtener_inscrito(id)
    if inscrito:
        session['seminarios'].remove(inscrito)
        session.modified = True
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=5017)
