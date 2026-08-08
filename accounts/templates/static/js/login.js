document.addEventListener('DOMContentLoaded', function() {
    // Form Elements
    const form = document.getElementById('loginForm');
    const submitBtn = document.getElementById('submitBtn');
    const rememberBtn = document.getElementById('rememberBtn');
    const inputs = document.querySelectorAll('.form-control');

    // Remember functionality
    rememberBtn.addEventListener('click', function(e) {
        e.preventDefault();
        this.classList.toggle('active');
    });

    // Form focus effects
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '#ff6b35';
            this.style.boxShadow = '0 0 15px rgba(255, 107, 53, 0.3)';
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.style.borderColor = 'rgba(255, 255, 255, 0.1)';
                this.style.boxShadow = 'none';
            }
        });

        // Real-time validation
        input.addEventListener('input', function() {
            if (this.value.length > 0) {
                this.style.borderColor = '#28a745';
            } else {
                this.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            }
        });
    });

    // Form submission with loading state
    form.addEventListener('submit', function(e) {
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Loading...';

        // Remove loading state after 5 seconds (fallback)
        setTimeout(function() {
            submitBtn.classList.remove('loading');