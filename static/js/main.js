document.addEventListener('DOMContentLoaded', function () {
    var now = new Date();
    var dateStr = now.getFullYear() + '年' +
        String(now.getMonth() + 1).padStart(2, '0') + '月' +
        String(now.getDate()).padStart(2, '0') + '日 ' +
        ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'][now.getDay()];
    var el = document.getElementById('headerDate');
    if (el) el.textContent = dateStr;

    initCarousel();
    initDots();
});

/* Carousel */
var slideIndex = 0;
var autoSlideTimer = null;
function initCarousel() {
    var inner = document.getElementById('carouselInner');
    if (!inner) return;
    var items = inner.querySelectorAll('.carousel-item');
    if (items.length === 0) return;

    showSlide(0);
    startAutoSlide();
    var carousel = document.getElementById('carousel');
    carousel.addEventListener('mouseenter', stopAutoSlide);
    carousel.addEventListener('mouseleave', startAutoSlide);
}

function showSlide(n) {
    var inner = document.getElementById('carouselInner');
    var items = inner.querySelectorAll('.carousel-item');
    var dots = document.querySelectorAll('#carouselDots span');
    if (items.length === 0) return;
    slideIndex = (n + items.length) % items.length;
    inner.style.transform = 'translateX(-' + (slideIndex * 100) + '%)';
    items.forEach(function (item) { item.classList.remove('active'); });
    items[slideIndex].classList.add('active');
    dots.forEach(function (d, i) { d.classList.toggle('active', i === slideIndex); });
}

function moveSlide(n) { stopAutoSlide(); showSlide(slideIndex + n); startAutoSlide(); }

function startAutoSlide() {
    stopAutoSlide();
    autoSlideTimer = setInterval(function () { showSlide(slideIndex + 1); }, 5000);
}
function stopAutoSlide() { if (autoSlideTimer) { clearInterval(autoSlideTimer); autoSlideTimer = null; } }

function initDots() {
    var inner = document.getElementById('carouselInner');
    if (!inner) return;
    var count = inner.querySelectorAll('.carousel-item').length;
    var dotsContainer = document.getElementById('carouselDots');
    if (!dotsContainer) return;
    for (var i = 0; i < count; i++) {
        var dot = document.createElement('span');
        dot.onclick = function () { showSlide(slideIndex = parseInt(this.dataset.index)); };
        dot.dataset.index = i;
        if (i === 0) dot.classList.add('active');
        dotsContainer.appendChild(dot);
    }
}

/* News Tabs */
function switchNewsTab(el, tab) {
    var tabs = el.parentElement.querySelectorAll('.news-tab');
    tabs.forEach(function (t) { t.classList.remove('active'); });
    el.classList.add('active');
    var container = el.closest('.section');
    var contents = container.querySelectorAll('.news-content');
    contents.forEach(function (c) { c.classList.remove('active'); });
    var target = container.querySelector('#news-' + tab);
    if (target) target.classList.add('active');
}
