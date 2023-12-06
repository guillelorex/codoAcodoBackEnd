
const URL = "https://guillelorex.pythonanywhere.com/"
const formulario = document.querySelector('#formularioCreateCliente');

// Capturamos el evento de envío del formulario
if (formulario) {document.getElementById('formularioCreateCliente').addEventListener('submit', function(event) {
if (formulario) {document.getElementById('formularioCreateCliente').addEventListener('submit', function(event) {
event.preventDefault(); // Evitamos que se envie el form
var formData = new FormData();
formData.append('idCliente', document.getElementById('idCliente').value);
formData.append('idCliente', document.getElementById('idCliente').value);
formData.append('nombre',document.getElementById('nombre').value);
formData.append('apellido', document.getElementById('apellido').value);
formData.append('apellido', document.getElementById('apellido').value);
formData.append('mail',document.getElementById('mail').value);
formData.append('tipoUsuario',document.getElementById('tipoUsuario').value);
formData.append('tipoUsuario',document.getElementById('tipoUsuario').value);

// Realizamos la solicitud POST al servidor
fetch(URL + 'clientes', {
method: 'POST', body: formData // Aquí enviamos formData en lugar de JSON
fetch(URL + 'clientes', {
method: 'POST', body: formData // Aquí enviamos formData en lugar de JSON
})
//Después de realizar la solicitud POST, se utiliza el método then() para manejar la respuesta del servidor.

.then(function (response) {
if (response.ok) {
return response.json();
} else {
// Si hubo un error, lanzar explícitamente una excepción
// para ser "catcheada" más adelante
throw new Error('Error al agregar el cliente en el front.');
throw new Error('Error al agregar el cliente en el front.');
}
})
// Respuesta OK
.then(function () {
// En caso de éxito
alert('Cliente agregado correctamente.');
alert('Cliente agregado correctamente.');
})
.catch(function (error) {
// En caso de error
alert('Error al agregar el Cliente en el front.');
alert('Error al agregar el Cliente en el front.');
console.error('Error:', error);
})
.finally(function () {
// Limpiar el formulario en ambos casos (éxito o error)
document.getElementById('idCliente').value = "";
document.getElementById('idCliente').value = "";
document.getElementById('nombre').value = "";
document.getElementById('apellido').value = "";
document.getElementById('mail').value = "";
document.getElementById('tipoUsuario').value = "";
document.getElementById('tipoUsuario').value = "";
});
})
}
}