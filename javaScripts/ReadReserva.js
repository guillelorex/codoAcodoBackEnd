const URL = "http://127.0.0.1:5000/"
// Realizamos la solicitud GET al servidor para obtener todos los
productos
fetch(URL + 'productos')
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {

                throw new Error('Error al obtener el menu.');
            }
            })
    .then(function (data) {
        let tablaReservas = document.getElementById('tablaMenu');
    for (let reserva of data) {
        let fila = document.createElement('tr');
        fila.innerHTML = '<td>' + reserva.codigo + '</td>' +
        '<td>' + reserva.nombre + '</td>' +
        '<td>' + reserva.fecha + '</td>' +'<td>Cantidad de personas'
        + reserva.personas +'</td>' 

    tablaReservas.appendChild(fila);
    }
    })
    .catch(function (error) {
    // En caso de error
        alert('Error al leer la reserva.');
        console.error('Error:', error);
    })  
