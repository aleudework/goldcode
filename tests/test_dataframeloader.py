from goldcode.utils.dataframeloader import DataFrameLoader

reader = DataFrameLoader()

path = '/Users/alhu/Data/Konverteringsdata/Downloadet/BilagsMapping/BilagsMapping_251231'

df = reader.load_df_from_chunks(path)

print(df.info())

df.to_parquet('/Volumes/ALHU APFS/bilagsmapping.parquet', index=False)

print("---------")


dfloader = DataFrameLoader()

input_folder = '/Volumes/ALHU APFS/Migrering/Lejerbo Regnskaber/601-0'

df = dfloader.load_files_to_df(input_folder)

print(df.head())

