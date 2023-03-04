document.addEventListener("DOMContentLoaded", () => {
  var myForm = document.getElementById('registro');
  myForm.onsubmit = function(e){
      // "e" es el evento JS que ocurre cuando enviamos el formulario
      // e.preventDefault() es un método que detiene la naturaleza predeterminada de JavaScript
      e.preventDefault();
      // crea el objeto FormData desde JavaScript y envíalo a través de una solicitud post fetch
      var errores = new Array();
      var form = new FormData(myForm);
      //Validaciones
      EMAIL_REGEX = new RegExp('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
      PASSWORD_REGEX = new RegExp('^(?=.*[A-Z])(?=.*[!@#$&+*])(?=.*[0-9])(?=.*[a-z]).{5,30}$')
      CELULAR_REGEX = new RegExp('^[0-9]{10}$')
      var is_valid = true

      if (!form.get("email").match(EMAIL_REGEX)){
        errores.push("El formato de email no es válido.");
        is_valid = false
      }
      if (form.get("nombre").length < 2){
        errores.push("El nombre debe tener al menos 2 caracteres.")
        is_valid = false
      }
      if (form.get("apellido").length < 2){
        errores.push("El apellido debe tener al menos 2 caracteres.")
        is_valid = false
      }
      if (!form.get("celular").match(CELULAR_REGEX)){
        errores.push("El formato de celular no es válido, empieza del 0 y no agregues espacios.");
        is_valid = false
      }
      if (!form.get("password").match(PASSWORD_REGEX)){
        errores.push("La contraseña debe contener entre 5 y 30 letras: 1 carácter numérico, 1 letra mayúscula, 1 letra minuscula y un carácter especial.")
        is_valid = false
      }
      if (form.get('password') != form.get('re_password')){
        errores.push("Las contraseñas no coiciden.")
        is_valid = false
      }

      var etiquetaError = document.querySelector("#error")
      if(!is_valid){
        etiquetaError.innerHTML = ""
        for(var i = 0; i < errores.length; i++){
          etiquetaError.innerHTML += "<li>" + errores[i] + "</li>"
        }
        var boxMensaje = document.querySelector(".mensaje-2")
        boxMensaje.style.display = "flex"
        errores = []
        count = 0
      }else{
        //así es como configuramos una solicitud post y enviamos los datos del formulario
        fetch("/process", { method :'POST', body : form})
        .then(response => {
          if (response.redirected) {
            window.location.assign(response.url)
          } else {
            response.json().then(data => {
                etiquetaError.innerHTML = ""
                etiquetaError.innerHTML += "<li>" + data.mensaje + "</li>"
                var boxMensaje = document.querySelector(".mensaje-2")
                boxMensaje.style.display = "flex"
            });
          }
        })
      }
      
      var botonAceptar2 = document.querySelector("#aceptar-2");
      var boxMensaje2 = document.querySelector(".mensaje-2");
      botonAceptar2.addEventListener("click", function () {
        boxMensaje2.style.display = "none";
      });

  }
});
