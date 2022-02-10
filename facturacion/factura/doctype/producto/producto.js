// Copyright (c) 2021, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Producto', {
	// refresh: function(frm) {

	// }
	onload:function(frm){
		frm.set_query("codimpuesto", function () {
			return {
			  query: "facturacion.facturacion.factura.doctype.producto.producto.getTarifaImpuesto",
			  filters: {
				impuesto: frm.doc.impuesto,
			  }
			};
		  });
	}
});
