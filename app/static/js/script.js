// Ensure the document is ready before executing scripts
$(document).ready(function () {
    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Form validation
    $('form').on('submit', function (event) {
        var isValid = true;
        $(this).find('input, textarea').each(function () {
            if ($(this).prop('required') && $(this).val() === '') {
                isValid = false;
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        if (!isValid) {
            event.preventDefault();
            alert('Please fill in all required fields.');
        }
    });

    // AJAX form submission
    $('form.ajax-form').on('submit', function (event) {
        event.preventDefault();
        var form = $(this);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                alert('Form submitted successfully!');
                form.trigger('reset');
            },
            error: function (response) {
                alert('An error occurred. Please try again.');
            }
        });
    });

    // Add a new form field dynamically
    $('#add-field').on('click', function () {
        var formFields = $('#form-fields');
        var newField = `
            <div class="form-group">
                <label for="field_name">Field Name</label>
                <input type="text" class="form-control" name="field_name[]" placeholder="Enter field name" required>
                <label for="field_type">Field Type</label>
                <select class="form-control" name="field_type[]">
                    <option value="text">Text</option>
                    <option value="email">Email</option>
                    <option value="number">Number</option>
                    <option value="date">Date</option>
                </select>
                <button type="button" class="btn btn-danger remove-field">Remove Field</button>
            </div>`;
        formFields.append(newField);
    });

    // Remove a form field dynamically
    $(document).on('click', '.remove-field', function () {
        $(this).closest('.form-group').remove();
    });


    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function (event) {
        var target = this.hash;
        event.preventDefault();
        var navOffset = $('.navbar').height();
        $('html, body').animate({
            scrollTop: $(target).offset().top - navOffset
        }, 800, function () {
            window.location.hash = target;
        });
    });

    // Animated button click effect
    $('.btn').on('mousedown', function (e) {
        var ripple = $('<span class="ripple"></span>');
        var x = e.pageX - $(this).offset().left;
        var y = e.pageY - $(this).offset().top;
        ripple.css({ top: y + 'px', left: x + 'px' });
        $(this).append(ripple);
        setTimeout(function () {
            ripple.remove();
        }, 600);
    });

    // Toggle visibility for password fields
    $('.toggle-password').on('click', function () {
        var input = $($(this).attr('toggle'));
        if (input.attr('type') === 'password') {
            input.attr('type', 'text');
        } else {
            input.attr('type', 'password');
        }
        $(this).toggleClass('fa-eye fa-eye-slash');
    });
});
