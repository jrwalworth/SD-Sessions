$(document).ready(function() {
    $('.register').click(function(){
        $('.reg-content').show();
        $('.login-content').hide();
        $('.register').addClass('active');
        $('.login').removeClass('active');
    });
    $('.login').click(function(){
        $('.login-content').show();
        $('.reg-content').hide();
        $('.login').addClass('active');
        $('.register').removeClass('active');
    });
});