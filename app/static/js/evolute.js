const  Menu = document.querySelector(".menu")
const   nav_menu = document.getElementById('menu')
const  icon  = Menu.querySelector('i')

Menu.addEventListener("click", ()=>{
    nav_menu.classList.toggle("active")
    if (icon.classList.contains('fa-bars')){
        icon.classList.remove('fa-bars');
        icon.classList.add("fa-times");
    }else{
        icon.classList.remove("fa-times");
        icon.classList.add("fa-bars");

    }

})

/*fechar mensagem */

  // Espera 4 segundos e remove a mensagem flash
  setTimeout(function() {
    const flashes = document.querySelectorAll('.flashes li');
    flashes.forEach(function(flash) {
      flash.style.transition = "opacity 1s ease-out";
      flash.style.opacity = "0";
      setTimeout(() => flash.remove(), 1000); // remove do DOM após desaparecer
    });
  }, 4000); // tempo em milissegundos (4000ms = 4 segundos)
