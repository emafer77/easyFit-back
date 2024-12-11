import psycopg

class MusculoConnection:
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
    
    def create(self, nombre):
        """Inserta un nuevo músculo en la base de datos"""
        query = "INSERT INTO musculos (nombre) VALUES (%s) RETURNING id"
        result = self.execute_query(query, (nombre,), fetch=True)
        if result:
            return result[0][0]  # Devuelve el ID del músculo creado
        return None
    
    def read_all(self):
        """Obtiene todos los músculos"""
        query = "SELECT * FROM musculos"
        return self.execute_query(query, fetch=True)
    
    def read_one(self, musculo_id):
        """Obtiene un músculo por su ID"""
        query = "SELECT * FROM musculos WHERE id = %s"
        result = self.execute_query(query, (musculo_id,), fetch=True)
        if result:
            return {
                "id": result[0][0],
                "nombre": result[0][1]
            }
        return None
    
    def update(self, musculo_id, nombre_nuevo):
        """Actualiza el nombre de un músculo"""
        query = "UPDATE musculos SET nombre = %s WHERE id = %s"
        self.execute_query(query, (nombre_nuevo, musculo_id))
        return True
    
    def delete(self, musculo_id):
        """Elimina un músculo por su ID"""
        query = "DELETE FROM musculos WHERE id = %s"
        self.execute_query(query, (musculo_id,))
        return True
