window.onload = function () {

      var anchoVentana = window.innerWidth

      window.onresize = function(){
        anchoVentana = window.innerWidth;
      };

      var box_izquierdo = document.querySelector(".forma_izquierda");
      var box_derecho = document.querySelector(".forma_derecha");
      box_derecho.addEventListener("mouseover", function () {
        if (anchoVentana > 767){  
          box_derecho.className += "columna forma_derecha col-12 col-md-11"
          box_derecho.style.backgroundColor = "#F9E4A5";
          box_izquierdo.className = "columna forma_izquierda col-12 col-md-1"
          box_izquierdo.style.opacity = "0";
        }
        });
  
      box_derecho.addEventListener("mouseout", function () {
        if (anchoVentana > 767){  
          box_derecho.className += "columna forma_derecha col-12 col-md-6"
          box_derecho.style.backgroundColor = "white";
          box_izquierdo.className = "columna forma_izquierda col-12 col-md-6"
          box_izquierdo.style.opacity = "1";
        }
      });
  
      box_izquierdo.addEventListener("mouseover", function () {
        if (anchoVentana > 767){  
          box_izquierdo.className += "columna forma_derecha col-12 col-md-11"
          box_izquierdo.style.backgroundColor = "#F9E4A5";
          box_derecho.className = "columna forma_izquierda col-12 col-md-1"
          box_derecho.style.opacity = "0";
        }
      });
  
      box_izquierdo.addEventListener("mouseout", function () {
        if (anchoVentana > 767){ 
          box_derecho.className += "columna forma_derecha col-12 col-md-6"
          box_izquierdo.style.backgroundColor = "white";
          box_izquierdo.className = "columna forma_izquierda col-12 col-md-6"
          box_derecho.style.opacity = "1";
        }
      });
};

