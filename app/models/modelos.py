from app import db

class Pasajero(db.Model):
    __tablename__ = 'pasajero'

    id_pasajero = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))

    boletos = db.relationship('Boleto', back_populates='pasajero')


class Boleto(db.Model):
    __tablename__ = 'boleto'

    numero_boleto = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    precio = db.Column(db.Numeric(10, 2))
    hora = db.Column(db.Time)

    id_pasajero = db.Column(db.Integer, db.ForeignKey('pasajero.id_pasajero'))
    numero_vuelo = db.Column(db.Integer, db.ForeignKey('vuelo.numero_vuelo'))

    pasajero = db.relationship('Pasajero', back_populates='boletos')
    vuelo = db.relationship('Vuelo', back_populates='boletos')


class Vuelo(db.Model):
    __tablename__ = 'vuelo'

    numero_vuelo = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)

    codigo_destino = db.Column(db.Integer, db.ForeignKey('destino.codigo_destino'))
    numero_avion = db.Column(db.Integer, db.ForeignKey('avion.numero_avion'))
    numero_empleado = db.Column(db.Integer, db.ForeignKey('empleado.numero_empleado'))

    destino = db.relationship('Destino', back_populates='vuelos')
    avion = db.relationship('Avion', back_populates='vuelos')
    empleado = db.relationship('Empleado', back_populates='vuelos')
    boletos = db.relationship('Boleto', back_populates='vuelo')


class Destino(db.Model):
    __tablename__ = 'destino'

    codigo_destino = db.Column(db.Integer, primary_key=True)
    ciudad = db.Column(db.String(50))
    pais = db.Column(db.String(50))

    vuelos = db.relationship('Vuelo', back_populates='destino')


class Avion(db.Model):
    __tablename__ = 'avion'

    numero_avion = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))

    vuelos = db.relationship('Vuelo', back_populates='avion')


class Empleado(db.Model):
    __tablename__ = 'empleado'

    numero_empleado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellido = db.Column(db.String(50))
    fecha_ingreso = db.Column(db.Date)

    vuelos = db.relationship('Vuelo', back_populates='empleado')
    piloto = db.relationship('Piloto', uselist=False, back_populates='empleado')


class Piloto(db.Model):
    __tablename__ = 'piloto'

    numero_empleado = db.Column(db.Integer, db.ForeignKey('empleado.numero_empleado'), primary_key=True)
    calificacion = db.Column(db.String(50))
    licencia = db.Column(db.String(50))

    empleado = db.relationship('Empleado', back_populates='piloto')
