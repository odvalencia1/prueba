# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import frappe, os
from frappe.model.document import Document
import random
from datetime import datetime
import random
from datetime import datetime
import xml.etree.ElementTree as ET

@frappe.whitelist(allow_guest=True)
def sendEmail(self):
	try:
		
		attachments = [{
			'fname': "Factura",
			'fcontent': frappe.attach_print(self.doctype, self.name, print_format=None)
		}]
		frappe.sendmail( recipients= [self.correo],
			cc=[],
			message= 'Gracias por preferirnos Sr(a) '+self.nombre+
				'.</BR>\n'+
				'Se adjunta factura en PDF.',
			subject= 'Factura de compra '+self.nombre,
			attachments= [frappe.attach_print(self.doctype,
        self.name, file_name=self.nombre)],
			reference_doctype= self.doctype,
			reference_name= self.name  )
	except Exception as e:
		frappe.throw("Error de envío de email: " + str(e))
		raise

@frappe.whitelist(allow_guest=True)
def generarClaveAcesso(self,fecha,tipoComprobante,ruc,ambiente,serie,secuencial):
    arrayFecha =  datetime.strptime(str(fecha), '%Y-%m-%d')
    dia = arrayFecha.strftime("%d")
    mes = arrayFecha.strftime("%m")
    anio = arrayFecha.strftime("%Y")
    claveAcceso = dia + mes + anio
    pin = "".join(random.sample('0123456789', 8))
    claveAcceso48 = (claveAcceso + tipoComprobante + ruc + ambiente + serie + secuencial + pin + '1')
    claveAcceso = claveAcceso48 + pin_dv_gen(claveAcceso48)
    return claveAcceso

@frappe.whitelist(allow_guest=True)
def pin_dv_gen(digs):
    baseMultiplicador = 7
    multiplicador = 2
    verificador = 0
    total = 0
	#frappe.throw( title='Error', msg='This file does not exist'+ claveAcceso48)
    for i in  reversed(digs):
        aux = int(i) * multiplicador
        multiplicador = multiplicador + 1
        if multiplicador > baseMultiplicador:
            multiplicador = 2
        total+=aux

    if total < 0 :
        verificador = 0
    else:
        m = total % 11

        r = 11 - m
        if r == 11:
            verificador = 0
        else:
            verificador = r

    if verificador == 10 :
            verificador = 1

    return str(verificador)

