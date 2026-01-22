"""
Skal omstruktureres og med kommentarer
"""


import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

class Downloader():

    def __init__(self, conn_str):
        self.conn_str = conn_str


    def set_default_conn_str(self):
        try:
            server = os.getenv('SERVER_KONV_DB')
            database = os.getenv('DATABASE_KONV_DB')
            username = os.getenv('USERNAME_KONV_DB')
            password = os.getenv('PASSWORD_KONV_DB')

            conn_str = (
                f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}"
                "?driver=ODBC+Driver+18+for+SQL+Server"
                "&TrustServerCertificate=yes")
        
            self.conn_str = conn_str

        except Exception as e:
            print(e)

            
    def test_connection(self, conn_str=None):
        """
        Test connection to DB
        """
        try:
            if conn_str is None:
                conn_str = self.conn_str

            engine = create_engine(conn_str)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("DB-forbindelse OK")
        except SQLAlchemyError as e:
            print("DB-forbindelse fejlede:", e)


    def download_large_table(self, table_name, output_path, log_path, chunksize=1_000_000, conn_str=None):

        # Use class conn_str
        if conn_str is None:
            conn_str = self.conn_str

        # --- Logging setup --- #

        # Opret log handler (der kommer to, én til terminal og én til log-fil)
        log_handlers = []
        # Håndter log fil
        if log_path:
            # log handler for file. Appender hvis filen eksisterer
            log_handlers.append(logging.FileHandler(log_path, mode='a', encoding='utf-8'))
        # Håndter terminal
        log_handlers.append(logging.StreamHandler())
        # Configurer log
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s: %(message)s",
            handlers=log_handlers
        )

        # Informer om tabel til upload
        logging.info(f"[INFO] Påbegynder download af {table_name}")

        # --- Egentlig logik ---

        sql = f"SELECT * FROM {table_name}"
        
        if not os.path.isdir(output_path):
            print(f"Output mappe eksisterer ikke")
            return
        
        try:
            # Initilisere engine til database
            engine = create_engine(conn_str)

            with engine.connect() as conn:

                # Definerer en chunk. Opretter en generator (som først kaldes i loopet
                # Lidt som pandas i forvejen definerer noget og først eksekveres ved specifikke funktioner)
                chunks = pd.read_sql(
                    text(sql),
                    conn,
                    chunksize=chunksize
                )

                for i, chunk in enumerate(chunks):
                    path = os.path.join(output_path, f"{table_name}_{i}.parquet")
                    chunk.to_parquet(path, index=False)
                    logging.info(f"[GEMT] Chunk nr: {i}, I alt {len(chunk)} rækker, path: {path}")


            logging.info(f"[FÆRDIG] Download er kørt færdigt")

        except SQLAlchemyError as e:
            logging.error(f"FEJL i DB-Motor: {e}")


