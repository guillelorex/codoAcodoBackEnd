const URL = "https://guillelorex.pythonanywhere.com/"
// Realizamos la solicitud GET al servidor para obtener todos los productos
fetch(URL + 'platillos')
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {

                throw new Error('Error al obtener el menu.');
            }
            })
    .then(function (data) {
        let tablaMenu = document.getElementById('tablaMenu');
    for (let menu of data) {
        let fila = document.createElement('tr');
        fila.innerHTML = '<td>' + menu.idPlatillo + '</td>' +
        '<td>' + menu.nombre + '</td>' +
        '<td align="right">' + menu.precio + '</td>' +'<td><img src=static/img/'
        + menu.imagen_url +'alt="Imagen del producto" style="width: 100px;"></td>' 

    //tablaMenu.appendChild(fila);
    }
    })
    .catch(function (error) {
    // En caso de error
        alert('Error al leer el menu.');
        console.error('Error:', error);
 })   
