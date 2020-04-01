file_path = "./dataset/20200315-sitrep-55-covid-19.pdf"

df = tabula.read_pdf(file_path, pages='all')

print(df)
