// core/static/js/almanaque-control.js
// Permite cambiar mes/año con flechas del teclado, sin botones visibles

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

    function actualizarAlmanaque() {
        mesSpan.textContent = meses[mes];
        anioSpan.textContent = anio;
    }

    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            mes--;
            if (mes < 0) {
                mes = 11;
                anio--;
            }
            actualizarAlmanaque();
        } else if (e.key === 'ArrowRight') {
            mes++;
            if (mes > 11) {
                mes = 0;
                anio++;
            }
            actualizarAlmanaque();
        } else if (e.key === 'ArrowUp') {
            anio++;
            actualizarAlmanaque();
        } else if (e.key === 'ArrowDown') {
            anio--;
            actualizarAlmanaque();
        }
    });

    actualizarAlmanaque();
});
