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
        let tablaBebida = document.getElementById('tablaMenu');
    for (let bebida of data) {
        let fila = document.createElement('tr');
        fila.innerHTML = '<td>' + bebida.codigo + '</td>' +
        '<td>' + bebida.nombre + '</td>' +
        '<td align="right">' + bebida.precio + '</td>' +'<td><img src=static/img/'
        + bebida.imagen_url +'alt="Imagen del producto" style="width: 100px;"></td>' 

    tablaBebida.appendChild(fila);
    }
    })
    .catch(function (error) {
    // En caso de error
        alert('Error al leer la bebida.');
        console.error('Error:', error);
    })  