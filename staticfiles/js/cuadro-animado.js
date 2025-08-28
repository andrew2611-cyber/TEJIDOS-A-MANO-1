// Sincroniza el color del cuadro animado con el estado del texto COSIDAS
// Este script debe ser cargado solo en la página de inicio

document.addEventListener('DOMContentLoaded', function () {
    const textoCosidas = document.getElementById('texto-cosidas');
    const cuadroAnimado = document.getElementById('cuadro-animado');
    if (!textoCosidas || !cuadroAnimado) return;
    function syncCuadroColor() {
        if (textoCosidas.classList.contains('verde')) {
            cuadroAnimado.style.background = '#fb8609'; // Amarillo solicitado
        } else {
            cuadroAnimado.style.background = '#6c2eb6'; // Morado
        }
    }
    // Inicial
    syncCuadroColor();
    // Observa cambios de clase en textoCosidas
    const observer = new MutationObserver(syncCuadroColor);
    observer.observe(textoCosidas, { attributes: true, attributeFilter: ['class'] });
});
