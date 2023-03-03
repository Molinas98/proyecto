
    document.addEventListener("DOMContentLoaded", () => {
      
      /*//codigo basado en el codigo brindado por Alejandra Silva */
      const cuadroBusqueda = document.querySelector("#titulo")
      const fecha_inicio = document.querySelector("#fecha_inicio")
      const fecha_fin = document.querySelector("#fecha_fin")
      const filas = document.querySelectorAll(".cuerpo_historial > a");
      const titulos = Array.from(filas).map(
        (row) => row.querySelectorAll("div")[0]
      );

      const fechas = Array.from(filas).map(
        (row) => row.querySelectorAll("div")[2]
      );
      
      
      function filtrar_datos(){
            const searchQuery = cuadroBusqueda.value.toLowerCase();
            for (const titulo of titulos) {
              const row = titulo.closest("a");
              const titulo_dato = titulo.textContent.toLowerCase();
              row.style.display = "flex";
      
              if (titulo_dato.search(searchQuery) === -1)
                row.style.display = "none";
              
            }
            
            const fechaInicio = Date.parse(fecha_inicio.value);
            const fechaFin = Date.parse(fecha_fin.value);
      
            for (const fecha of fechas) {
              const row = fecha.closest("a");
              const fecha_dato = Date.parse(fecha.textContent);
      
              if( fecha_dato < fechaInicio || fecha_dato > fechaFin)
                  row.style.display = "none";
            }
          }
      
          cuadroBusqueda.addEventListener("input", () => {
            filtrar_datos()
          });
      
          fecha_inicio.addEventListener("input", () => {
            filtrar_datos()
          });

          fecha_fin.addEventListener("input", () => {
            filtrar_datos()
          });

          var myForm = document.getElementById('busqueda');
          myForm.onsubmit = function(e){
              e.preventDefault();
              filtrar_datos()
          }

      });

      window.onload = function () {

        var fecha = new Date();
        var mes = fecha.getMonth() + 1;
        var dia = fecha.getDate();
        var dia_siguente = fecha.getDate() +1;
        var ano = fecha.getFullYear();
        if (dia < 10) dia = "0" + dia;
        if (dia_siguente < 10) dia_siguente = "0" + dia_siguente;
        if (mes < 10) mes = "0" + mes;
        var inicio = document.querySelector("#fecha_inicio");
        var fin = document.querySelector("#fecha_fin");
        inicio.value = ano + "-" + mes + "-" + dia;
        fin.value = ano + "-" + mes + "-" + dia_siguente;
    };
