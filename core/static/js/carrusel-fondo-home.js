document.addEventListener('DOMContentLoaded', function () {
    const fondoImgs = document.querySelectorAll('.fondo-carrusel-home');
    const zapatoImgs = document.querySelectorAll('.zapato-carrusel-home');
    const textoCosidas = document.getElementById('texto-cosidas');
    let actual = 0;
    setInterval(() => {
        fondoImgs[actual].classList.remove('activo');
        zapatoImgs[actual].classList.remove('activo');
        textoCosidas.classList.remove('verde');
        if (actual === 1) {
            textoCosidas.classList.add('verde');
        }
        actual = (actual + 1) % fondoImgs.length;
        fondoImgs[actual].classList.add('activo');
        zapatoImgs[actual].classList.add('activo');
    }, 2000); // 2 segundos por imagen
});