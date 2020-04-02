from cirilib.imports import *


def export_from_pdf(file_name):
	file_path = os.path.join(PDF_DIR, file_name)
	df = tabula.read_pdf(file_path, pages='all', pandas_options={'header': None})[1:]
	if len(df) > 1:
		df = df[0].append(df[1:], ignore_index=True)


# convert to csv, maybe use it?
# tabula.convert_into(file_path, "output.csv", output_format="csv", pages='all')


file = "20200401-sitrep-72-covid-19.pdf"
