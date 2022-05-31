// const activePath = window.location;
// console.log(activePath);

$(document).ready(function () {
    $('.nav-links > li').click(function (e) {
            $('.nav-links > li').removeClass('active');
        $(this).addClass('active');
    });
});



// Add active class to the current button (highlight it)
// var header = document.getElementById("myDIV");
// var btns = header.getElementsByClassName("btn");
// for (var i = 0; i < btns.length; i++) {
//   btns[i].addEventListener("click", function() {
//   var current = document.getElementsByClassName("active");
//   current[0].className = current[0].className.replace(" active", "");
//   this.className += " active";
//   });
// }