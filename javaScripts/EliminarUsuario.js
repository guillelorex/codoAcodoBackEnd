const URL = "http://127.0.0.1:5000/"
const app = Vue.createApp({
data() {
    return {
        usuarios: []
    }
},
methods: {
    obtenerUsuario() {
    // Obtenemos el contenido del inventario
    fetch(URL + 'usuario')
        .then(response => {
        // Parseamos la respuesta JSON
        if (response.ok) { return response.json(); }
        })
        .then(data => {
            // El código Vue itera este elemento para generar la tabla
            this.usuario = data;
        })
        .catch(error => {
            console.log('Error:', error);
            alert('Error al obtener el usuario.');
        });
    },
    eliminarUsuario(codigo) {
        if (confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
            fetch(URL + `usuario/${codigo}`, { method: 'DELETE' })
                .then(response => {
                if (response.ok) {
                    this.usuario = this.usuario.filter(usuarios => usuarios.codigo !== codigo);
                    alert('Usuario eliminado correctamente.');
                }
                })
                .catch(error => {
                    alert(error.message);
                });
        }
    }
},
mounted() {//Al cargar la página, obtenemos la lista de productos
    this.obtenerUsuario();
}
});
app.mount('body');