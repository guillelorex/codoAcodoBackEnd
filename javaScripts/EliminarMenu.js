const URL = "http://127.0.0.1:5000/"
const app = Vue.createApp({
data() {
    return {
        menu: []
    }
},
methods: {
    obtenerPlatillos() {
    // Obtenemos el contenido del inventario
    fetch(URL + 'platillo')
        .then(response => {
        // Parseamos la respuesta JSON
        if (response.ok) { return response.json(); }
        })
        .then(data => {
            // El código Vue itera este elemento para generar la tabla
            this.platillos = data;
        })
        .catch(error => {
            console.log('Error:', error);
            alert('Error al obtener los platillos.');
        });
    },
    eliminarPlatillos(codigo) {
        if (confirm('¿Estás seguro de que quieres eliminar este platillo?')) {
            fetch(URL + `platillo/${codigo}`, { method: 'DELETE' })
                .then(response => {
                if (response.ok) {
                    this.platillos = this.platillos.filter(platillo => platillo.codigo !== codigo);
                    alert('Platillo eliminado correctamente.');
                }
                })
                .catch(error => {
                    alert(error.message);
                });
        }
    }
},
mounted() {//Al cargar la página, obtenemos la lista de productos
    this.obtenerPlatillos();
}
});
app.mount('body');