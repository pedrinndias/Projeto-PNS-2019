from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

md_path = 'docs/documentacao_notebook.md'
pdf_path = 'docs/documentacao_notebook.pdf'

with open(md_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

c = canvas.Canvas(pdf_path, pagesize=A4)
width, height = A4
x = 2 * cm
y = height - 2 * cm

for line in lines:
    if y < 2 * cm:
        c.showPage()
        y = height - 2 * cm
    c.drawString(x, y, line.strip())
    y -= 0.6 * cm

c.save()
print('PDF gerado com sucesso!')