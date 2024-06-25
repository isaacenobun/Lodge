document.addEventListener('DOMContentLoaded', (event) => {
  // Get the current URL path
  var path = window.location.pathname;

  // Get all the nav links
  var navLinks = document.querySelectorAll('.sidebar-nav .nav-link');

  // Loop through nav links
  navLinks.forEach(link => {
    // Check if the link's href matches the current path
    if (link.getAttribute('href') === path) {
      // Remove the 'collapsed' class
      link.classList.remove('collapsed');
    }
  });
});
