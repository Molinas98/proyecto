document.addEventListener("DOMContentLoaded", () => {

  var fecha = new Date();
  var mes = fecha.getMonth() + 1;
  var dia = fecha.getDate();
  var ano = fecha.getFullYear();
  if (dia < 10) dia = "0" + dia;
  if (mes < 10) mes = "0" + mes;
  var calendario = document.querySelector("#fecha_limite");
  calendario.value = ano + "-" + mes + "-" + dia;

  var myForm = document.getElementById('pedido');
  myForm.onsubmit = function(e){
      // "e" es el evento JS que ocurre cuando enviamos el formulario
      // e.preventDefault() es un método que detiene la naturaleza predeterminada de JavaScript
      e.preventDefault();
      // crea el objeto FormData desde JavaScript y envíalo a través de una solicitud post fetch
      var errores = new Array();
      var form = new FormData(myForm);
      //Validaciones
      var is_valid = true
      if (form.get("titulo").length < 5){
        errores.push("El título debe tener al menos 5 caracteres.")
        is_valid = false
      }
      if (form.get("descripcion").length < 10){
        errores.push("El descripción debe tener al menos 10 caracteres.")
        is_valid = false
      }

      var etiquetaError = document.querySelector("#error")
      if(!is_valid){
        etiquetaError.innerHTML = ""
        for(var i = 0; i < errores.length; i++){
          etiquetaError.innerHTML += "<li>" + errores[i] + "</li>"
        }
        var boxMensaje = document.querySelector(".mensaje-2");
        boxMensaje.style.display = "flex"
        errores = []
        count = 0
      }else{
        //así es como configuramos una solicitud post y enviamos los datos del formulario
        fetch("http://127.0.0.1:5000/dashboard/process", { method :'POST', body : form})
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


function desaparecerboton(){
  var boxMensaje = document.querySelector(".mensaje");
  boxMensaje.remove()
}
