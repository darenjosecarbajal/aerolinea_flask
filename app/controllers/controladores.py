from flask import Blueprint, request, jsonify
from flask import render_template, redirect, url_for
from app.models.modelos import db, Pasajero, Boleto, Vuelo, Destino, Avion, Empleado, Piloto
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

# --------------------------
# PASAJEROS
# --------------------------

@main_bp.route('/pasajeros')
def mostrar_pasajeros():
    pasajeros = Pasajero.query.all()
    return render_template('pasajeros.html', pasajeros=pasajeros)

@main_bp.route('/pasajeros/nuevo', methods=['GET', 'POST'])
def nuevo_pasajero():
    if request.method == 'POST':
        data = request.form
        pasajero = Pasajero(
            nombre=data['nombre'],
            apellido=data['apellido'],
            correo=data['correo'],
            telefono=data['telefono']
        )
        db.session.add(pasajero)
        db.session.commit()
        return redirect(url_for('main.mostrar_pasajeros'))
    return render_template('crear_pasajero.html')

@main_bp.route('/pasajeros/editar/<int:id>', methods=['GET', 'POST'])
def editar_pasajero(id):
    pasajero = Pasajero.query.get_or_404(id)
    if request.method == 'POST':
        pasajero.nombre = request.form['nombre']
        pasajero.apellido = request.form['apellido']
        pasajero.correo = request.form['correo']
        pasajero.telefono = request.form['telefono']
        db.session.commit()
        return redirect(url_for('main.mostrar_pasajeros'))
    return render_template('editar_pasajero.html', pasajero=pasajero)

@main_bp.route('/pasajeros/eliminar/<int:id>', methods=['POST'])
def eliminar_pasajero(id):
    pasajero = Pasajero.query.get_or_404(id)
    db.session.delete(pasajero)
    db.session.commit()
    return redirect(url_for('main.mostrar_pasajeros'))

# --------------------------
# BOLETOS
# --------------------------

@main_bp.route('/boletos/lista')
def mostrar_boletos():
    boletos = Boleto.query.all()
    return render_template('boletos.html', boletos=boletos)

@main_bp.route('/boletos/nuevo', methods=['GET', 'POST'])
def nuevo_boleto():
    pasajeros = Pasajero.query.all()
    vuelos = Vuelo.query.all()

    if not pasajeros or not vuelos:
        return render_template('crear_boleto.html', error=True, pasajeros=pasajeros, vuelos=vuelos)

    if request.method == 'POST':
        boleto = Boleto(
            fecha=request.form['fecha'],
            hora=request.form['hora'],
            precio=request.form['precio'],
            id_pasajero=request.form['id_pasajero'],
            numero_vuelo=request.form['numero_vuelo']
        )
        db.session.add(boleto)
        db.session.commit()
        return redirect(url_for('main.mostrar_boletos'))

    return render_template('crear_boleto.html', error=False, pasajeros=pasajeros, vuelos=vuelos)

@main_bp.route('/boletos/editar/<int:id>', methods=['GET', 'POST'])
def editar_boleto(id):
    boleto = Boleto.query.get_or_404(id)
    if request.method == 'POST':
        boleto.fecha = request.form['fecha']
        boleto.hora = request.form['hora']
        boleto.precio = request.form['precio']
        boleto.id_pasajero = request.form['id_pasajero']
        boleto.numero_vuelo = request.form['numero_vuelo']
        db.session.commit()
        return redirect(url_for('main.mostrar_boletos'))

    pasajeros = Pasajero.query.all()
    vuelos = Vuelo.query.all()
    return render_template('editar_boleto.html', boleto=boleto, pasajeros=pasajeros, vuelos=vuelos)

@main_bp.route('/boletos/eliminar/<int:id>', methods=['POST'])
def eliminar_boleto(id):
    boleto = Boleto.query.get_or_404(id)
    db.session.delete(boleto)
    db.session.commit()
    return redirect(url_for('main.mostrar_boletos'))

# --------------------------
# VUELOS
# --------------------------

@main_bp.route('/vuelos/lista')
def mostrar_vuelos():
    vuelos = Vuelo.query.all()
    return render_template('vuelos.html', vuelos=vuelos)

@main_bp.route('/vuelos/nuevo', methods=['GET', 'POST'])
def nuevo_vuelo():
    destinos = Destino.query.all()
    aviones = Avion.query.all()
    empleados = Empleado.query.all()

    if not destinos or not aviones or not empleados:
        return render_template('crear_vuelo.html', error=True, destinos=destinos, aviones=aviones, empleados=empleados)

    if request.method == 'POST':
        vuelo = Vuelo(
            fecha=request.form['fecha'],
            hora=request.form['hora'],
            codigo_destino=request.form['codigo_destino'],
            numero_avion=request.form['numero_avion'],
            numero_empleado=request.form['numero_empleado']
        )
        db.session.add(vuelo)
        db.session.commit()
        return redirect(url_for('main.mostrar_vuelos'))

    return render_template('crear_vuelo.html', error=False, destinos=destinos, aviones=aviones, empleados=empleados)

@main_bp.route('/vuelos/editar/<int:id>', methods=['GET', 'POST'])
def editar_vuelo(id):
    vuelo = Vuelo.query.get_or_404(id)
    if request.method == 'POST':
        vuelo.fecha = request.form['fecha']
        vuelo.hora = request.form['hora']
        vuelo.codigo_destino = request.form['codigo_destino']
        vuelo.numero_avion = request.form['numero_avion']
        vuelo.numero_empleado = request.form['numero_empleado']
        db.session.commit()
        return redirect(url_for('main.mostrar_vuelos'))
    return render_template('editar_vuelo.html', vuelo=vuelo)

