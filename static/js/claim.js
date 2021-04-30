let formCard = document.querySelector('.form-card');
VanillaTilt.init(formCard)

var width = window.matchMedia("(max-width: 700px)")
mobile(width)
width.addListener(mobile)
function mobile(width) {
    if(width.matches){
        formCard.vanillaTilt.destroy()
    }
    else {
        VanillaTilt.init(formCard, )
    }
}
// Animate Background icons
var icns = document.getElementById("icns-div").children;

for (let i = 0; i < icns.length; i++) {
    const element = icns[i];
    anime({
        targets: element,
        translateY: anime.random(-100, -700),
        translateX: anime.random(-50, 50),
        rotateZ: anime.random(-50, 50),
        scale: anime.random(0.5, 1.5),
        opacity: 1,
        delay: 300,
        duration: 2000,
    });
}