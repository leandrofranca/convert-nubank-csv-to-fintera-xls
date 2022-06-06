import csv
import re
from collections import OrderedDict
from datetime import datetime
from os import listdir
from os.path import isfile, join, splitext

from pyexcel_xls import save_data

csvs = [f for f in listdir('.') if isfile(
    join('.', f)) and re.search("^nubank.*csv$", f)]

for c in csvs:
    arquivo_saida = splitext(c)[0] + ".xls"
    print('Tratando arquivo', c, 'e gerando', arquivo_saida)
    output = OrderedDict()
    tuples = [["Tipo", "Nº de Parcelas", "Quantia (R$)", "Descrição", "Data", "Categoria",
               "Nº do Documento", "Centro de Custo / Receita", "Cliente/Fornecedor", "Observação"]]
    with open(c) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['title'] == 'Pagamento recebido':
                continue
            date = datetime.strptime(row['date'], '%Y-%m-%d')
            tuples += [["Normal", "", float(row['amount'])*-1, row['title'],
                        date, row['category'].capitalize(), "", "", "", ""]]
    output.update({"Sheet1": tuples})
    save_data(arquivo_saida, output)
