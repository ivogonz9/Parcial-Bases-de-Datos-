
# 🏨 Proyecto Integrador: Gestión Hotelera

Sistema de gestión hotelera desarrollado en Python utilizando el ORM **Peewee**, diseñado para conectarse a una base de datos relacional **MySQL** e iterar datos mediante operaciones CRUD con visualización formateada en consola via **Tabulate**.

Proyecto desarrollado para la materia **Base de Datos I** de la *Tecnicatura Superior en Desarrollo de Software* (IES 9-008 Manuel Belgrano).

---

## 🛠️ Stack Tecnológico

* **Lenguaje:** Python 3.14
* **Base de Datos:** MySQL (gestionado con MySQL Workbench)
* **ORM:** Peewee
* **Driver MySQL:** PyMySQL
* **Librería de Consola:** Tabulate
* **Control de Versiones:** Git & GitHub

---

## 🗄️ Modelo de Datos

El sistema modela la interacción entre **Huéspedes**, **Habitaciones**, **Recepcionistas**, **Reservas** y **Pagos**:

* **HUESPED** `(1:N)` **RESERVA**: Un huésped puede tener múltiples reservas.
* **HABITACION** `(1:N)` **RESERVA**: Una habitación puede asociarse a varias reservas en distintas fechas.
* **RECEPCIONISTA** `(1:N)` **RESERVA**: Un recepcionista puede registrar múltiples reservas.
* **RESERVA** `(1:N)` **PAGO**: Una reserva puede contar con uno o más pagos registrados.

---

👥 Integrantes del Equipo
Facundo Saenz

Ignacio Montagna

Ivo Gonzalez

Docente: Juan Caballero Gallar
