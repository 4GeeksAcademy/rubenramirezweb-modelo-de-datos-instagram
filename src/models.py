from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Foreignkey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er

# Una Tabla User -> para registrar usuarios

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
            # do not serialize the password, its a security breach
        }
