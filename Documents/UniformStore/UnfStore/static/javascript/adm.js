
const key = document.querySelector('#key');

key.addEventListener('animationend', () => {
    window.location.href = '/Admin_page';
});

/* window.addEventListener('animationend', function(){
    const key = this.document.querySelector('#key');
    window.location.href = 'Admin_page';
}); */