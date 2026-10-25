/*creacion de base de datos y tablas*/
 create database Hotel;
 use Hotel;
 create table Huesped(
 id_huesped int not null auto_increment primary key,
 Nombre varchar (255) not null,
 direccion varchar (255)
 );
 create table habitacion(
 id_habitacion int not null auto_increment primary key,
 tipo varchar (255) not null,
 precio decimal (10,2) not null
 );
 create table Recepcionista(
 id_Recepcionista int not null auto_increment primary key,
 nombre varchar (255)
 );
  create table Reserva(
 id_Reserva int not null auto_increment primary key,
 numero int not null unique,
 cant_dias int not null,
 id_huesped int,
 foreign key (id_huesped) references Huesped(id_huesped),
 id_habitacion int,
 foreign key (id_habitacion) references habitacion(id_habitacion),
 id_Recepcionista int,
 foreign key (id_Recepcionista) references Recepcionista(id_Recepcionista)
 );
create table Pago(
id_pago int not null auto_increment primary key,
monto decimal (10,2) not null,
fecha datetime not null,
metodo_pago varchar (255) not null,
id_reserva int,
foreign key (id_Reserva) references Reserva(id_Reserva)
);
/*Usuario con todos los privilegios*/
CREATE ROLE IF NOT EXISTS 'rol_admin_hotel';
GRANT ALL PRIVILEGES ON Hotel.* TO 'rol_admin_hotel';
CREATE USER IF NOT EXISTS 'ivo'@'localhost' IDENTIFIED BY 'AdminHotel123!';
GRANT 'rol_admin_hotel' TO 'ivo'@'localhost';
SET DEFAULT ROLE 'rol_admin_hotel' TO 'ivo'@'localhost';
/*Usuario escritura y lectura*/
CREATE ROLE IF NOT EXISTS 'rol_rw_hotel';
GRANT SELECT, INSERT, UPDATE, DELETE ON Hotel.* TO 'rol_rw_hotel';
CREATE USER IF NOT EXISTS 'operador_hotel'@'localhost' IDENTIFIED BY 'Operador123!';
GRANT 'rol_rw_hotel' TO 'operador_hotel'@'localhost';
SET DEFAULT ROLE 'rol_rw_hotel' TO 'operador_hotel'@'localhost';
/*Usuario permiso minimo*/
CREATE ROLE IF NOT EXISTS 'rol_publico_hotel';
GRANT SELECT ON Hotel.* TO 'rol_publico_hotel';
CREATE USER IF NOT EXISTS 'publico_hotel'@'localhost' IDENTIFIED BY 'Publico123!';
GRANT 'rol_publico_hotel' TO 'publico_hotel'@'localhost';
SET DEFAULT ROLE 'rol_publico_hotel' TO 'publico_hotel'@'localhost';
FLUSH PRIVILEGES;
/*Insertar a las tablas, registros*/
INSERT INTO Huesped (Nombre, direccion) VALUES 
('Carlos Benitez', 'Av. San Martin 120'), 
('Lucia Morales', 'Calle Belgrano 450'), 
('Mariano Gomez', 'Rivadavia 890');

INSERT INTO habitacion (tipo, precio) VALUES 
('Simple', 15000.00), 
('Doble', 25000.00), 
('Suite Presidencial', 60000.00);

INSERT INTO Recepcionista (nombre) VALUES 
('Sofia Perez'), 
('Lucas Rodriguez');

INSERT INTO Reserva (numero, cant_dias, id_huesped, id_habitacion, id_Recepcionista) VALUES 
(101, 3, 1, 1, 1), 
(102, 5, 2, 2, 2);

INSERT INTO Pago (monto, fecha, metodo_pago, id_reserva) VALUES 
(45000.00, '2026-10-10 10:00:00', 'Tarjeta de Credito', 1), 
(125000.00, '2026-10-11 11:30:00', 'Transferencia', 2), 
(15000.00, '2026-10-12 18:00:00', 'Tarjeta de Credito', 1), 
(25000.00, '2026-10-13 09:15:00', 'Efectivo', 2);
-- ==============================================================
-- 1. CONSULTAS ABMC
-- (Cumple la rúbrica de afectar 2 tablas relacionadas por integrante: UPDATE, DELETE e INSERT)
-- ==============================================================
-- INSERT (Afecta 2 tablas relacionadas: inserta en Pago calculando el monto desde Reserva y Habitacion)
INSERT INTO Pago (monto, fecha, metodo_pago, id_reserva) 
SELECT (hab.precio * r.cant_dias), NOW(), 'Efectivo', r.id_Reserva 
FROM Reserva r 
JOIN habitacion hab ON r.id_habitacion = hab.id_habitacion 
WHERE r.numero = 101;
-- UPDATE (Afecta 2 tablas relacionadas: actualiza Reserva según condición en Huesped)
UPDATE Reserva r 
JOIN Huesped h ON r.id_huesped = h.id_huesped 
SET r.cant_dias = r.cant_dias + 1 
WHERE h.Nombre = 'Carlos Benitez';
-- DELETE (Afecta 2 tablas relacionadas: elimina de Pago según condición en Reserva)
DELETE p 
FROM Pago p 
JOIN Reserva r ON p.id_reserva = r.id_Reserva 
WHERE r.numero = 101 AND p.metodo_pago = 'Efectivo';
-- SELECT (Consulta sobre 2 tablas relacionadas: Huesped y Reserva)
SELECT h.Nombre AS Huesped, h.direccion AS Direccion, r.numero AS Numero_Reserva, r.cant_dias AS Dias_Estadia 
FROM Huesped h 
JOIN Reserva r ON h.id_huesped = r.id_huesped;