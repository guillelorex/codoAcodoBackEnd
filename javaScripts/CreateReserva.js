const URL = "https://guillelorex.pythonanywhere.com/"
// Capturamos el evento de envío del formulario
document.getElementById('formulario').addEventListener('submit', function(event) {
    event.preventDefault(); // Evitamos que se envie el form
    var formData = new FormData();
    formData.append('idCliente', document.getElementById('idCliente').value);
    formData.append('cantPersonas',document.getElementById('cant').value);
    formData.append('fecha',document.getElementById('fecha').value);
// Realizamos la solicitud POST al servidor
fetch(URL + 'reservas', {
    method: 'POST',
    body: formData // Aquí enviamos formData en lugar de JSON
})
//Después de realizar la solicitud POST, se utiliza el método then() para manejar la respuesta del servidor.

.then(function (response) {
    if (response.ok) {
        return response.json();
} else {
// Si hubo un error, lanzar explícitamente una excepción
// para ser "catcheada" más adelante
         throw new Error('Error al agregar la reserva.');
    }
})
// Respuesta OK
.then(function () {
// En caso de éxito
    alert('Reserva agregada correctamente.');
})
.catch(function (error) {
// En caso de error
alert('Error al agregar la reserva.');
console.error('Error:', error);
})
.finally(function () {
// Limpiar el formulario en ambos casos (éxito o error)
document.getElementById('idCliente').value = "";
document.getElementById('fecha').value = "";
document.getElementById('cant').value = "";
});
})