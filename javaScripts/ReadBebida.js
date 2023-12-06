const URL = "https://guillelorex.pythonanywhere.com/"
// Realizamos la solicitud GET al servidor para obtener todos los productos
fetch(URL + 'bebidas')
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {

                throw new Error('Error al obtener el menu.');
            }
            })
    .then(function (data) {
        let tablaBebida = document.getElementById('tablaBebida');
    
        for (let bebida of data) {
        let fila = document.createElement('tr');
        fila.innerHTML = '<td>' + bebida.idBebida + '</td>' +
        '<td>' + bebida.nombre + '</td>' +
        '<td align="right">' + bebida.precio + '</td>' +
        '<td><img src="static/imagenes/' + bebida.imagen + '" alt="Imagen del producto" style="width: 100px;"></td>'; // Corregida la URL de la imagen

    tablaBebida.appendChild(fila);
    }
    })
    .catch(function (error) {
    // En caso de error
        alert('Error al leer la bebida.');
        console.error('Error:', error);
    })  