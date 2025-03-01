// Theme Toggler
(() => {
    'use strict'
  
    const getStoredTheme = () => localStorage.getItem('theme')
    const setStoredTheme = theme => localStorage.setItem('theme', theme)
  
    const getPreferredTheme = () => {
        const storedTheme = getStoredTheme()
        if (storedTheme) {
            return storedTheme
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
  
    const setTheme = theme => {
        if (theme === 'auto') {
            document.documentElement.setAttribute('data-bs-theme', 
                window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
            )
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme)
        }
    }
  
    const showActiveTheme = (theme, focus = false) => {
        const themeSwitcher = document.querySelector('[data-bs-theme-value]')
        if (!themeSwitcher) return
        
        const activeThemeIcon = document.querySelector('[data-theme-icon-active]')
        const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`)
        
        document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
            element.classList.remove('active')
            element.setAttribute('aria-pressed', 'false')
        })
        
        btnToActive.classList.add('active')
        btnToActive.setAttribute('aria-pressed', 'true')
        
        const themeSwitcherLabel = `${btnToActive.textContent} mode`
        themeSwitcher.setAttribute('aria-label', themeSwitcherLabel)
        
        if (focus) themeSwitcher.focus()
        
        // Update the active icon
        const activeThemeIconClass = btnToActive.querySelector('i').className
        activeThemeIcon.className = activeThemeIconClass
    }
  
    // Set initial theme
    setTheme(getPreferredTheme())
  
    // Show active theme
    window.addEventListener('DOMContentLoaded', () => {
        showActiveTheme(getPreferredTheme())
        
        // Add click handlers to theme buttons
        document.querySelectorAll('[data-bs-theme-value]')
            .forEach(toggle => {
                toggle.addEventListener('click', () => {
                    const theme = toggle.getAttribute('data-bs-theme-value')
                    setStoredTheme(theme)
                    setTheme(theme)
                    showActiveTheme(theme, true)
                })
            })
    })
})();

// HTMX Configuration and Extensions
document.addEventListener('DOMContentLoaded', () => {
    // Initialize HTMX extensions
    htmx.logAll();  // Enable debug logging
    htmx.config.historyCacheSize = 10;  // Limit history cache size
    htmx.config.refreshOnHistoryMiss = true;  // Refresh content on history miss
    
    // Add loading states extension
    htmx.defineExtension('loading-states', {
        onEvent: function(name, evt) {
            let elt = evt.detail.elt;
            if (name === 'htmx:beforeRequest') {
                elt.classList.add('htmx-request');
            } else if (name === 'htmx:afterRequest') {
                elt.classList.remove('htmx-request');
            }
        }
    });
});

// Bootstrap Initialization
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(el => new bootstrap.Tooltip(el))
    
    // Initialize all popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(el => new bootstrap.Popover(el))
});

// Form Helpers
const forms = {
    validate: (form) => {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    },
    
    clearValidation: (form) => {
        form.classList.remove('was-validated');
    },
    
    handleSubmit: (event) => {
        const form = event.target;
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        form.classList.add('was-validated');
    }
};

// Add form validation listeners
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', forms.handleSubmit, false);
    });
});

// Utility Functions
const utils = {
    formatDateTime: (dateString) => {
        return new Date(dateString).toLocaleString();
    },
    
    formatDate: (dateString) => {
        return new Date(dateString).toLocaleDateString();
    },
    
    formatNumber: (number) => {
        return new Intl.NumberFormat().format(number);
    },
    
    copyToClipboard: (text) => {
        navigator.clipboard.writeText(text).then(() => {
            // Show success message
            const toast = new bootstrap.Toast(document.getElementById('clipboard-toast'));
            toast.show();
        });
    }
};