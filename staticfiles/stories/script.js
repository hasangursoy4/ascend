// Geri butonu — fade-out class'ını temizle
window.addEventListener('pageshow', (e) => {
    document.body.classList.remove('fade-out');
});

document.addEventListener('DOMContentLoaded', () => {
    const checkbox = document.getElementById('theme-checkbox');
    const body = document.body;

    // Varsayılan = LIGHT mode
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
        if (checkbox) checkbox.checked = true;
    } else {
        body.classList.remove('dark-mode');
        if (checkbox) checkbox.checked = false;
    }

    if (checkbox) {
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark');
            } else {
                body.classList.remove('dark-mode');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // SAYFA GEÇİŞ ANİMASYONU
    document.querySelectorAll('a[href]').forEach(link => {
        const href = link.getAttribute('href');
        // Sadece iç linklere uygula, # anchor ve javascript: linklerine değil
        if (!href || href.startsWith('#') || href.startsWith('javascript') || href.startsWith('mailto')) return;
        // Yeni sekmede açılanları atla
        if (link.target === '_blank') return;

        link.addEventListener('click', (e) => {
            const isLevelBtn = link.classList.contains('level-btn-detail') || link.classList.contains('popup-option');
            const isCatBtn = link.classList.contains('cat-btn');
            if (isLevelBtn || isCatBtn) {
                sessionStorage.setItem('scrollPos', window.scrollY);
            }

            e.preventDefault();
            body.classList.add('fade-out');
            setTimeout(() => {
                window.location.href = href;
            }, 80);
        });
    });

    // Sayfa yüklenince scroll pozisyonunu geri yükle
    const savedScroll = sessionStorage.getItem('scrollPos');
    if (savedScroll) {
        window.scrollTo(0, parseInt(savedScroll));
        sessionStorage.removeItem('scrollPos');
    }

    // LEVEL PICKER POPUP
    const levelBadge = document.getElementById('level-badge');
    const levelPopup = document.getElementById('level-popup');

    if (levelBadge && levelPopup) {
        levelBadge.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault(); // fade-out tetiklenmesin
            levelPopup.classList.toggle('visible');
        });

        document.addEventListener('click', () => {
            levelPopup.classList.remove('visible');
        });

        levelPopup.addEventListener('click', (e) => e.stopPropagation());
    }

    // VOCAB HIGHLIGHT — tooltip + scroll
    document.querySelectorAll('.vocab-highlight').forEach(span => {
        const meaning = span.getAttribute('data-meaning');
        const tooltip = document.createElement('span');
        tooltip.classList.add('tooltip');
        tooltip.textContent = meaning;
        span.appendChild(tooltip);

        span.addEventListener('click', () => {
            const slug = span.getAttribute('data-slug');
            const card = findVocabCard(slug);
            if (card) {
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                card.classList.add('flash');
                setTimeout(() => card.classList.remove('flash'), 1500);
            }
        });
    });

    function findVocabCard(slug) {
        const cards = document.querySelectorAll('.vocab-card');
        for (const card of cards) {
            const word = card.getAttribute('data-word') || '';
            const cardSlug = word.replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
            if (cardSlug === slug) return card;
        }
        return null;
    }

    // VOCAB KART — tıklayınca metindeki kelimeye scroll
    document.querySelectorAll('.vocab-card').forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', () => {
            const word = card.getAttribute('data-word');
            if (!word) return;
            const slug = word.replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
            const span = document.querySelector(`.vocab-highlight[data-slug="${slug}"]`);
            if (span) {
                span.scrollIntoView({ behavior: 'smooth', block: 'center' });
                span.style.transition = 'background 0.3s';
                span.style.background = 'rgba(47,62,87,0.15)';
                span.style.borderRadius = '3px';
                setTimeout(() => {
                    span.style.background = '';
                    span.style.borderRadius = '';
                }, 1500);
            }
        });
    });
});