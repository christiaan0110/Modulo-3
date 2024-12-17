from pymongo import MongoClient
from bson.objectid import ObjectId


# Función para conectar a la base de datos
def conectar_db(uri="mongodb://localhost:27017", db_name="recetario"):
    try:
        cliente = MongoClient(uri)
        db = cliente[db_name]
        return db
    except Exception as e:
        print("Error al conectar a la base de datos: " + str(e))
        return None


# Función para agregar una receta
def agregar_receta(db):
    nombre = input("Introduce el nombre de la receta: ")
    receta = {
        "nombre": nombre,
        "ingredientes": [],
        "pasos": []
    }
    try:
        print("\n--- Ingredientes ---")
        while True:
            ingrediente = input("Introduce un ingrediente (deja vacío para terminar): ")
            if ingrediente == "":
                break
            receta["ingredientes"].append(ingrediente)

        print("\n--- Pasos ---")
        while True:
            paso = input("Introduce un paso (deja vacío para terminar): ")
            if paso == "":
                break
            receta["pasos"].append(paso)

        resultado = db.recetas.insert_one(receta)
        print("Receta agregada con éxito con el ID: " + str(resultado.inserted_id))
    except Exception as e:
        print("Error al agregar la receta: " + str(e))


# Función para listar todas las recetas
def listar_recetas(db):
    try:
        recetas = db.recetas.find()
        print("\n--- Listado de Recetas ---")
        for receta in recetas:
            print(f"ID: {receta['_id']} | Nombre: {receta['nombre']}")
            print("Ingredientes:")
            for ingrediente in receta["ingredientes"]:
                print(f"  - {ingrediente}")
            print("Pasos:")
            for paso in receta["pasos"]:
                print(f"  - {paso}")
            print("\n")
    except Exception as e:
        print("Error al listar las recetas: " + str(e))


# Función para editar una receta
def editar_receta(db):
    listar_recetas(db)
    receta_id = input("Ingrese el ID de la receta a editar: ")
    try:
        receta = db.recetas.find_one({"_id": ObjectId(receta_id)})
        if receta:
            print("Introduce los nuevos valores (deja en blanco para mantener el actual):")
            nombre = input(f"Nombre [{receta['nombre']}]: ") or receta['nombre']

            ingredientes = []
            print("\n--- Ingredientes --- (deja vacío para mantener)")
            for ingrediente in receta["ingredientes"]:
                nuevo_ingrediente = input(
                    f"Ingrese el nuevo valor para {ingrediente} (o deja en blanco para mantener): ")
                ingredientes.append(nuevo_ingrediente if nuevo_ingrediente else ingrediente)

            pasos = []
            print("\n--- Pasos --- (deja vacío para mantener)")
            for paso in receta["pasos"]:
                nuevo_paso = input(f"Ingrese el nuevo valor para {paso} (o deja en blanco para mantener): ")
                pasos.append(nuevo_paso if nuevo_paso else paso)

            nuevos_datos = {
                "nombre": nombre,
                "ingredientes": ingredientes,
                "pasos": pasos
            }

            db.recetas.update_one({"_id": ObjectId(receta_id)}, {"$set": nuevos_datos})
            print("Receta actualizada exitosamente!")
        else:
            print("Receta no encontrada.")
    except Exception as e:
        print("Error al editar la receta: " + str(e))


# Función para eliminar una receta
def eliminar_receta(db):
    listar_recetas(db)
    receta_id = input("Ingrese el ID de la receta a eliminar: ")
    try:
        resultado = db.recetas.delete_one({"_id": ObjectId(receta_id)})
        if resultado.deleted_count > 0:
            print("Receta eliminada exitosamente!")
        else:
            print("Receta no encontrada.")
    except Exception as e:
        print("Error al eliminar la receta: " + str(e))


# Función para mostrar el menú
def menu():
    print("=== GESTIÓN DE RECETAS ===")
    print("1. Agregar receta")
    print("2. Editar receta")
    print("3. Eliminar receta")
    print("4. Listar recetas")
    print("5. Salir")


# Función principal del programa
def main():
    db = conectar_db()
    if db is None:
        return
    while True:
        menu()
        opcion = input("Opción: ")
        if opcion == "1":
            agregar_receta(db)
        elif opcion == "2":
            editar_receta(db)
        elif opcion == "3":
            eliminar_receta(db)
        elif opcion == "4":
            listar_recetas(db)
        elif opcion == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()