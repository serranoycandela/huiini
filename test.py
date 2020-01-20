from pdflatex import PDFLaTeX
from FacturasLocal import FacturaLocal as Factura
import os



import subprocess

#cp = subprocess.run(["C:\\Program Files\\MiKTeX 2.9\\miktex\\bin\\x64\\pdflatex.exe", "C:\\Dropbox\\Sicad\\Huiini\\0FEC2A65-F744-4E61-B65C-B5EC11B1EF45.tex"],shell=True)


f = Factura("C:\\Users\\Jorge Cano\\Documents\\GitHub\\huiini\\0FEC2A65-F744-4E61-B65C-B5EC11B1EF45.xml")

f.setFolio(1)
f.conviertemeEnTex()
f.conviertemeEnPDF()
