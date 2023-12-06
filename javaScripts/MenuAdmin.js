const URL = "https://guillelorex.pythonanywhere.com/"

function retrieveDrinks() {
    fetch(URL + 'bebidas')
    .then(function (response) {
        if (response.ok) {
            return response.json();
        } else {

                throw new Error('Error al obtener el menu.');
            }
            })
    .then(function (data) {
        buildTableBebida(data);
    })
    .catch(function (error) {
    // En caso de error
        alert('Error al leer la bebida.');
        console.error('Error:', error);
    }) 
} 

function hideClearButton() {
    var b = document.querySelector("#clear-button");
    if (!b.classList.contains("hide")) {
        b.classList.toggle("hide");
    }
}

function hideViewButton() {
    var b = document.querySelector("#view-button");
    if (!b.classList.contains("hide")) {
        b.classList.toggle("hide");
    }
}

function clearTable() {
    document.querySelector("#tablaBebida").innerHTML = ""; 
    hideClearButton();
    showViewButton();
}

function showClearButton() {
    var b = document.querySelector("#clear-button");
    b.classList.toggle("hide");
}

function showViewButton() {
    var b = document.querySelector("#view-button");
    b.classList.toggle("hide");
}

function buildTableBebida(data) {
    clearTable();
    let tablaBebida = document.getElementById('tablaBebida');

    for (let bebida of data) {
        let fila = document.createElement('tr');
        fila.innerHTML = '<td>' + bebida.idBebida + '</td>' +
            '<td>' + bebida.nombre + '</td>' +
            '<td align="right">' + bebida.precio + '</td>' +
            '<td><img src="static/imagenes/' + bebida.imagen + '" alt="Imagen del producto" style="width: 100px;"></td>';

        tablaBebida.appendChild(fila);
    }
    hideViewButton();
    showClearButton();
}

function mostrarFormCrear() {
    hideCrearButton();
    var b = document.querySelector("#container-form");
    b.classList.toggle("hide");
}

function hideCrearButton() {
    var b = document.querySelector("#crear-button");
    if (!b.classList.contains("hide")) {
        b.classList.toggle("hide");
    }
}

function ocultarFormCrear() {
    var b = document.querySelector("#container-form");
    if (!b.classList.contains("hide")) {
        b.classList.toggle("hide");
    }
    var c = document.querySelector("#crear-button");
    c.classList.toggle("hide");
}