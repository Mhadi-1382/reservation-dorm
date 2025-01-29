var slides=document.getElementsByClassName("slide");
var prev=document.querySelector(".prev");
var next=document.querySelector(".next");
var n=0;

function displaynone(){
    for(let i=0;i<slides.length;i++){
        slides[i].style.display='none';
    }
}

function noActive(){
    for(let i=0;i<slides.length;i++){
        slides[i].classList.remove('active');
    }
}

next.addEventListener("click",function(){
    n++;
    if(n>slides.length-1){
        n=0;
    }
    displaynone();
    noActive();
    slides[n].style.display='block';
    slides[n].classList.add('active');
});

prev.addEventListener("click",function(){
    n--;
    if(n<0){
        n=slides.length-1;
    }
    displaynone();
    noActive();
    slides[n].style.display='block';
    slides[n].classList.add('active');
});

setInterval(function(){
    n++;
    if(n>slides.length-1){
        n=0;
    }
    displaynone();
    noActive();
    slides[n].style.display='block';
    slides[n].classList.add('active');
}, 4000);


