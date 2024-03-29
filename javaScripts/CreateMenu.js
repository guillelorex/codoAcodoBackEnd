const URL = "https://guillelorex.pythonanywhere.com/"
// Capturamos el evento de envío del formulario
document.getElementById('formulario').addEventListener('submit', function
(event) {
event.preventDefault(); // Evitamos que se envie el form
var formData = new FormData();
formData.append('idPlatillo', document.getElementById('idPlatillo').value);
formData.append('nombre',document.getElementById('nombre').value);
formData.append('precio', document.getElementById('precio').value);
formData.append('imagen',document.getElementById('imagen').files[0]);
// Realizamos la solicitud POST al servidor
fetch(URL + 'platillo', {
method: 'POST',body: formData // Aquí enviamos formData en lugar de JSON
})
//Después de realizar la solicitud POST, se utiliza el método then() para manejar la respuesta del servidor.

.then(function (response) {
if (response.ok) {
return response.json();
} else {
// Si hubo un error, lanzar explícitamente una excepción
// para ser "catcheada" más adelante
throw new Error('Error al agregar el producto.');
}
})
// Respuesta OK
.then(function () {
// En caso de éxito
alert('Producto agregado correctamente.');
})
.catch(function (error) {
// En caso de error
alert('Error al agregar el producto.');
console.error('Error:', error);
})
.finally(function () {
// Limpiar el formulario en ambos casos (éxito o error)
document.getElementById('idPlatillo').value = "";
document.getElementById('nombre').value = "";
document.getElementById('precio').value = "";
document.getElementById('imagen').value = "";
});
})