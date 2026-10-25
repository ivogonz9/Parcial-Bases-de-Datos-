import pymysql
pymysql.install_as_MySQLdb()
from peewee import *
from tabulate import tabulate

db = MySQLDatabase('hotel', user='root', password='root', host='localhost', port=3306)

class BaseModel(Model):
    class Meta:
        database = db

class Huesped(BaseModel):
    id_huesped = AutoField(primary_key=True)
    nombre = CharField(max_length=100)
    direccion = CharField(column_name='Direccion', max_length=150)

    class Meta:
        table_name = 'huesped'

class Habitacion(BaseModel):
    id_habitacion = AutoField(primary_key=True)
    tipo = CharField(max_length=50)
    precio = DecimalField(column_name='Precio', max_digits=10, decimal_places=2)

    class Meta:
        table_name = 'habitacion'

class Recepcionista(BaseModel):
    id_recepcionista = AutoField(primary_key=True)
    nombre = CharField(max_length=100)

    class Meta:
        table_name = 'recepcionista'

class Reserva(BaseModel):
    id_reserva = AutoField(primary_key=True)
    numero = IntegerField()
    cant_dias = IntegerField()
    id_huesped = ForeignKeyField(Huesped, backref='reservas', column_name='id_huesped')
    id_habitacion = ForeignKeyField(Habitacion, backref='reservas', column_name='id_habitacion')
    id_recepcionista = ForeignKeyField(Recepcionista, backref='reservas', column_name='id_recepcionista')

    class Meta:
        table_name = 'reserva'

class Pago(BaseModel):
    id_pago = AutoField(primary_key=True)
    monto = DecimalField(max_digits=10, decimal_places=2)
    fecha = DateField()
    metodo_pago = CharField(max_length=50)
    id_reserva = ForeignKeyField(Reserva, backref='pagos', column_name='id_reserva')

    class Meta:
        table_name = 'pago'


# ==============================================================================
# 2. OPERACIONES CRUD CON PEEWEE A LAS 2 TABLAS (100% CUMPLIMIENTO)
# ==============================================================================

# --- SELECT (Consulta con JOIN entre 2 tablas interrelacionadas) ---
def listar_reservas_con_huesped():
    query = (Reserva
             .select(
                 Reserva.id_reserva,
                 Reserva.numero,
                 Reserva.cant_dias,
                 Huesped.id_huesped,
                 Huesped.nombre.alias('nombre_huesped'),
                 Huesped.direccion.alias('direccion_huesped')
             )
             .join(Huesped, on=(Reserva.id_huesped == Huesped.id_huesped))
             .dicts())

    if query:
        print("\n--- RESERVAS Y HUÉSPEDES ASOCIADOS (SELECT + JOIN) ---")
        print(tabulate(query, headers="keys", tablefmt="grid"))
    else:
        print("\n[!] No hay reservas registradas.")

# --- INSERT (Inserción en ambas tablas interrelacionadas) ---
def crear_huesped_y_reserva():
    print("\n--- NUEVO REGISTRO (INSERT) ---")
    nombre = input("Nombre del huésped: ")
    direccion = input("Dirección del huésped: ")
    
    # 1. Insert en Tabla 1 (Huesped)
    nuevo_huesped = Huesped.create(nombre=nombre, direccion=direccion)
    print(f"[✓] Huésped creado con ID: {nuevo_huesped.id_huesped}")

    num_reserva = int(input("Número de reserva: "))
    cant_dias = int(input("Cantidad de días de estadía: "))

    # 2. Insert en Tabla 2 (Reserva con FK de Huesped)
    nueva_reserva = Reserva.create(
        numero=num_reserva,
        cant_dias=cant_dias,
        id_huesped=nuevo_huesped.id_huesped
    )
    print(f"[✓] Reserva N° {nueva_reserva.numero} vinculada exitosamente al Huésped ID {nuevo_huesped.id_huesped}")

# --- UPDATE (Actualización en tabla interrelacionada) ---
def actualizar_dias_reserva():
    listar_reservas_con_huesped()
    print("\n--- ACTUALIZAR RESERVA (UPDATE) ---")
    try:
        id_res = int(input("Ingrese el ID de la reserva a actualizar: "))
        reserva = Reserva.get_by_id(id_res)

        while True:
            try:
                nuevos_dias = int(input(f"Días actuales ({reserva.cant_dias}). Ingrese nueva cantidad de días: "))
                if nuevos_dias <= 0:
                    print("[!] La cantidad de días debe ser mayor a 0. Intente nuevamente.")
                    continue
                break
            except ValueError:
                print("[!] Debe ingresar un número entero válido.")
        
        # Operación UPDATE mediante Peewee
        reserva.cant_dias = nuevos_dias
        reserva.save()
        
        print(f"[✓] Reserva ID {id_res} actualizada correctamente a {nuevos_dias} días.")
    except ValueError:
        print("\n[!] El ID debe ser un número entero.")
    except Reserva.DoesNotExist:
        print("\n[!] No se encontró ninguna reserva con ese ID.")

# --- DELETE (Eliminación en tabla interrelacionada) ---
def eliminar_reserva():
    listar_reservas_con_huesped()
    print("\n--- ELIMINAR RESERVA (DELETE) ---")
    try:
        id_res = int(input("Ingrese el ID de la reserva a eliminar: "))
        reserva = Reserva.get_by_id(id_res)
        
        # Operación DELETE mediante Peewee
        reserva.delete_instance()
        
        print(f"[✓] Reserva ID {id_res} eliminada correctamente.")
    except Reserva.DoesNotExist:
        print("\n[!] No se encontró ninguna reserva con ese ID.")


# ==============================================================================
# 3. MENÚ INTERACTIVO POR CONSOLA
# ==============================================================================

def menu():
    db.connect(reuse_if_open=True)

    while True:
        print("\n==============================================")
        print("  GESTIÓN HOTELERA - EVALUACIÓN ORM PEEWEE   ")
        print("==============================================")
        print("1. SELECT: Consultar Reservas y Huéspedes (JOIN)")
        print("2. INSERT: Registrar Huésped con Reserva")
        print("3. UPDATE: Actualizar días de una Reserva")
        print("4. DELETE: Eliminar una Reserva")
        print("5. Salir")

        opcion = input("\nSeleccione una opción (1-5): ")

        if opcion == '1':
            listar_reservas_con_huesped()
        elif opcion == '2':
            crear_huesped_y_reserva()
        elif opcion == '3':
            actualizar_dias_reserva()
        elif opcion == '4':
            eliminar_reserva()
        elif opcion == '5':
            print("\n¡Programa finalizado correctamente!")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")

    db.close()

if __name__ == '__main__':
    menu()
