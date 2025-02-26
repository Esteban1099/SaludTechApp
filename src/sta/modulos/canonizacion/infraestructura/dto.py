from src.sta.config.db import db

class DemografiaDTO(db.Model):
    __tablename__ = "demografias_canonizadas"
    id = db.Column(db.String, primary_key=True)
    edad = db.Column(db.Integer, nullable=False)
    grupo_edad = db.Column(db.String, nullable=False)
    sexo = db.Column(db.String, nullable=False)
    etnicidad = db.Column(db.String, nullable=False)

    diagnostico_id = db.Column(db.String, db.ForeignKey('diagnosticos_canonizados.id', ondelete='CASCADE'))
    diagnostico = db.relationship("DiagnosticoDTO", back_populates="demografia", uselist=False)

class DiagnosticoDTO(db.Model):
    __tablename__ = "diagnosticos_canonizados"
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)

    imagen_canonizada_id = db.Column(db.String, db.ForeignKey('imagenes_canonizadas.id', ondelete='CASCADE'), unique=True)
    imagen_canonizada = db.relationship("ImagenCanonizadaDTO", back_populates="diagnostico", uselist=False)

    demografia = db.relationship("DemografiaDTO", back_populates="diagnostico", uselist=False)
    atributos = db.relationship("AtributoDTO", back_populates="diagnostico", cascade="all, delete-orphan")

class RegionAnatomicaDTO(db.Model):
    __tablename__ = "regiones_anatomicas_canonizadas"
    id = db.Column(db.String, primary_key=True)
    categoria = db.Column(db.String, nullable=False)
    especificacion = db.Column(db.String, nullable=False)

    imagen_canonizada_id = db.Column(db.String, db.ForeignKey('imagenes_canonizadas.id', ondelete='CASCADE'))
    imagen_canonizada = db.relationship("ImagenCanonizadaDTO", back_populates="regiones_anatomicas")

class AtributoDTO(db.Model):
    __tablename__ = "atributos_canonizados"
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)

    diagnostico_id = db.Column(db.String, db.ForeignKey('diagnosticos_canonizados.id', ondelete='CASCADE'))
    diagnostico = db.relationship("DiagnosticoDTO", back_populates="atributos")

class ImagenCanonizadaDTO(db.Model):
    __tablename__ = "imagenes_canonizadas"
    id = db.Column(db.String, primary_key=True)
    id_imagen_original = db.Column(db.String, nullable=False)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_canonizacion = db.Column(db.DateTime, nullable=False)
    modalidad = db.Column(db.String, nullable=False)
    formato_canonizado = db.Column(db.String, nullable=False)
    metadatos = db.Column(db.String, nullable=True)

    diagnostico = db.relationship("DiagnosticoDTO", back_populates="imagen_canonizada", uselist=False)
    regiones_anatomicas = db.relationship("RegionAnatomicaDTO", back_populates="imagen_canonizada",
                                        cascade="all, delete-orphan") 