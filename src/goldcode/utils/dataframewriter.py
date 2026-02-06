import pandas as pd
import os
import logging


class DataFrameWriter:
    def __init__(self):
        pass

    def write_df(self, df, outfile, default=".parquet", logging: logging = None):
        """
        Skriver en df til det format, som passer i output-stien
        """
        try:
            # Henter ext
            filename, ext = os.path.splitext(outfile)

            if ext == "" or ext is None:
                ext = default
                outfile += default

            if ext.lower() == ".parquet":
                df.to_parquet(outfile, index=False)

            if ext.lower() in (".xls", ".xlsx"):
                df.to_excel(outfile, index=False)

            if ext.lower() in (".csv"):
                df.to_csv(outfile, index=False)

            if logging:
                logging.info(f"[INFO] Fil {filename} skrevet som {ext}")

        except Exception as e:
            if logging:
                logging.error(e)
            print(e)
