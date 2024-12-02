var nextBtn = document.querySelector('.next'),
    prevBtn = document.querySelector('.prev'),
    carousel = document.querySelector('.carousel'),
    list = document.querySelector('.list'),
    item = document.querySelectorAll('.item'),
    runningTime = document.querySelector('.carousel .timeRunning'),
    navbar = document.querySelector('.nav')

let timeRunning = 1000
let timeAutoNext = 7000

window.addEventListener('scroll', () => {
    // navbar.classList.toggle('fixo', window.scrollY > 0)
    if (window.scrollY > 0){
        navbar.style.backgroundColor = "rgba(0, 0, 0, 0.3)";
        navbar.style.textAlign = "center";
        navbar.style.padding = "1.5em 0 1.5em 0";
    }
    else {
        navbar.style.backgroundColor = "transparent";
        navbar.style.textAlign = "left";
        navbar.style.padding = "1.5em 0 1.5em 5em"
    }
})


//fim nav

nextBtn.onclick = function () {
    showSlider('next')
}

prevBtn.onclick = function () {
    showSlider('prev')
}

let runTimeOut

let runNextAuto = setTimeout(() => {
    nextBtn.click()
}, timeAutoNext)


function resetTimeAnimation() {
    runningTime.style.animation = 'none'
    runningTime.offsetHeight /* trigger reflow */
    runningTime.style.animation = null
    runningTime.style.animation = 'runningTime 7s linear 1 forwards'
}


function showSlider(type) {
    let sliderItemsDom = list.querySelectorAll('.carousel .list .item')
    if (type === 'next') {
        list.appendChild(sliderItemsDom[0])
        carousel.classList.add('next')
    } else {
        list.prepend(sliderItemsDom[sliderItemsDom.length - 1])
        carousel.classList.add('prev')
    }

    clearTimeout(runTimeOut)

    runTimeOut = setTimeout(() => {
        carousel.classList.remove('next')
        carousel.classList.remove('prev')
    }, timeRunning)


    clearTimeout(runNextAuto)
    runNextAuto = setTimeout(() => {
        nextBtn.click()
    }, timeAutoNext)

    resetTimeAnimation() // Reset the running time animation
}

// Start the initial animation 
resetTimeAnimation()






// PERGUNTAS FREQUENTES 
const faqs = document.querySelectorAll(".faq");

faqs.forEach((faq) => {
    faq.addEventListener("click", () => {
        faq.classList.toggle("active");
    });
});
