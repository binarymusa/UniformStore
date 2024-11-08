
document.addEventListener('DOMContentLoaded', function(){
    var alert = document.querySelector('.alert');
    setTimeout(function() {
        alert.parentNode.removeChild(alert);
    }, 3000) 
})