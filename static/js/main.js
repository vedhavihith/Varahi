// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');
if (navToggle) {
  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
}

// Auto-dismiss flash messages
setTimeout(() => {
  document.querySelectorAll('.flash').forEach(el => el.remove());
}, 5000);

// Search form: submit on Enter
const searchInput = document.querySelector('.filter-inner input[name="search"]');
if (searchInput) {
  searchInput.addEventListener('keydown', e => {
    if (e.key === 'Enter') e.target.closest('form').submit();
  });
}
