$(document).ready(function() {

    // Target the specific form for post creation
    $('#post-form').on('submit', function(event) {

        // 1. Perform Form Validations (check for empty fields)
        var isValid = true;

        // Check for empty Title field
        if ($('#title').val().trim() === '') {
            $('#title').addClass('is-invalid');
            isValid = false;
        } else {
            $('#title').removeClass('is-invalid');
        }

        // Check for empty Content field
        if ($('#content').val().trim() === '') {
            $('#content').addClass('is-invalid');
            isValid = false;
        } else {
            $('#content').removeClass('is-invalid');
        }

        // 2. Event Handling and UI Effects (hiding/showing elements)
        if (!isValid) {
            // Prevent the default form submission (stops it from reaching Flask)
            event.preventDefault();

            // Show the validation alert message
            $('#validation-alert').removeClass('d-none');

            // Scroll to the top to ensure the user sees the alert
            $('html, body').animate({ scrollTop: 0 }, 'fast');
        } else {
            // Hide alert if validation passes and allow submission
            $('#validation-alert').addClass('d-none');
            // A simple confirmation message could go here before submission, 
            // but for a smooth workflow, we allow the form to submit to Flask.
        }
    });

    // Optional: Clear validation error when the user starts typing
    $('#post-form input, #post-form textarea').on('input', function() {
        if ($(this).hasClass('is-invalid')) {
            $(this).removeClass('is-invalid');
        }
    });

});