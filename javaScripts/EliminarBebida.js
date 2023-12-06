const URL = "https://guillelorex.pythonanywhere.com/"
const app = Vue.createApp({
data() {
    return {
        bebidas: []
    }
},
methods: {
    obtenerBebidas() {
    // Obtenemos el contenido del inventario
    fetch(URL + 'bebida')
        .then(response => {
        // Parseamos la respuesta JSON
        if (response.ok) { return response.json(); }
        })
        .then(data => {
            // El código Vue itera este elemento para generar la tabla
            this.bebidas = data;
        })
        .catch(error => {
            console.log('Error:', error);
            alert('Error al obtener las bebidas.');
        });
    },
    eliminarBebidas(codigo) {
        if (confirm('¿Estás seguro de que quieres eliminar esta bebida?')) {
            fetch(URL + `bebida/${codigo}`, { method: 'DELETE' })
                .then(response => {
                if (response.ok) {
                    this.bebidas = this.bebidas.filter(bebida => bebida.codigo !== codigo);
                    alert('Bebida eliminada correctamente.');
                }
                })
                .catch(error => {
                    alert(error.message);
                });
        }
    }
},
mounted() {//Al cargar la página, obtenemos la lista de productos
    this.obtenerBebidas();
}
});
app.mount('body'); 