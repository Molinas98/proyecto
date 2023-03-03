window.onload = function () {
    
    var botonImagen = document.querySelector("#imagen_detalles");
    var contenedorImagen = document.querySelector(".contenedor_imagen");
    if(botonImagen != null){
      botonImagen.addEventListener("click", function () {
        contenedorImagen.style.display = "flex";
      });
      // este codigo esta basado en la siguiente pagina: https://codepen.io/angelthecoder/pen/EJNgVL
      var touchtime = 0;
      var botonPagina = document.querySelector("body");
      var contenedorImagen = document.querySelector(".contenedor_imagen")
      botonPagina.addEventListener("click", function (e) {
        e.preventDefault;
        if (touchtime == 0) {
            touchtime = new Date().getTime();
        } else {
            if (((new Date().getTime()) - touchtime) < 800) {
              contenedorImagen.style.display = "none";
              touchtime = 0;
            } else {
                touchtime = new Date().getTime();
            }
        }
      });
    }
};


function desaparecerboton(){
  var boxMensaje = document.querySelector(".mensaje");
  boxMensaje.remove()
}
