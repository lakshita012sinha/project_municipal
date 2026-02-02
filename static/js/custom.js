// Custom JavaScript for Rajasthan Municipal Login

$(document).ready(function() {
    // Add smooth animations
    $('.box-area').addClass('animate__animated animate__fadeInUp');
    
    // Form validation
    $('form').on('submit', function(e) {
        var username = $('#username').val().trim();
        var password = $('#password').val().trim();
        
        if (username === '' || password === '') {
            e.preventDefault();
            showAlert('Please fill in all required fields.', 'danger');
            return false;
        }
        
        // Show loading state
        var submitBtn = $(this).find('button[type="submit"]');
        var originalText = submitBtn.text();
        submitBtn.html('<i class="ri-loader-4-line"></i> Logging in...').prop('disabled', true);
        
        // Re-enable button after 5 seconds (in case of server delay)
        setTimeout(function() {
            submitBtn.html(originalText).prop('disabled', false);
        }, 5000);
    });
    
    // Remember me functionality
    if (localStorage.getItem('rememberMe') === 'true') {
        $('#formCheck').prop('checked', true);
        $('#username').val(localStorage.getItem('savedUsername') || '');
    }
    
    $('#formCheck').on('change', function() {
        if ($(this).is(':checked')) {
            localStorage.setItem('rememberMe', 'true');
            localStorage.setItem('savedUsername', $('#username').val());
        } else {
            localStorage.removeItem('rememberMe');
            localStorage.removeItem('savedUsername');
        }
    });
    
    // Save username when typing
    $('#username').on('blur', function() {
        if ($('#formCheck').is(':checked')) {
            localStorage.setItem('savedUsername', $(this).val());
        }
    });
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
    
    // Add focus effects
    $('.form-control').on('focus', function() {
        $(this).parent().addClass('focused');
    }).on('blur', function() {
        $(this).parent().removeClass('focused');
    });
    
    // Prevent form submission on Enter in username field (to avoid accidental submission)
    $('#username').on('keypress', function(e) {
        if (e.which === 13) {
            $('#password').focus();
            return false;
        }
    });
});

// Helper function to show alerts
function showAlert(message, type) {
    var alertHtml = '<div class="alert alert-' + type + ' alert-dismissible fade show" role="alert">' +
                    message +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>' +
                    '</div>';
    
    $('.header-text').after(alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);
}

// Add loading animation to images
$(window).on('load', function() {
    $('.featured-image img, .featured-outline img').addClass('loaded');
});

// Add keyboard navigation
$(document).on('keydown', function(e) {
    // Alt + L to focus on login form
    if (e.altKey && e.keyCode === 76) {
        $('#username').focus();
        e.preventDefault();
    }
});