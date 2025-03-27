import os
import MySQLdb


class DatabaseSetupService:
    def __init__(self, mysql):
        self.mysql = mysql

    def create_database(self):
        try:
            conn = MySQLdb.connect(
                host='localhost',
                user=os.getenv('MYSQL_USER'),
                passwd=os.getenv('MYSQL_PASSWORD')
            )
            cur = conn.cursor()
            
            cur.execute("SHOW DATABASES LIKE %s", (os.getenv('MYSQL_DB'),))
            result = cur.fetchone()

            if not result:
                cur.execute(f"CREATE DATABASE {os.getenv('MYSQL_DB')}")
                print(f"Banco de dados '{os.getenv('MYSQL_DB')}' criado com sucesso!")

            cur.close()
            conn.close()

        except MySQLdb.Error as e:
            print(f"Erro ao conectar ou criar banco de dados: {e}")

    def create_tables(self):
        try:
            conn = self.mysql.connection
            cur = conn.cursor()

            cur.execute("SHOW TABLES LIKE 'feedback'")
            feedback_table_exists = cur.fetchone()

            cur.execute("SHOW TABLES LIKE 'feature'")
            feature_table_exists = cur.fetchone()

            if not feedback_table_exists:
                cur.execute("""
                    CREATE TABLE feedback (
                        id INT PRIMARY KEY,
                        feedback TEXT NOT NULL
                    )
                """)
                print("Tabela 'feedback' criada com sucesso!")

            if not feature_table_exists:
                cur.execute("""
                    CREATE TABLE feature (
                        id INT PRIMARY KEY,
                        feature_name VARCHAR(100) NOT NULL
                    )
                """)
                print("Tabela 'feature' criada com sucesso!")

            cur.close()
        
        except MySQLdb.Error as e:
            print(f"Erro ao verificar ou criar tabelas: {e}")