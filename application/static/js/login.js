// Get form elements
const form = document.querySelector('form');
const emailInput = document.getElementById('Email-Address');
const passwordInput = document.getElementById('Password');
const submitButton = document.getElementById('Submit');

// Add event listener to form submit
form.addEventListener('submit', (event) => {
  // Prevent default form submission behavior
  event.preventDefault();

  // Retrieve input values

  const email = emailInput.value;
  const password = passwordInput.value;
  // Validate form data
  if (!email || !password) {
    alert('All fields are required.');
    return;
  }
  if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
    alert('Invalid email address.');
    return;
  }


  // Create form data object
  const formData = new FormData();
  formData.append('Email-Address', email);
  formData.append('Password', password);


  // Send HTTP POST request to Flask server with form data
  fetch('/logIn', {
    method: 'POST',
    body: formData
  })
  .then(message => message.text())
  .then(data => {
    console.log(data);
    // Get the HTML element where you want to display the message
    const messageElement = document.getElementById('message');
    // Set the innerHTML of the element to the returned message
    messageElement.innerHTML = data;
  })
  .catch(error => {
    console.error(error);
  });})
