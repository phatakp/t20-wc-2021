// Form Input
var inputFocus = function () {
    $(".form-control").focus(function () {
        $(this)[0].placeholder = "";
        $(this).removeClass("is-invalid");
    });
};

inputFocus();