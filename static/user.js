// static/user.js

document.addEventListener('DOMContentLoaded', () => {
  const signupForm = document.getElementById('signupForm');
  if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const formData = new FormData(signupForm);
      const payload = new URLSearchParams(formData);

      const response = await fetch('/signup', {
        method: 'POST',
        body: payload
      });

      if (response.redirected) {
        window.location.href = response.url;
      } else {
        const text = await response.text();
        alert(text);
      }
    });
  }

  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const formData = new FormData(loginForm);
      const payload = new URLSearchParams(formData);

      const response = await fetch('/login', {
        method: 'POST',
        body: payload
      });

      if (response.redirected) {
        window.location.href = response.url;
      } else {
        const text = await response.text();
        alert(text);
      }
    });
  }

  const feedbackForm = document.getElementById('feedbackForm');
  if (feedbackForm) {
    feedbackForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const formData = new FormData(feedbackForm);
      const payload = new URLSearchParams(formData);

      const response = await fetch('/feedback', {
        method: 'POST',
        body: payload
      });

      if (response.ok) {
        alert("Thank you! Your feedback has been submitted.");
        feedbackForm.reset();
      } else {
        alert("Something went wrong!");
      }
    });
  }
});
