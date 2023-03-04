document.addEventListener("DOMContentLoaded", () => {

    var anchoVentana = window.innerWidth

    window.onresize = function(){
      anchoVentana = window.innerWidth;
    };
    botones = document.querySelectorAll(".opcion")
    if (anchoVentana > 767){  
        for (var i = 0; i < botones.length; i = i + 1){
            botones[i].addEventListener("mouseover", function(){
                this.className += " efecto"
            })
            botones[i].addEventListener("mouseout", function(){
                this.className = "btn text-center opcion"
            })
        }
    }else{
        for (var i = 0; i < botones.length; i = i + 1){
            botones[i].addEventListener("touchstart", function(){
                this.style.backgroundColor = "#1047EF"
                this.style.color = "white"

            })

            botones[i].addEventListener("touchend", function(){
                this.style.backgroundColor = "white"
                this.style.color = "#1047EF"
            })
        }
    }
});

function desaparecerboton(){
    var boxMensaje = document.querySelector(".mensaje");
    boxMensaje.remove()
}
  