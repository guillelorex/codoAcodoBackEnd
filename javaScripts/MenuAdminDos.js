function retrieveFood() {  
    fetch(URL + 'platillos')
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {
                throw new Error('Error al obtener el menu.');
            }
            })
    .then(function (data) {
        buildTablePlatillo(data);
    })
    .catch(function (error) {
    // En caso de error
        alert('Error al leer el menu.');
        console.error('Error:', error);
    })   
}

function hideClearbuttonDos() {
    var b = document.querySelector("#clear-buttonDos");
    if (!b.classList.contains("hide")) {
        b.classList.toggle("hide");
    }
}

function hideViewbuttonDos() {
    var b = document.querySelector("#view-buttonDos");
    if (!b.classList.contains("hide")) {
        b.classList.toggle("hide");
    }
}


function clearTableDos() {
    document.querySelector("#tablaMenu").innerHTML = ""; 
    hideClearbuttonDos();
    showViewbuttonDos();
}

function showClearbuttonDos() {
    var b = document.querySelector("#clear-buttonDos");
    b.classList.toggle("hide");
}

function showViewbuttonDos() {
    var b = document.querySelector("#view-buttonDos");
    b.classList.toggle("hide");
}

function buildTablePlatillo(data) {
    clearTableDos();
    let tablaMenu = document.getElementById('tablaMenu');

    for (let platillo of data) {
        let fila = document.createElement('tr');
        fila.innerHTML = '<td>' + platillo.idPlatillo + '</td>' +
            '<td>' + platillo.nombre + '</td>' +
            '<td align="right">' + platillo.precio + '</td>' +
            '<td><img src="static/img/' + platillo.imagen_url + '" alt="Imagen del producto" style="width: 100px;"></td>';

        tablaMenu.appendChild(fila);
    }
    hideViewbuttonDos();
    showClearbuttonDos();
}