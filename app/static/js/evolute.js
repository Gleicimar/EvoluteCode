const  Menu = document.querySelector(".menu")
const   nav_menu = document.getElementById('menu')
const  icon  =Menu.querySelector('i')
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

