document.addEventListener('DOMContentLoaded', function() {
    var enBtn = document.getElementById('lang-en');
    var frBtn = document.getElementById('lang-fr');
    var currentLang = localStorage.getItem('language') || 'en';

    function switchLanguage(lang) {
        localStorage.setItem('language', lang);
        document.documentElement.lang = lang;

        // Handle search input placeholder
        var searchInput = document.querySelector('input[name="search"]');
        if (searchInput) {
            var frPlaceholder = searchInput.getAttribute('data-fr-placeholder');
            var enPlaceholder = searchInput.getAttribute('data-en-placeholder');
            if (frPlaceholder && enPlaceholder) {
                searchInput.placeholder = lang === 'fr' ? frPlaceholder : enPlaceholder;
            }
        }

        // Handle select options with data-en/data-fr attributes
        var allOptions = document.querySelectorAll('option[data-en][data-fr]');
        for (var i = 0; i < allOptions.length; i++) {
            var opt = allOptions[i];
            opt.textContent = lang === 'fr' ? opt.getAttribute('data-fr') : opt.getAttribute('data-en');
        }

        // Handle dynamic subcategory options
        if (window.updateFormLanguage) {
            window.updateFormLanguage(lang);
        }

        // Update button styles
        if (enBtn) {
            enBtn.style.background = lang === 'en' ? 'var(--primary)' : 'transparent';
            enBtn.style.color = lang === 'en' ? 'white' : 'var(--text-secondary)';
        }
        if (frBtn) {
            frBtn.style.background = lang === 'fr' ? 'var(--primary)' : 'transparent';
            frBtn.style.color = lang === 'fr' ? 'white' : 'var(--text-secondary)';
        }
    }

    if (enBtn) {
        enBtn.addEventListener('click', function() { switchLanguage('en'); });
    }
    if (frBtn) {
        frBtn.addEventListener('click', function() { switchLanguage('fr'); });
    }

    switchLanguage(currentLang);
});
