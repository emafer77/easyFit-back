import psycopg

class CategoriaEjercicioConnection:
    def __init__(self):
        try:
            self.conn = psycopg.connect(
                dbname='easyfitpg', 
                user='emafer77', 
                password='Maniola777', 
                host='localhost', 
                port='5432'
            )
        except psycopg.OperationalError as err:
            print(f"Error de conexión: {err}")
            self.conn = None
    
    def execute_query(self, query, params=None, fetch=False):
        """Método general para ejecutar consultas con parámetros y manejar errores"""
        if self.conn:
            try:
                with self.conn.cursor() as cur:
                    cur.execute(query, params)
                    if fetch:
                        return cur.fetchall()
                    self.conn.commit()
            except psycopg.Error as e:
                print(f"Error en la consulta: {e}")
                self.conn.rollback()
        else:
            print("Conexión no disponible.")
    
    def create(self, nombre, descripcion):
        """Inserta una nueva categoría de ejercicio en la base de datos"""
        query = "INSERT INTO categorias_ejercicios (nombre, descripcion) VALUES (%s, %s) RETURNING id"
        result = self.execute_query(query, (nombre, descripcion), fetch=True)
        if result:
            return result[0][0]  # Devuelve el ID de la categoría creada
        return None
    
    def read_all(self):
        """Obtiene todas las categorías de ejercicio"""
        query = "SELECT * FROM categorias_ejercicios"
        return self.execute_query(query, fetch=True)
    
    def read_one(self, categoria_id):
        """Obtiene una categoría de ejercicio por su ID"""
        query = "SELECT * FROM categorias_ejercicios WHERE id = %s"
        result = self.execute_query(query, (categoria_id,), fetch=True)
        if result:
            return {
                "id": result[0][0],
                "nombre": result[0][1],
                "descripcion": result[0][2]
            }
        return None
    
    def update(self, categoria_id, nombre_nuevo, descripcion_nueva):
        """Actualiza el nombre y la descripción de una categoría de ejercicio"""
        query = "UPDATE categorias_ejercicios SET nombre = %s, descripcion = %s WHERE id = %s"
        self.execute_query(query, (nombre_nuevo, descripcion_nueva, categoria_id))
        return True
    
    def delete(self, categoria_id):
        """Elimina una categoría de ejercicio por su ID"""
        query = "DELETE FROM categorias_ejercicios WHERE id = %s"
        self.execute_query(query, (categoria_id,))
        return True
