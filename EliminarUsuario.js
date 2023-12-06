const URL = "https://guillelorex.pythonanywhere.com/"
const app = Vue.createApp({
    data() {
        return {
            clientes: []
        }
},
methods: {
    obtenerCliente() {
    // Obtenemos el contenido del inventario
        fetch(URL + 'clientes')
            .then(response => {
            // Parseamos la respuesta JSON
            if (response.ok) { return response.json(); }
            })
            .then(data => {
                // El código Vue itera este elemento para generar la tabla
                this.clientes = data;
            })
            .catch(error => {
                console.log('Error:', error);
                alert('Error al obtener el cliente.');
            });
    },
    eliminarCliente(codigo) {
        if (confirm('¿Estás seguro de que quieres eliminar este cliente?')) {
            fetch(URL + `clientes/${codigo}`, { method: 'DELETE' })
                .then(response => {
                if (response.ok) {
                    this.clientes = this.clientes.filter(cliente => cliente.codigo !== codigo);
                    alert('Cliente eliminado correctamente.');
                }
                })
                .catch(error => {
                    alert(error.message);
                });
        }
    }
},
mounted() {//Al cargar la página, obtenemos la lista de productos
    this.obtenerCliente();
}
});
app.mount('body'); 