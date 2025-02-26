from src.sta.config.db import db

Base = db.declarative_base()


class DemografiaDTO(db.Model):
    __tablename__ = "demografias"
    id = db.Column(db.String, primary_key=True)
    edad = db.Column(db.Integer, primary_key=True, nullable=False)
    grupo_edad = db.Column(db.String, nullable=False, primary_key=True)
    sexo = db.Column(db.String, nullable=False, primary_key=True)
    etnicidad = db.Column(db.String, nullable=False, primary_key=True)

    diagnostico_id = db.Column(db.String, db.ForeignKey('diagnosticos.id', ondelete='CASCADE'))
    diagnostico = db.relationship("DiagnosticoDTO", back_populates="demografia", uselist=False)


class DiagnosticoDTO(db.Model):
    __tablename__ = "diagnosticos"
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)

    imagen_medica_id = db.Column(db.String, db.ForeignKey('imagenes_medicas.id', ondelete='CASCADE'), unique=True)
    imagen_medica = db.relationship("ImagenMedicaDTO", back_populates="diagnostico", uselist=False)

    demografia = db.relationship("DemografiaDTO", back_populates="diagnostico", uselist=False)

    atributos = db.relationship("AtributoDTO", back_populates="diagnostico", cascade="all, delete-orphan")


class RegionAnatomicaDTO(db.Model):
    __tablename__ = "regiones_anatomicas"
    id = db.Column(db.String, primary_key=True)
    categoria = db.Column(db.String, nullable=False)
    especificacion = db.Column(db.String, nullable=False)

    imagen_medica_id = db.Column(db.String, db.ForeignKey('imagenes_medicas.id', ondelete='CASCADE'))
    imagen_medica = db.relationship("ImagenMedicaDTO", back_populates="regiones_anatomicas")


class AtributoDTO(db.Model):
    __tablename__ = "atributos"
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)

    diagnostico_id = db.Column(db.String, db.ForeignKey('diagnosticos.id', ondelete='CASCADE'))
    diagnostico = db.relationship("DiagnosticoDTO", back_populates="atributos")


class ImagenMedicaDTO(db.Model):
    __tablename__ = "imagenes_medicas"
    id = db.Column(db.String, primary_key=True, unique=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    modalidad = db.Column(db.String, nullable=False, primary_key=True)

    diagnostico = db.relationship("DiagnosticoDTO", back_populates="imagen_medica", uselist=False)

    regiones_anatomicas = db.relationship("RegionAnatomicaDTO", back_populates="imagen_medica",
                                          cascade="all, delete-orphan")
