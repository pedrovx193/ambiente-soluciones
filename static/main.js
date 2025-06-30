document.addEventListener("DOMContentLoaded", () => {//el arbol DOM ya esta construido para usarlo
  // === Carrusel ===
  const track = document.querySelector(".carousel-track");//busco en html el primer elemento que tenga la clase carousel-track y lo guarda en una variable track
  if (track) {//verifico si la variable track es valida
    const prevBtn = document.querySelector(".carousel-btn.prev");//busco el boton flecha izquierda verifico en el html
    const nextBtn = document.querySelector(".carousel-btn.next");//busco el boton flecha derecha verifico en el html

    const scrollAmount = track.offsetWidth * 0.7;//calcula el desplazamiento del carrusel en este caso se mueve el 70% del carrusel
    prevBtn.addEventListener("click", () => {//agrego el evento al btn izq (- desplaza atras) smooth (desplazato animado)
      track.scrollBy({ left: -scrollAmount, behavior: "smooth" });//animar el desplazamiento izquierdo
    });
    nextBtn.addEventListener("click", () => {//agrego el evento al boton derecho
      track.scrollBy({ left: scrollAmount, behavior: "smooth" });//animar el desplazamiento derecho
    });
  }

   
});

  // Banner de bienvenida
  const toast = document.createElement('div');
  toast.textContent = "¡Bienvenido a Ambiente Soluciones!";
  toast.style.position = 'fixed';
  toast.style.top = '4%';
  toast.style.left = '50%';
  toast.style.transform = 'translate(-50%, -50%)';
  toast.style.background = 'rgba(0, 0, 0, 0.7)';
  toast.style.color = 'yellow';
  toast.style.padding = '20px 40px';
  toast.style.borderRadius = '8px';
  toast.style.zIndex = 1000;
  toast.style.fontSize = '1.3rem';
  toast.style.textAlign = 'center';
  toast.style.boxShadow = '0 4px 12px rgba(0,0,0,0.4)';
  document.body.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3000);//duracion del toast 3000 milisegundos
