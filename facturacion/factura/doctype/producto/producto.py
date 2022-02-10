# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Producto(Document):
	def before_save (self):
		self.precio_sin_impuesto = self.precio / (1+(int(self.porcentaje)/100))
		self.precio_impuesto = self.precio - self.precio_sin_impuesto

@frappe.whitelist(allow_guest=True)
def getTarifaImpuesto(filters):
	if filters.get('impuesto'):
		impuesto = filters.get('impuesto')
	return frappe.db.get_list('Tarifa',
    filters={
        'codimpuesto': impuesto
    },)