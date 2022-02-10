// Copyright (c) 2022, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Nota de credito', {
	// refresh: function(frm) {

	// }
	factura:function(frm,c){
		if(frm.doc.factura!=undefined && frm.doc.factura!="")
		{	
			frm.clear_table("detalle_factura");
			frappe.call({
				method: 'facturacion.factura.doctype.nota_de_credito.nota_de_credito.getProductos',
				args: {factura: frm.doc.factura},
				callback: (r) => {
					if(r.message!=undefined)
					{
						var fac = r.message
						console.log(fac)
						fac.forEach(element => {
							var new_ = frm.add_child("detalle_factura");
							frappe.model.set_value(new_.doctype, new_.name, "producto", element.producto);
							frappe.model.set_value(new_.doctype, new_.name, "nombre", element.nombre);
							frappe.model.set_value(new_.doctype, new_.name, "cantidad", element.cantidad);
							frappe.model.set_value(new_.doctype, new_.name, "precio_unitario", element.precio_unitario);
							frappe.model.set_value(new_.doctype, new_.name, "total", element.total);
							frappe.model.set_value(new_.doctype, new_.name, "precio_impuesto", element.precio_impuesto);
						}); 
						frm.refresh_field("detalle_factura");
					}
				}
			});
		}
	}
});
