document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.toast');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        }, 3000);
    });

    const filterForm = document.querySelector('.filter-bar');
    if (filterForm) {
        const selects = filterForm.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', () => filterForm.closest('form').submit());
        });
    }

    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let timeout;
        searchInput.addEventListener('input', () => {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                searchInput.closest('form').submit();
            }, 500);
        });
    }

    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    function openSidebar() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('open');
            sidebarOverlay.classList.add('visible');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeSidebar() {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('open');
            sidebarOverlay.classList.remove('visible');
            document.body.style.overflow = '';
        }
    }

    function updateMenuBtn() {
        if (window.innerWidth <= 768) {
            if (mobileMenuBtn) mobileMenuBtn.style.display = 'flex';
        } else {
            if (mobileMenuBtn) mobileMenuBtn.style.display = 'none';
            if (sidebar) {
                sidebar.classList.remove('open');
                document.body.style.overflow = '';
            }
            if (sidebarOverlay) sidebarOverlay.classList.remove('visible');
        }
    }

    updateMenuBtn();
    window.addEventListener('resize', updateMenuBtn);

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', openSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }

    if (sidebar) {
        sidebar.querySelectorAll('.sidebar-nav .nav-item, .sidebar-footer .nav-item').forEach(item => {
            item.addEventListener('click', function() {
                closeSidebar();
            });
        });

        let touchStartX = 0;
        sidebar.addEventListener('touchstart', function(e) {
            touchStartX = e.touches[0].clientX;
        }, { passive: true });

        sidebar.addEventListener('touchend', function(e) {
            let touchEndX = e.changedTouches[0].clientX;
            if (touchEndX - touchStartX < -80 && window.innerWidth <= 768) {
                closeSidebar();
            }
        }, { passive: true });
    }

    lucide.createIcons();
});
