const themeToggle = document.getElementById('theme-toggle');
const toggleSlider = document.querySelector('.toggle-slider');
const isDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;

// Initialize the switch to the user's preference
if (isDarkMode) {
  document.documentElement.classList.add('dark');
  themeToggle.checked = true;
} else {
  document.documentElement.classList.remove('dark');
  themeToggle.checked = false;
}

// Handle switch toggle
themeToggle.addEventListener('change', () => {
  if (themeToggle.checked) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
  // Store user's preference in MongoDB
  fetch('/api/theme', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ isDarkMode: themeToggle.checked })
  });
});

// Retrieve user's preference from MongoDB on page load
fetch('/api/theme')
  .then(response => response.json())
  .then(data => {
    if (data.isDarkMode) {
      document.documentElement.classList.add('dark');
      themeToggle.checked = true;
      toggleSlider.style.backgroundColor = '#38a169';
      toggleSlider.style.borderColor = '#38a169';
    } else {
      document.documentElement.classList.remove('dark');
      themeToggle.checked = false;
      toggleSlider.style.backgroundColor = '#718096';
      toggleSlider.style.borderColor = '#718096';
    }
  });
