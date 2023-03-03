
document.addEventListener("DOMContentLoaded", () => {
        getData()
    });


//codigo basado en esta pagina: https://www.sitepoint.com/delay-sleep-pause-wait/
function sleep(ms) {return new Promise(resolve => setTimeout(resolve, ms));}

function getData(){
    fetch('/process_notificaciones')
        .then( response => response.json() )
        .then( async data =>  {
            for (var i = 0; i < data.length; i++) {
                if(data[i]["anterior"] != data[i]["actual"]){
                    await sleep(2000)
                    var notify = crear_notificacion(data[i])
                    notificacion(notify[0],notify[1], data[i]["id"])
                }
            }
        });
    }



function notificacion(titulo, mensaje, id){

    var propiedades = {
        body: mensaje,
        icon: "static/img/icono_notificacion.png"
    }

    if(!("Notification" in window)){
        alert("El navegador no soporta notificaciones");
    }else if (Notification.permission === "granted"){
        var notificacion = new Notification(titulo, propiedades)

        notificacion.onclick = (ev) => {
            ev.preventDefault()
            fetch('/actualizar_estados/'+ id)
            .then(response => response.json())
            .then(data =>  window.location.href = '/trabajo/'+ id);
        }
        
    }else if( Notification.permission !== "denied"){
        Notification.requestPermission(function(permission){
            if (Notification.permission === "granted"){
                var notificacion = new Notification(titulo, propiedades) 
                notificacion.onclick = (ev) => {
                    ev.preventDefault()
                    fetch('/actualizar_estados/'+ id)
                    .then(response => response.json())
                    .then(data =>  console.log(data));
                }
            }
        });
    }
}

function crear_notificacion(contenido){
    var titulo = "El trabajo " + contenido["titulo"] + " cambio de estado";
    var mensaje = "Su estado cambio de " + contenido["anterior"] + " a " + contenido["actual"]
    return [titulo, mensaje]
}


