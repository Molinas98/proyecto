document.addEventListener("DOMContentLoaded", () => {
    botones = document.querySelectorAll(".opcion")
    console.log(botones.length)
    for (var i = 0; i < botones.length; i = i + 1){
        botones[i].addEventListener("mouseover", function(){
        this.className += " efecto"
        })
        botones[i].addEventListener("mouseout", function(){
        this.className = "btn text-center opcion"
        })
    }
});

function desaparecerboton(){
    var boxMensaje = document.querySelector(".mensaje");
    boxMensaje.remove()
  }
  