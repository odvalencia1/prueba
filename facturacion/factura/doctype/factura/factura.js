// Copyright (c) 2021, Frappe and contributors
// For license information, please see license.txt
var numRedondeo = 100.00;
frappe.ui.form.on("detalle_factura", {
	precio_unitario(frm, cdt, cdn) {
		calcularTotal(frm);
	},
	detalle_factura_remove(frm, cdt, cdn) {
		calcularTotal(frm);
	},
	detalle_factura_add(frm, cdt, cdn) {
		console.log(frm);
		console.log(cdt);
		console.log(cdn);
		frm.fields_dict['detalle_factura'].grid
	},
	cantidad(frm, cdt, cdn) {
		calcularTotal(frm);
	},
});

frappe.ui.form.on('Factura', {
	
	detalle_factura_on_form_rendered: function(frm, cdt, cdn){
		if(frm.fields_dict['detalle_factura'].grid.open_grid_row != undefined)
		{
			controlSoloNumero(frm.fields_dict['detalle_factura'].grid.open_grid_row.fields_dict.cantidad);
		}
	},
});

function calcularTotal(frm){
		var lst = frm.doc.detalle_factura;
		var sub = 0.0;
		var iva = 0.0;
		for(var i=0;i<lst.length;i++){  
			frm.doc.detalle_factura[i].total = frm.doc.detalle_factura[i].cantidad * frm.doc.detalle_factura[i].precio_unitario;
			iva += frm.doc.detalle_factura[i].cantidad * frm.doc.detalle_factura[i].precio_impuesto;
		}
		frm.refresh();
		if(isIterable(lst))
		{
			for (let value of lst) {
				sub = sub + value.total;
			}
		}
		
		var total = sub +iva - frm.doc.descuento;
		frm.set_value('subtotal', sub);
		frm.set_value('iva', iva);
		frm.set_value('total', total);
}
function isIterable(obj) {
	// checks for null and undefined
	if (obj == null) {
		return false;
	}
	return typeof obj[Symbol.iterator] === 'function';
}