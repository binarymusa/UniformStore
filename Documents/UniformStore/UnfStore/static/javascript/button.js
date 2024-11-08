
// connected to the login page
window.addEventListener('DOMContentLoaded', function() {
    const button = document.querySelector('#btn-1')

    function redirect(){
        window.location.href = '/sign_up_page'
    }
    button.addEventListener('click', function() {
        redirect();
    });

})