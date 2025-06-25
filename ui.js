// ui.js
export function createAuthUI(signUpHandler, logInHandler) {
  const container = document.createElement('div');
  container.className = 'container';

  const title = document.createElement('h2');
  title.textContent = 'Welcome';

  const emailInput = document.createElement('input');
  emailInput.type = 'email';
  emailInput.id = 'email';
  emailInput.placeholder = 'Email';

  const passwordInput = document.createElement('input');
  passwordInput.type = 'password';
  passwordInput.id = 'password';
  passwordInput.placeholder = 'Password';

  const buttonGroup = document.createElement('div');
  buttonGroup.className = 'btn-group';

  const signUpButton = document.createElement('button');
  signUpButton.textContent = 'Sign Up';
  signUpButton.addEventListener('click', () => {
    signUpHandler(emailInput.value, passwordInput.value);
  });

  const logInButton = document.createElement('button');
  logInButton.textContent = 'Log In';
  logInButton.addEventListener('click', () => {
    logInHandler(emailInput.value, passwordInput.value);
  });

  buttonGroup.appendChild(signUpButton);
  buttonGroup.appendChild(logInButton);

  container.appendChild(title);
  container.appendChild(emailInput);
  container.appendChild(passwordInput);
  container.appendChild(buttonGroup);

  return container;
}
