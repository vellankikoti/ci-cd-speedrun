// Auto-collapse parent nav section when a child link is clicked
// For MkDocs Material theme

window.addEventListener('DOMContentLoaded', function () {
  // Find all sidebar nav links that are not parents
  document.querySelectorAll('.md-nav__item .md-nav__link').forEach(function(link) {
    link.addEventListener('click', function(e) {
      // Only act if this is a child (not a parent with children)
      var parentItem = link.closest('.md-nav__item');
      if (parentItem && !parentItem.classList.contains('md-nav__item--nested')) {
        // Find the open parent section
        var openSection = link.closest('.md-nav__list .md-nav__item--active');
        if (openSection && openSection.classList.contains('md-nav__item--active')) {
          // Collapse it after a short delay (so navigation works)
          setTimeout(function() {
            openSection.classList.remove('md-nav__item--active');
          }, 200);
        }
      }
    });
  });
}); 