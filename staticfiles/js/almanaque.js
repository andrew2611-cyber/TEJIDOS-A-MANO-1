// core/static/js/almanaque.js
// Lógica para el almanaque simple (mes y año, con botones para cambiar)

// core/static/js/almanaque.js
// Lógica para mostrar solo el mes y año actual en mayúsculas, sin botones

document.addEventListener('DOMContentLoaded', function() {
    const meses = [
        'ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO',
        'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE'
    ];
    const mesSpan = document.getElementById('almanaque-mes');
    const anioSpan = document.getElementById('almanaque-anio');
    let fecha = new Date();
    let mes = fecha.getMonth();
    let anio = fecha.getFullYear();
    mesSpan.textContent = meses[mes];
    anioSpan.textContent = anio;
});
