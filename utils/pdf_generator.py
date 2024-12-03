from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from models.model import Patrimonios  

def criar_pdf(sala):
    pdf_filename = f"tabela_patrimonio_sala_{sala}.pdf"
    
    documento = SimpleDocTemplate(pdf_filename, pagesize=A4)
    
    elementos = []
    
    img_path = 'static/img/iconefp.png'
    img = Image(img_path, width=50, height=50)
    elementos.append(img)
    
    styles = getSampleStyleSheet()
    titulo = Paragraph(f"Tabela de Patrimônios - Sala {sala}", styles['Title'])
    elementos.append(titulo)

    patrimonios = Patrimonios.query.filter_by(local=sala).all()

    dados = [['Etiqueta', 'Local', 'Denominação', 'Data de Chegada','Situação']]
    for patrimonio in patrimonios:
        dados.append([
            patrimonio.numero_de_etiqueta,
            patrimonio.local,
            patrimonio.denominacao_de_imobiliario,
            patrimonio.data_de_chegada
        ])

    tabela = Table(dados)
    
    # Aplicando estilo à tabela
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black,),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elementos.append(tabela)

    documento.build(elementos)
    
    return pdf_filename