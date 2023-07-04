// WITHOUT DOM

"use strict"

const transactionBtn  = document.getElementById('transaction');
const transactionBlock = document.getElementById('transaction__block');
const arrow  = document.querySelector('.arrow');
transactionBtn.addEventListener('click', () => {
  if (transactionBlock.style.display === 'block') {
    transactionBlock.style.display = 'none';
  } else {
    transactionBlock.style.display = 'block';
  }
  arrow.classList.toggle('active');
});

document.addEventListener("click", (e) => {
  if (!transactionBtn.contains(e.target) && !transactionBlock.contains(e.target)) {
    transactionBlock.style.display = "none";
  }
});

const typeSelect = document.getElementById('type');
const categoryExpenses = document.getElementById('category__expenses');
const categoryIncome = document.getElementById('category__income');

typeSelect.addEventListener('change', function() {
  if (this.value === 'expenses') {
    categoryExpenses.style.display = 'block';
    categoryIncome.style.display = 'none';
  } else if (this.value === 'income') {
    categoryExpenses.style.display = 'none';
    categoryIncome.style.display = 'block';
  } else {
    categoryExpenses.style.display = 'none';
    categoryIncome.style.display = 'none';
  }
});

const html = document.querySelector('html');
const loginModal = document.getElementById("login__modal");
const registerModal = document.getElementById("register__modal");

const openModal = (modal) => {
  modal.style.display = 'block';
  html.classList.add('modal__open');
}

const closeModal = (modal) => {
  modal.style.display = 'none';
  html.classList.remove('modal__open');
}

const openModalHandler = (modal, button) => {
  button.addEventListener('click', () => {
    openModal(modal);
  });
}

const loginButton = document.getElementById('open__login');
const registerButton = document.getElementById('open__register');
openModalHandler(loginModal, loginButton);
openModalHandler(registerModal, registerButton);

window.addEventListener('DOMContentLoaded', () => {
  closeModal(loginModal);
  closeModal(registerModal);
});

const closeButtons = document.getElementsByClassName("close");
for (let i = 0; i < closeButtons.length; i++) {
  closeButtons[i].addEventListener("click", () => {
    registerModal.style.display = "none";
    loginModal.style.display = "none";
  });
}

document.addEventListener("click", (e) => {
  if (e.target === loginModal || e.target === registerModal) {
    loginModal.style.display = "none";
    registerModal.style.display = "none";
  }
});

const submitBtn = document.querySelectorAll(".submit__btn");

const nameRegex = /^[a-zA-Z\s]+$/;
//const phoneRegex = /^\+?\d+$/;
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const passRegex = /^(?=.*\d)[a-zA-Z\d]{8,}$/;

function validateInput(input, regex) {
  return regex.test(input.value);
}

submitBtn.forEach((button) => {
  button.addEventListener('click', (e) => {
    e.preventDefault();
    let isValid = true;

    const form = button.closest('form');
    const nameInput = form.querySelector('input[name="username"]');
    const surnameInput = form.querySelector('input[name="surname"]');
    const emailInput = form.querySelector('input[name="mail"]');
    const confirmEmailInput = form.querySelector('input[name="confirm-mail"]');
    const passInput = form.querySelector('input[name="pass"]');
    const confirmPassInput = form.querySelector('input[name="confirm-pass"]');
    const phoneInput = form.querySelector('input[name="phone"]');

    if (!validateInput(nameInput, nameRegex)) {
      nameInput.nextElementSibling.textContent = 'Please enter the correct name';
      isValid = false;
    } else {
      nameInput.nextElementSibling.textContent = '';
    }

    if (!validateInput(surnameInput, nameRegex)) {
      surnameInput.nextElementSibling.textContent = 'Please enter the correct surname';
      isValid = false;
    } else {
      surnameInput.nextElementSibling.textContent = '';
    }

    if (!validateInput(emailInput, emailRegex)) {
      emailInput.nextElementSibling.textContent = 'Please enter a valid email address';
      isValid = false;
    } else {
      emailInput.nextElementSibling.textContent = '';
    }

    if (emailInput.value !== confirmEmailInput.value) {
      confirmEmailInput.nextElementSibling.textContent = 'Email addresses do not match';
      isValid = false;
    } else {
      confirmEmailInput.nextElementSibling.textContent = '';
    }

    if (!validateInput(passInput, passRegex)) {
      passInput.nextElementSibling.textContent = 'Please enter a valid password';
      isValid = false;
    } else {
      passInput.nextElementSibling.textContent = '';
    }

    if (passInput.value !== confirmPassInput.value) {
      confirmPassInput.nextElementSibling.textContent = 'Passwords do not match';
      isValid = false;
    } else {
      confirmPassInput.nextElementSibling.textContent = '';
    }

//    if (!validateInput(phoneInput, phoneRegex)) {
//      phoneInput.nextElementSibling.textContent = 'Please enter a valid phone number';
//      isValid = false;
//    } else {
//      phoneInput.nextElementSibling.textContent = '';
//    }

    if (isValid) {
      document.location.href = './thank-you/index.html';
    }
  });
});

submitBtn.forEach((button) => {
  button.addEventListener('click', (e) => {
    e.preventDefault();

    const form = button.closest('form');
    const emailInput = form.querySelector('input[name="mail"]');
    const passInput = form.querySelector('input[name="pass"]');

    let isValid = true;

    if (!validateInput(emailInput, emailRegex) || emailInput.value.trim() === '') {
      emailInput.nextElementSibling.textContent = 'Please enter an email';
      isValid = false;
    } else {
      emailInput.nextElementSibling.textContent = '';
    }

    if (!validateInput(passInput, passRegex) || passInput.value.trim() === '') {
      passInput.nextElementSibling.textContent = 'Please enter a password';
      isValid = false;
    } else {
      passInput.nextElementSibling.textContent = '';
    }

    if (isValid) {
      document.location.href = './thank-you/index.html';
    }
  });
});