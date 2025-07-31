from flask import Blueprint, request, jsonify
from flask import render_template, redirect, url_for
from app.models.modelos import db, Pasajero, Boleto, Vuelo, Destino, Avion, Empleado, Piloto

main_bp = Blueprint('main', __name__)

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

@main_bp.route('/pasajeros', methods=['GET'])
def get_pasajeros():
    pasajeros = Pasajero.query.all()
    return jsonify([{
        "id": p.id_pasajero,
        "nombre": p.nombre,
        "apellido": p.apellido,
        "correo": p.correo,
        "telefono": p.telefono
    } for p in pasajeros])

@main_bp.route('/pasajeros', methods=['POST'])
def create_pasajero():
    data = request.get_json()
    nuevo = Pasajero(**data)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Pasajero creado"}), 201

@main_bp.route('/pasajeros/<int:id>', methods=['GET'])
def get_pasajero(id):
    p = Pasajero.query.get_or_404(id)
    return jsonify({
        "id": p.id_pasajero,
        "nombre": p.nombre,
        "apellido": p.apellido,
        "correo": p.correo,
        "telefono": p.telefono
    })

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

@main_bp.route('/boletos', methods=['GET'])
def get_boletos():
    return jsonify([{
        "numero": b.numero_boleto,
        "fecha": str(b.fecha),
        "hora": str(b.hora),
        "precio": float(b.precio),
        "id_pasajero": b.id_pasajero,
        "numero_vuelo": b.numero_vuelo
    } for b in Boleto.query.all()])

@main_bp.route('/boletos', methods=['POST'])
def create_boleto():
    data = request.get_json()
    nuevo = Boleto(**data)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Boleto creado"}), 201

@main_bp.route('/boletos/<int:id>', methods=['PUT'])
def update_boleto(id):
    b = Boleto.query.get_or_404(id)
    for k, v in request.get_json().items():
        setattr(b, k, v)
    db.session.commit()
    return jsonify({"mensaje": "Boleto actualizado"})

@main_bp.route('/boletos/<int:id>', methods=['DELETE'])
def delete_boleto(id):
    b = Boleto.query.get_or_404(id)
    db.session.delete(b)
    db.session.commit()
    return jsonify({"mensaje": "Boleto eliminado"})

# --------------------------
# VUELOS
# --------------------------

@main_bp.route('/vuelos', methods=['GET'])
def get_vuelos():
    return jsonify([{
        "numero": v.numero_vuelo,
        "fecha": str(v.fecha),
        "hora": str(v.hora),
        "codigo_destino": v.codigo_destino,
        "numero_avion": v.numero_avion,
        "numero_empleado": v.numero_empleado
    } for v in Vuelo.query.all()])

@main_bp.route('/vuelos', methods=['POST'])
def create_vuelo():
    data = request.get_json()
    nuevo = Vuelo(**data)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Vuelo creado"}), 201

@main_bp.route('/vuelos/<int:id>', methods=['PUT'])
def update_vuelo(id):
    v = Vuelo.query.get_or_404(id)
    for k, v_ in request.get_json().items():
        setattr(v, k, v_)
    db.session.commit()
    return jsonify({"mensaje": "Vuelo actualizado"})

@main_bp.route('/vuelos/<int:id>', methods=['DELETE'])
def delete_vuelo(id):
    v = Vuelo.query.get_or_404(id)
    db.session.delete(v)
    db.session.commit()
    return jsonify({"mensaje": "Vuelo eliminado"})

# --------------------------
# DESTINOS
# --------------------------

@main_bp.route('/destinos', methods=['GET'])
def get_destinos():
    return jsonify([{
        "codigo": d.codigo_destino,
        "ciudad": d.ciudad,
        "pais": d.pais
    } for d in Destino.query.all()])

@main_bp.route('/destinos', methods=['POST'])
def create_destino():
    d = Destino(**request.get_json())
    db.session.add(d)
    db.session.commit()
    return jsonify({"mensaje": "Destino creado"}), 201

@main_bp.route('/destinos/<int:id>', methods=['PUT'])
def update_destino(id):
    d = Destino.query.get_or_404(id)
    for k, v in request.get_json().items():
        setattr(d, k, v)
    db.session.commit()
    return jsonify({"mensaje": "Destino actualizado"})

@main_bp.route('/destinos/<int:id>', methods=['DELETE'])
def delete_destino(id):
    d = Destino.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({"mensaje": "Destino eliminado"})

# --------------------------
# AVIONES
# --------------------------

@main_bp.route('/aviones', methods=['GET'])
def get_aviones():
    return jsonify([{
        "numero": a.numero_avion,
        "tipo": a.tipo
    } for a in Avion.query.all()])

@main_bp.route('/aviones', methods=['POST'])
def create_avion():
    a = Avion(**request.get_json())
    db.session.add(a)
    db.session.commit()
    return jsonify({"mensaje": "Avión creado"}), 201

@main_bp.route('/aviones/<int:id>', methods=['PUT'])
def update_avion(id):
    a = Avion.query.get_or_404(id)
    for k, v in request.get_json().items():
        setattr(a, k, v)
    db.session.commit()
    return jsonify({"mensaje": "Avión actualizado"})

@main_bp.route('/aviones/<int:id>', methods=['DELETE'])
def delete_avion(id):
    a = Avion.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    return jsonify({"mensaje": "Avión eliminado"})

# --------------------------
# EMPLEADOS
# --------------------------

@main_bp.route('/empleados', methods=['GET'])
def get_empleados():
    return jsonify([{
        "numero": e.numero_empleado,
        "nombre": e.nombre,
        "apellido": e.apellido,
        "fecha_ingreso": str(e.fecha_ingreso)
    } for e in Empleado.query.all()])

@main_bp.route('/empleados', methods=['POST'])
def create_empleado():
    e = Empleado(**request.get_json())
    db.session.add(e)
    db.session.commit()
    return jsonify({"mensaje": "Empleado creado"}), 201

@main_bp.route('/empleados/<int:id>', methods=['PUT'])
def update_empleado(id):
    e = Empleado.query.get_or_404(id)
    for k, v in request.get_json().items():
        setattr(e, k, v)
    db.session.commit()
    return jsonify({"mensaje": "Empleado actualizado"})

@main_bp.route('/empleados/<int:id>', methods=['DELETE'])
def delete_empleado(id):
    e = Empleado.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    return jsonify({"mensaje": "Empleado eliminado"})

# --------------------------
# PILOTOS
# --------------------------

@main_bp.route('/pilotos', methods=['GET'])
def get_pilotos():
    return jsonify([{
        "numero_empleado": p.numero_empleado,
        "calificacion": p.calificacion,
        "licencia": p.licencia
    } for p in Piloto.query.all()])

@main_bp.route('/pilotos', methods=['POST'])
def create_piloto():
    p = Piloto(**request.get_json())
    db.session.add(p)
    db.session.commit()
    return jsonify({"mensaje": "Piloto creado"}), 201

@main_bp.route('/pilotos/<int:id>', methods=['PUT'])
def update_piloto(id):
    p = Piloto.query.get_or_404(id)
    for k, v in request.get_json().items():
        setattr(p, k, v)
    db.session.commit()
    return jsonify({"mensaje": "Piloto actualizado"})

@main_bp.route('/pilotos/<int:id>', methods=['DELETE'])
def delete_piloto(id):
    p = Piloto.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"mensaje": "Piloto eliminado"})