@main_bp.route('/vuelos/eliminar/<int:id>', methods=['POST'])
def eliminar_vuelo(id):
    vuelo = Vuelo.query.get_or_404(id)
    db.session.delete(vuelo)
    db.session.commit()
    return redirect(url_for('main.mostrar_vuelos'))

# --------------------------
# DESTINOS
# --------------------------

@main_bp.route('/destinos/lista')
def mostrar_destinos():
    destinos = Destino.query.all()
    return render_template('destinos.html', destinos=destinos)

@main_bp.route('/destinos/nuevo', methods=['GET', 'POST'])
def nuevo_destino():
    if request.method == 'POST':
        destino = Destino(
            ciudad=request.form['ciudad'],
            pais=request.form['pais']
        )
        db.session.add(destino)
        db.session.commit()
        return redirect(url_for('main.mostrar_destinos'))
    return render_template('crear_destino.html')

@main_bp.route('/destinos/editar/<int:id>', methods=['GET', 'POST'])
def editar_destino(id):
    destino = Destino.query.get_or_404(id)
    if request.method == 'POST':
        destino.ciudad = request.form['ciudad']
        destino.pais = request.form['pais']
        db.session.commit()
        return redirect(url_for('main.mostrar_destinos'))
    return render_template('editar_destino.html', destino=destino)

@main_bp.route('/destinos/eliminar/<int:id>', methods=['POST'])
def eliminar_destino(id):
    destino = Destino.query.get_or_404(id)
    db.session.delete(destino)
    db.session.commit()
    return redirect(url_for('main.mostrar_destinos'))

# --------------------------
# AVIONES
# --------------------------

@main_bp.route('/aviones/lista')
def mostrar_aviones():
    aviones = Avion.query.all()
    return render_template('aviones.html', aviones=aviones)

@main_bp.route('/aviones/nuevo', methods=['GET', 'POST'])
def nuevo_avion():
    if request.method == 'POST':
        avion = Avion(tipo=request.form['tipo'])
        db.session.add(avion)
        db.session.commit()
        return redirect(url_for('main.mostrar_aviones'))
    return render_template('crear_avion.html')

@main_bp.route('/aviones/editar/<int:id>', methods=['GET', 'POST'])
def editar_avion(id):
    avion = Avion.query.get_or_404(id)
    if request.method == 'POST':
        avion.tipo = request.form['tipo']
        db.session.commit()
        return redirect(url_for('main.mostrar_aviones'))
    return render_template('editar_avion.html', avion=avion)

@main_bp.route('/aviones/eliminar/<int:id>', methods=['POST'])
def eliminar_avion(id):
    avion = Avion.query.get_or_404(id)
    db.session.delete(avion)
    db.session.commit()
    return redirect(url_for('main.mostrar_aviones'))

# --------------------------
# EMPLEADOS
# --------------------------

@main_bp.route('/empleados/lista')
def mostrar_empleados():
    empleados = Empleado.query.all()
    return render_template('empleados.html', empleados=empleados)

@main_bp.route('/empleados/nuevo', methods=['GET', 'POST'])
def nuevo_empleado():
    if request.method == 'POST':
        empleado = Empleado(
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            fecha_ingreso=datetime.strptime(request.form['fecha_ingreso'], "%Y-%m-%d").date()
        )
        db.session.add(empleado)
        db.session.commit()
        return redirect(url_for('main.mostrar_empleados'))

    return render_template('crear_empleado.html')

@main_bp.route('/empleados/editar/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    if request.method == 'POST':
        empleado.nombre = request.form['nombre']
        empleado.apellido = request.form['apellido']
        empleado.fecha_ingreso = datetime.strptime(request.form['fecha_ingreso'], "%Y-%m-%d").date()
        db.session.commit()
        return redirect(url_for('main.mostrar_empleados'))
    return render_template('editar_empleado.html', empleado=empleado)

@main_bp.route('/empleados/eliminar/<int:id>', methods=['POST'])
def eliminar_empleado(id):
    empleado = Empleado.query.get_or_404(id)
    db.session.delete(empleado)
    db.session.commit()
    return redirect(url_for('main.mostrar_empleados'))

# --------------------------
# PILOTOS
# --------------------------

@main_bp.route('/pilotos/lista')
def mostrar_pilotos():
    pilotos = Piloto.query.all()
    return render_template('pilotos.html', pilotos=pilotos)

@main_bp.route('/pilotos/nuevo', methods=['GET', 'POST'])
def nuevo_piloto():
    empleados = Empleado.query.all()

    if not empleados:
        return render_template('crear_piloto.html', error=True, empleados=empleados)

    if request.method == 'POST':
        piloto = Piloto(
            numero_empleado=request.form['numero_empleado'],
            calificacion=request.form['calificacion'],
            licencia=request.form['licencia']
        )
        db.session.add(piloto)
        db.session.commit()
        return redirect(url_for('main.mostrar_pilotos'))

    return render_template('crear_piloto.html', error=False, empleados=empleados)

@main_bp.route('/pilotos/editar/<int:id>', methods=['GET', 'POST'])
def editar_piloto(id):
    piloto = Piloto.query.get_or_404(id)
    if request.method == 'POST':
        piloto.calificacion = request.form['calificacion']
        piloto.licencia = request.form['licencia']
        db.session.commit()
        return redirect(url_for('main.mostrar_pilotos'))
    return render_template('editar_piloto.html', piloto=piloto)

@main_bp.route('/pilotos/eliminar/<int:id>', methods=['POST'])
def eliminar_piloto(id):
    piloto = Piloto.query.get_or_404(id)
    db.session.delete(piloto)
    db.session.commit()
    return redirect(url_for('main.mostrar_pilotos'))