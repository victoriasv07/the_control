import csv
from models.model import Patrimonios

def criar_csv(sala):
    with open(f"tabela_patrimonio_sala_{sala}.csv", "w", newline="") as csv_file:
        patrimonios = Patrimonios.query.filter_by(local=sala).all()
        cabecalho = ["numero_de_etiqueta", "local", "denominacao_de_imobiliario", "data_de_chegada"]
        writer = csv.DictWriter(csv_file, fieldnames=cabecalho)
        writer.writeheader()
        for patrimonio in patrimonios:
            writer.writerow(
                {
                    "numero_de_etiqueta": patrimonio.numero_de_etiqueta,
                    "local": patrimonio.local,
                    "denominacao_de_imobiliario": patrimonio.denominacao_de_imobiliario,
                    "data_de_chegada": patrimonio.data_de_chegada
                }
            )

    csv_file.close()
    return f"tabela_patrimonio_sala_{sala}.csv"
