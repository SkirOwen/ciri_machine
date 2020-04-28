from cirilib.imports import *

try:
    import tabula
except ImportError:
    print("Please install tabula for python and try again\n",
          "tabula-py==2.1.0")


def export_from_pdf(file_name):
    file_path = os.path.join(PDF_DIR, file_name)
    print("Extracting table from", file_name, "...")
    df = tabula.read_pdf(file_path, pages='all', pandas_options={'header': None})[1:]
    
    table_begin_index = 1
    
    for i in range(len(df)):
        if any(word in str(df[i][0][0]) for word in TABLE_START_WORD):
            table_begin_index = i
    
    if len(df) > 1:
        df = df[0].append(df[table_begin_index:], ignore_index=True)
    print(file_name, "extracted!")
    return df


# convert to csv, maybe use it?
# tabula.convert_into(file_path, "output.csv", output_format="csv", pages='all')

# file = "20200401-sitrep-72-covid-19.pdf"

files = os.listdir(PDF_DIR)

if __name__ == '__main__':
    reports = []
    reports.append(export_from_pdf(files[0]))
    print(reports)
