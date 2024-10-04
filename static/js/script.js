const switchT = document.querySelector('.switch')
      switchToggle = document.querySelector('.toggle-switch'),
      root = document.querySelector(':root')
      menuBtn = document.querySelector('.bx-chevron-left')
      sideBar = document.querySelector('.side-bar')
      home = document.querySelector('.home')
      textos = document.querySelectorAll('.opacity')
      setasDrop = document.querySelectorAll('.bx-chevron-up')
      dropItens = document.querySelectorAll('#drop-itens')

let modeStatus = localStorage.getItem('status')
if (modeStatus === 'fechado'){
    sideBar.classList.toggle('close')
    home.classList.toggle('close')
    dropItens.forEach(element => {
        element.classList.remove('mostrar')
    })
    verificarJanela()
}

let modeTheme = localStorage.getItem('mode')
if (modeTheme === 'dark'){
    switchT.classList.add('active')
    root.classList.add('dark')
}

switchT.addEventListener('click', () => {
    switchT.classList.toggle('active')
    root.classList.toggle('dark')
    setTimeout(function(){
        if (switchT.classList.contains('active')){
            localStorage.setItem('mode', 'dark')
        } else {
            localStorage.setItem('mode', 'light')
        }
    }, 100)
})

menuBtn.addEventListener('click', () => {
    sideBar.classList.toggle('close')
    home.classList.toggle('close')
    menuBtn.classList.add('close')
    dropItens.forEach(element => {
        element.classList.remove('mostrar')
    })
    setTimeout(function(){
        if (sideBar.classList.contains('close')){
            localStorage.setItem('status', 'fechado')
            textos.forEach(element => {
                element.style.opacity = 0
            });
            setasDrop.forEach(element => {
                element.style.opacity = 0
            });
            switchToggle.style.right = "unset"
            menuBtn.classList.add('close')
        } else {
            localStorage.setItem('status', 'aberto')
            textos.forEach(element => {
                element.style.opacity = 1
            });
            setasDrop.forEach(element => {
                element.style.opacity = 1
            })
            switchToggle.style.right = 0
            menuBtn.classList.remove('close')
        }
    }, 1)
})

function verificarJanela(){
    if (sideBar.classList.contains('close')){
        textos.forEach(element => {
            element.style.opacity = 0
        });
        setasDrop.forEach(element => {
            element.style.opacity = 0
        });
        switchToggle.style.right = "unset"
        menuBtn.classList.add('close')
    } else {
        textos.forEach(element => {
            element.style.opacity = 1
        });
        setasDrop.forEach(element => {
            element.style.opacity = 1
        })
        switchToggle.style.right = 0
        menuBtn.classList.remove('close')
    }
}

function abrirDrop(ambiente){
    document.querySelector(`.menu-item.${ambiente}`).classList.toggle('mostrar')
    document.querySelector(`.menu-${ambiente}`).classList.toggle('mostrar')
    if (sideBar.classList.contains('close')){
        sideBar.classList.remove('close')
        home.classList.remove('close')
        setTimeout(verificarJanela(), 100)
    }
}

particlesJS("particles-js", {
    "particles":{
        "number":{"value":40,
            "density":{"enable":true,"value_area":800}
        },
        "color":{"value":"#ffffff"},
        "shape":{
            "type":"circle",
            "stroke":{"width":0,"color":"#000000"},
            "polygon":{"nb_sides":5},
            "image":{"src":"img/github.svg","width":100,"height":100}
        },
        "opacity":{
            "value":0.5,
            "random":false,
            "anim":{"enable":false,"speed":1,"opacity_min":0.1,"sync":false}
        },
        "size":{
            "value":3,
            "random":true,
            "anim":{
                "enable":false,
                "speed":40,
                "size_min":0.1,
                "sync":false}
        },
        "line_linked":{
            "enable":true,
            "distance":150,
            "color":"#ffffff",
            "opacity":0.4,
            "width":1
        },
        "move":{
            "enable":true,
            "speed":4,
            "direction":"top",
            "random":false,
            "straight":false,
            "out_mode":"out",
            "bounce":false,
            "attract":{
                "enable":false,
                "rotateX":600,
                "rotateY":1200}
         }
    },
    "interactivity":{
        "detect_on":"canvas",
        "events":{
            "onhover":{
                "enable":false,
                "mode":"repulse"},
            "onclick":{
                "enable":false,
                "mode":"push"},
            "resize":true
        },
        "modes":{
            "grab":{
                "distance":400,
                "line_linked":{"opacity":1}
            },
            "bubble":{
                "distance":400,
                "size":40,
                "duration":2,
                "opacity":8,
                "speed":3
            },
            "repulse":{
                "distance":200,
                "duration":0.4
            },
            "push":{"particles_nb":4},
            "remove":{"particles_nb":2}
        }
    },
    "retina_detect":true});