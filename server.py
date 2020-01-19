#import math
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
#from matplotlib.figure import Figure
#import StringIO
#import numpy
from os import listdir
#from werkzeug import secure_filename
import os
#import Facturas as fac
#from Facturas import Factura
from FacturasServer import FacturaServer as Factura
from jinja2 import Environment, FileSystemLoader
import jinja2
import time as time_old
from subprocess import Popen
from flask import Flask, make_response, request, send_from_directory, redirect, url_for, abort
import json
from sh import pdflatex

app = Flask(__name__)

env = Environment(loader=FileSystemLoader('templates'))
#script_path = os.path.dirname(os.path.abspath( __file__ ))
UPLOAD_FOLDER = '/home/huiini/huiini/uploads'
ALLOWED_EXTENSIONS = set(['xml'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route("/grabXML/")
# def recibeXml(xml,folio):
#     f = fac.Factura(xml)
#
#     return f.conviertemeEnPDF(folio)
def getTemplate(tpl_path):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename) 


@app.route('/resumen', methods= ['GET'])
def haz_diot():
    listaDiot = json.loads(request.args['lista_diot'])
    #listaDiot = request.args['lista_diot']
    context = {'lista_diot': listaDiot}
    tex_path = os.path.join(app.config['UPLOAD_FOLDER'],"resumenDiot.tex")
    script_path = os.path.dirname(os.path.abspath( __file__ ))
    getTemplate(os.path.join(script_path, "templateDiot.jinja")).stream(context).dump(tex_path)

    

    os.chdir(os.path.dirname(tex_path))
    conversion = pdflatex(tex_path)



    if conversion.exit_code == 0:
        return send_from_directory(app.config['UPLOAD_FOLDER'], "resumenDiot.pdf")
    else:
        content = {'please move along': 'nothing to see here'}
        abort(500)


@app.route('/download', methods= ['GET'])
def devuelve_pdf():

    f = Factura(os.path.join(app.config['UPLOAD_FOLDER'], request.args['xml_name']))

    f.setFolio(request.args['folio'])
    f.conviertemeEnTex()
    pudiste = f.conviertemeEnPDF(app.config['UPLOAD_FOLDER'])
    if pudiste == 0:
        return send_from_directory(app.config['UPLOAD_FOLDER'], request.args['uuid']+".pdf")
    else:
        return "0"

@app.route("/upload", methods=['GET', 'POST'])
def obten_xml():
    if request.method == 'POST':
        file = request.files['files']
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            f = Factura(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            f.setFolio(1)
#            f.conviertemeEnTex()
#            f.conviertemeEnPDF("/home/huiini/workspacePy/test_request/uploads/")
            return redirect(url_for('obten_xml'))
    
    time_old.sleep(2)
    return "ya"




@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('uploads', path)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
