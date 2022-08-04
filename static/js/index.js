var preloader = document.querySelector("#preloader");
var h1 = document.getElementById("h1heading");
window.addEventListener("load", function() {
    //hide the preloader
    preloader.style.display = "none";
    h1.classList.add("animate");
});
