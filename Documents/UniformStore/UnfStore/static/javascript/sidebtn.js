// const btn1 = document.querySelector('#hb1');
// const btn2 = document.querySelector('#hb2');
// const lts1 = document.querySelector('#light1');
// const lts2 = document.querySelector('#light2');

btn1.addEventListener('mouseenter', function(){
    lts1.classList.toggle('new');
});
btn1.addEventListener('mouseleave', function(){
    lts1.classList.toggle('');
});
btn2.addEventListener('mouseenter', function(){
    lts2.classList.toggle('new');
});
btn2.addEventListener('mouseleave', function(){
    lts2.classList.toggle('');
});