@frappe.whitelist(allow_guest=True)
def generarxml(doc):
    clave_acceso= doc.clave_acceso
    ruta = os.path.abspath(frappe.get_site_path("public", "files"))
    directorio = ruta + "/xmls"
    rutafile = directorio + "/" + clave_acceso + ".xml"

    if not os.path.exists(directorio):
        os.makedirs(directorio)

    company = frappe.get_doc("Negocio")
    ruc = clave_acceso[10:-26]
    
    
    factura = ET.Element('factura')
    factura.set("id", "comprobante")
    factura.set("version", "1.1.0")
    infoTributaria = ET.SubElement(factura, "infoTributaria")
    ambiente = ET.SubElement(infoTributaria, "ambiente")
    ambiente.text = clave_acceso[23:-25]
    tipoEmision = ET.SubElement(infoTributaria, "tipoEmision")
    tipoEmision.text = clave_acceso[47:-1]
    razonSocial = ET.SubElement(infoTributaria, "razonSocial")
    razonSocial.text = company.razon_social
    nombreComercial = ET.SubElement(infoTributaria, "nombreComercial")
    
    nombrecomer = company.nombre_comercial
    if  nombrecomer  != "" and nombrecomer  is not None :
        nombreComercial.text = nombrecomer
    else:
        nombreComercial.text = company.razon_social
    _ruc = ET.SubElement(infoTributaria, "ruc")
    _ruc.text = ruc
    infoFactura = ET.SubElement(factura, "infoFactura")
    claveAcceso = ET.SubElement(infoTributaria, "claveAcceso")
    claveAcceso.text = clave_acceso
    codDoc = ET.SubElement(infoTributaria, "codDoc")
    codDoc.text = clave_acceso[8:-39]
    estab = ET.SubElement(infoTributaria, "estab")
    estab.text = clave_acceso[24:-22]
    ptoEmi = ET.SubElement(infoTributaria, "ptoEmi")
    ptoEmi.text = clave_acceso[27:-19]
    secuencial = ET.SubElement(infoTributaria, "secuencial")
    secuencial.text = clave_acceso[30:-10]
    dirMatriz = ET.SubElement(infoTributaria, "dirMatriz")
    dirMatriz.text = company.direccion


    fechaEmision = ET.SubElement(infoFactura, "fechaEmision")
    femi = (clave_acceso[0:-47] + '/' + clave_acceso[2:-45] + '/' + clave_acceso[4:-41])
    fechaEmision.text = str(femi)
    
    dirEstablecimiento = ET.SubElement(infoFactura, "dirEstablecimiento") 
    dirEstablecimiento.text =  company.direccion
    
    objespecial = company.contribuyente_especial_numero
    if  objespecial != "" and objespecial is not None :
        contribuyenteEspecial = ET.SubElement(infoFactura,"contribuyenteEspecial")
        contribuyenteEspecial.text = objespecial


    obligadoContabilidad = ET.SubElement(infoFactura, "obligadoContabilidad")
    obligadoContabilidad.text = company.obli_conta

    datosComprador = frappe.get_doc('Cliente',doc.datos_cliente)
    tipoIdenComprador = datosComprador.tipo_documento

    tipoIdentificacionComprador = ET.SubElement(infoFactura,"tipoIdentificacionComprador")
    tipoIdentificacionComprador.text = tipoIdenComprador[0:2]

    razonSocialComprador = ET.SubElement(infoFactura, "razonSocialComprador")
    razonSocialComprador.text = datosComprador.name

    identificacionComprador = ET.SubElement(infoFactura, "identificacionComprador")
    identificacionComprador.text = datosComprador.cedula


    direccionComprador = ET.SubElement(infoFactura, "direccionComprador")
    direccionComprador.text = datosComprador.direccion

    totalSinImpuesto = ET.SubElement(infoFactura, "totalSinImpuestos")
    totalSinImpuesto.text = '{0:.2f}'.format(doc.subtotal)

    totalDescuento = ET.SubElement(infoFactura, "totalDescuento")
    totalDescuento.text = '{0:.2f}'.format(doc.descuento)
    
    totalConImpuestos = ET.SubElement(infoFactura,"totalConImpuestos")
    bimp=0
    totalImpuesto = ET.SubElement(totalConImpuestos,"totalImpuesto")
    codigo = ET.SubElement(totalImpuesto, "codigo")
    codigo.text = "02"
    codigoPorcentaje = ET.SubElement(totalImpuesto, "codigoPorcentaje")
    codigoPorcentaje.text = "02"
    baseImponible = ET.SubElement(totalImpuesto, "baseImponible")
    baseImponible.text = "12"
    valor = ET.SubElement(totalImpuesto, "valor")
    valor.text = '{0:.2f}'.format(doc.iva)

    propina = ET.SubElement(infoFactura, "propina")
    propina.text = "0.00"

    importeTotal = ET.SubElement(infoFactura, "importeTotal")
    imp_ = '{0:.2f}'.format(doc.total)

    importeTotal.text = imp_

    moneda = ET.SubElement(infoFactura, "moneda")
    moneda.text = "DOLAR"
    
    pagos  = ET.SubElement(infoFactura, "pagos")
    pago = ET.SubElement(pagos, "pago")
    formaPago = ET.SubElement(pago, "formaPago")
    formaPago.text = "20"
    total = ET.SubElement(pago, "total")
    total.text =  imp_ 
    detalles = ET.SubElement(factura, "detalles")
    #factura 
    for p in doc.detalle_factura:
        if not p.producto:
            frappe.throw("Error al momento de asigar el código"+ p.producto)
        detalle = ET.SubElement(detalles, "detalle")
        codigoPrincipal = ET.SubElement(detalle, "codigoPrincipal")
        codigoPrincipal.text = p.producto

        #codigoAuxiliar = ET.SubElement(detalle, "codigoAuxiliar")
        #codigoAuxiliar.text = ""

        descripcion = ET.SubElement(detalle, "descripcion")
        descripcion.text = p.nombre

        cantidad = ET.SubElement(detalle, "cantidad")
        cantidad.text = '{0:.2f}'.format(p.cantidad)

        precioUnitario = ET.SubElement(detalle, "precioUnitario")
        precioUnitario.text = '{0:.2f}'.format(p.precio_unitario)

        descuento = ET.SubElement(detalle, "descuento")
        descuento.text = "0.00"

        precioTotalSinImpuesto = ET.SubElement(detalle, "precioTotalSinImpuesto")

        precioTotalSinImpuesto.text =   '{0:.2f}'.format(float(p.total))

        impuestos_prod =  ET.SubElement(detalle, "impuestos")
        impuesto_prod =  ET.SubElement(impuestos_prod, "impuesto")
        codigo_prod =  ET.SubElement(impuesto_prod, "codigo")
        codigo_prod.text = "02"
        codigoPorcentaje_prod =  ET.SubElement(impuesto_prod, "codigoPorcentaje")
        codigoPorcentaje_prod.text = "02"

        tarifa_prod =  ET.SubElement(impuesto_prod, "tarifa")
        tarifa_prod.text = "12"
        baseImponible_prod =  ET.SubElement(impuesto_prod, "baseImponible")
        baseImponible_prod.text =  '{0:.2f}'.format(p.total)

        valor_prod =  ET.SubElement(impuesto_prod, "valor")
        valor_prod.text =  '{0:.2f}'.format(p.precio_impuesto)
    infoAdicional =  ET.SubElement(factura, "infoAdicional")
    campoAdicional =  ET.SubElement(infoAdicional, "campoAdicional")
    campoAdicional.text = datosComprador.telefono
    campoAdicional.set('nombre',"Telefono")
    campoAdicional =  ET.SubElement(infoAdicional, "campoAdicional")
    campoAdicional.text = datosComprador.correo_electronico
    campoAdicional.set('nombre',"Email")
    tree = ET.ElementTree(factura)
    tree.write(rutafile, xml_declaration=True, encoding='UTF-8', method="xml")
    return rutafile

class Factura(Document):
	def on_submit(self):
		negocio = frappe.get_doc("Negocio")
		if self.docstatus == 1:
			self.clave_acceso = generarClaveAcesso(self,self.fecha,"04",negocio.ruc,negocio.ambiente[0:1],negocio.estab + negocio.pto_emi,negocio.secuencial)
			self.barcode_ca=self.clave_acceso
			generarxml(self)
			sendEmail(self)
			le= 10 - len(str(int(negocio.secuencial)+1))
			secuencial =""
			for i in range(1, le):
				secuencial += "0"
			negocio.secuencial +=str(int(negocio.secuencial)+1)
            
