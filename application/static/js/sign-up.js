// Get form elements
const form = document.querySelector('form');
const accountNameInput = document.getElementById('Account-Name');
const emailInput = document.getElementById('Email-Address');
const phoneInput = document.getElementById('Phone-Number');
const passwordInput = document.getElementById('Password');
const rePasswordInput = document.getElementById('Re-Password');
const submitButton = document.getElementById('Submit');

// Add event listener to form submit
form.addEventListener('submit', (event) => {
  // Prevent default form submission behavior
  event.preventDefault();

  // Retrieve input values
  const accountName = accountNameInput.value;
  const email = emailInput.value;
  const phone = phoneInput.value;
  const password = passwordInput.value;
  const rePassword = rePasswordInput.value;

  // Validate form data
  if (!accountName || !email || !phone || !password || !rePassword) {
    alert('All fields are required.');
    return;
  }

  if (password !== rePassword) {
    alert('Passwords do not match.');
    return;
  }

  if (password.length < 8 || !/[A-Z]/.test(password) || !/\W/.test(password)) {
    alert('Password must be at least 8 characters long, and contain at least one uppercase letter and one symbol.');
    return;
  }

  if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
    alert('Invalid email address.');
    return;
  }


  // Create form data object
  const formData = new FormData();
  formData.append('Account-Name', accountName);
  formData.append('Email-Address', email);
  formData.append('Phone-Number', phone);
  formData.append('Password', password);
  formData.append('Re-Password', rePassword);

  // Send HTTP POST request to Flask server with form data
  fetch('/signUp', {
    method: 'POST',
    body: formData
  })
  .then(response => response.text())
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error(error);
  });
});
