const URL = "http://127.0.0.1:5000/"
const app = Vue.createApp({
data() {
    return {
        codigo: '',
        nombre: '',
        apellido: '',
        mail: '',
        tipoUs: '',
        mostrarDatosUsuario: false,
    };
},
methods: {
    obtenerUsuario() {
        fetch(URL + 'usuario/' + this.codigo)
            .then(response => {
            if (response.ok) {
                return response.json()
            } else {
            //Si la respuesta es un error, lanzamos una excepción para ser "catcheada" más adelante en el catch.
                throw new Error('Error al obtener los datos de la bebida.')
                    }
            })
    .then(data => {
        this.nombre = data.nombre;
        this.apellido = data.apellido;
        this.mail = data.mail;
        this.tipoUs = data.tipoUs;
        this.mostrarDatosUsuario = true;
    })
    .catch(error => {
        console.log(error);
        alert('Código no encontrado.');
    })
    },
    seleccionarImagen(event) {
        const file = event.target.files[0];
        this.imagenSeleccionada = file;
        this.imagenUrlTemp = URL.createObjectURL(file); // Crea una URL temporal para la vista previa
    },

    guardarCambios() {
        const formData = new FormData();
        formData.append('nombre', this.nombre);
        formData.append('apellido', this.apellido);
        formData.append('mail', this.mail);
        formData.append('tipoUs', this.tipoUs);
        
    //Utilizamos fetch para realizar una solicitud PUT a la API y guardar los cambios.
        fetch(URL + 'usuario/' + this.codigo, {
            method: 'PUT',
            body: formData,
        })
        .then(response => {
        //Si la respuesta es exitosa, utilizamos response.json() para parsear la respuesta en formato JSON.
            if (response.ok) {
                return response.json()
            } else {
            //Si la respuesta es un error, lanzamos una excepción.
            throw new Error('Error al guardar los cambios del usuario.')
            }
        })
        .then(data => {
            alert('Usuario actualizado correctamente.');
            this.limpiarFormulario();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al actualizar el usuario.');
        });
    },
    limpiarFormulario() {
        this.nombre = '';
        this.apellido = '';
        this.mail = '';
        this.tipoUs = '';
        this.mostrarDatosUsuario = false;
    }
}
});
app.mount('#app');