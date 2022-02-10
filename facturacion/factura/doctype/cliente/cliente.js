// Copyright (c) 2021, Frappe and contributors
// For license information, please see license.txt
frappe.ui.form.on('Cliente', {
	// refresh: function(frm) {

	// }
	validate:function(frm){
		if( !validarCedula(frm.doc.cedula)){	
			frappe.throw("Cédula no válida");
		}
		
		
		/*if( frm.doc.telefono.length!=10){
			frappe.throw("Teléfono no válido");
		}*/
		
	}
});
function validarCedula(numero) {          
   
	/* alert(numero); */

	var suma = 0;      
	var residuo = 0;      
	var pri = false;      
	var pub = false;            
	var nat = false;      
	var numeroProvincias = 22;                  
	var modulo = 11;
				
	/* Verifico que el campo no contenga letras */                  
	var ok=1;
	for (var i=0; i<numero.length && ok==1 ; i++){
	   var n = parseInt(numero.charAt(i));
	   if (isNaN(n)) ok=0;
	}
	if (ok==0){        
	   return false;
	}
				
	if (numero.length < 10 ){                         
	   return false;
	}
   
	/* Los primeros dos digitos corresponden al codigo de la provincia */
	var provincia = numero.substr(0,2);      
	if (provincia < 1 || provincia > numeroProvincias){           
   		return false;       
	}

	/* Aqui almacenamos los digitos de la cedula en variables. */
	var d1  = numero.substr(0,1);         
	var d2  = numero.substr(1,1);         
	var d3  = numero.substr(2,1);         
	var d4  = numero.substr(3,1);         
	var d5  = numero.substr(4,1);         
	var d6  = numero.substr(5,1);         
	var d7  = numero.substr(6,1);         
	var d8  = numero.substr(7,1);         
	var d9  = numero.substr(8,1);         
	var d10 = numero.substr(9,1);                
	   
	/* El tercer digito es: */                           
	/* 9 para sociedades privadas y extranjeros   */         
	/* 6 para sociedades publicas */         
	/* menor que 6 (0,1,2,3,4,5) para personas naturales */ 

	if (d3==7 || d3==8){                               
	   return false;
	}         
	   
	/* Solo para personas naturales (modulo 10) */         
	if (d3 < 6){           
		var nat = true;            
		var p1 = d1 * 2;  if (p1 >= 10) p1 -= 9;
		var p2 = d2 * 1;  if (p2 >= 10) p2 -= 9;
		var p3 = d3 * 2;  if (p3 >= 10) p3 -= 9;
		var p4 = d4 * 1;  if (p4 >= 10) p4 -= 9;
		var p5 = d5 * 2;  if (p5 >= 10) p5 -= 9;
		var p6 = d6 * 1;  if (p6 >= 10) p6 -= 9; 
		var p7 = d7 * 2;  if (p7 >= 10) p7 -= 9;
		var p8 = d8 * 1;  if (p8 >= 10) p8 -= 9;
		var p9 = d9 * 2;  if (p9 >= 10) p9 -= 9;             
		var modulo = 10;
	}         

	/* Solo para sociedades publicas (modulo 11) */                  
	/* Aqui el digito verficador esta en la posicion 9, en las otras 2 en la pos. 10 */
	else if(d3 == 6){           
		var pub = true;             
	   p1 = d1 * 3;
	   p2 = d2 * 2;
	   p3 = d3 * 7;
	   p4 = d4 * 6;
	   p5 = d5 * 5;
	   p6 = d6 * 4;
	   p7 = d7 * 3;
	   p8 = d8 * 2;            
	   p9 = 0;            
	}         
	   
	/* Solo para entidades privadas (modulo 11) */         
	else if(d3 == 9) {           
	   var pri = true;                                   
	   p1 = d1 * 4;
	   p2 = d2 * 3;
	   p3 = d3 * 2;
	   p4 = d4 * 7;
	   p5 = d5 * 6;
	   p6 = d6 * 5;
	   p7 = d7 * 4;
	   p8 = d8 * 3;
	   p9 = d9 * 2;            
	}
			  
	var suma = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9;                
	var residuo = suma % modulo;                                         

	/* Si residuo=0, dig.ver.=0, caso contrario 10 - residuo*/
	var digitoVerificador = residuo==0 ? 0: modulo - residuo;                

	/* ahora comparamos el elemento de la posicion 10 con el dig. ver.*/                         
	if (pub==true){           
	   if (digitoVerificador != d9){                                      
		  return false;
	   }                  
	   /* El ruc de las empresas del sector publico terminan con 0001*/         
	   if ( numero.substr(9,4) != '0001' ){                  
		  return false;
	   }
	}         
	else if(pri == true){         
	   if (digitoVerificador != d10){                          
		  return false;
	   }         
	   if ( numero.substr(10,3) != '001' ){                    
		  return false;
	   }
	}      

	else if(nat == true){         
	   if (digitoVerificador != d10){                          
		  return false;
	   }         
	   if (numero.length >10 && numero.substr(10,3) != '001' ){                    
		  return false;
	   }
	}      
	return true;   
}
