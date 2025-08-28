document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.icono-estrella').forEach(function(estrella) {
        estrella.addEventListener('click', function() {
            const productoId = this.getAttribute('data-producto-id');
            const esFavorito = this.classList.contains('favorito-activo');
            const url = esFavorito ? `/favoritos/quitar/${productoId}/` : `/favoritos/agregar/${productoId}/`;
            fetch(url, {method: 'POST', headers: {'X-CSRFToken': getCookie('csrftoken')}})
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        this.classList.toggle('favorito-activo');
                    }
                });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
