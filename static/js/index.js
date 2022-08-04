var preloader = document.querySelector("#preloader");
window.addEventListener("load", function() {
    //hide the preloader
    preloader.style.display = "none";
    let node = document.querySelector('.preload-transitions');
    node.classList.remove('preload-transitions');
});

