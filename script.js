/* ======================================================
   THE SELF-BOOKING SYSTEM — Soft Luxury Interactions
   ====================================================== */

document.addEventListener('DOMContentLoaded', () => {

  /* ---- FADE-UP ON SCROLL ---- */
  const animEls = document.querySelectorAll('.anim');
  const animObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        animObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -20px 0px' });

  animEls.forEach((el) => animObserver.observe(el));

  /* ---- STICKY NAV ---- */
  const stickyNav = document.getElementById('stickyNav');
  const hero = document.querySelector('.hero');

  if (stickyNav && hero) {
    const navObserver = new IntersectionObserver(([entry]) => {
      stickyNav.classList.toggle('visible', !entry.isIntersecting);
    }, { threshold: 0 });
    navObserver.observe(hero);
  }

  /* ---- ANIMATED COUNTERS ---- */
  const statNums = document.querySelectorAll('.stat-number[data-target]');
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  statNums.forEach((el) => counterObserver.observe(el));

  function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    const isDollar = el.classList.contains('stat-number--dollar');
    const duration = 2000;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.round(eased * target);
      el.textContent = isDollar ? '$' + current : current;
      if (progress < 1) requestAnimationFrame(tick);
    }

    requestAnimationFrame(tick);
  }

  /* ---- SMOOTH SCROLL ---- */
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      const target = document.querySelector(link.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
