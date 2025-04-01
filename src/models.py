from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active" : self.is_active
            # do not serialize the password, its a security breach
        }


# Relacion uno a uno
class Persona(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    pasaporte_id: Mapped[int] = mapped_column(Integer, ForeignKey('pasaporte.id'), unique=True)
    pasaporte: relationship('Pasaporte', back_populates='persona', uselist=False)


class Pasaporte(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[str] = mapped_column(String(20))




#### app ####

persona = Persona(nombre="Carlos")
pasaporte = Pasaporte(numero='ABC123')

persona.pasaporte = pasaporte

db.session.add(persona)
db.session.commit()
print(persona.pasaporte.numer) # ABC123
print(pasaporte.persona.nombre) # Carlos

# Relacion uno a muchos

class Autor(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    # Relacion
    libros: relationship('Libro', back_populates='autor')



class Libro(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(120))
    autor_id: Mapped[int] = mapped_column(Integer, ForeignKey('autor.id'))
    

# Relacion muchos a muchos

# Tabla intermedia
inscripciones = Table('inscripciones',
        Column("estudiante_id", Integer, ForeignKey('estudiante.id'), primary_key=True),
        Column('curso_id', Integer, ForeignKey('curso.id'), primary_key=True)
)

class Estudiante(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    cursos: relationship('Curso', sencondary=inscripciones, back_populates='estudiantes')


class Curso(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))