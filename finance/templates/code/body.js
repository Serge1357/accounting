// WITH DOM

"use strict"

const bodyContainer = document.getElementById('body__container');

const createH1 = document.createElement('h1');
createH1.textContent = 'Home Accounting';
bodyContainer.prepend(createH1);


const createP = document.createElement('p');
createP.classList.add('text__body');
createP.textContent = `Is a website that helps you keep track of your expenses and income.
It allows you to create transactions, track them, sort and analyze data.`;
createH1.after(createP);

const createDiv = document.createElement('div');
createDiv.classList.add('list__body');
createP.after(createDiv);
const createP2 = document.createElement('p');
createP2.classList.add('text__body');
createP2.textContent = `Here you can enter your transactions and view a list of all saved transactions.`;
createDiv.prepend(createP2);

const createBtn = document.createElement('button');
createBtn.classList.add('btn__body');
createBtn.textContent = 'List of transactions'
createP2.after(createBtn);

const createTable = document.createElement('table');
createTable.classList.add('table__body');
createTable.setAttribute('id', 'myTable');
createBtn.after(createTable);

const addButton = document.querySelector(".add__btn");
addButton.addEventListener("click", function (e) {
  e.preventDefault();

  const typeSelect = document.getElementById("type");
  const amountInput = document.getElementById("amount");
  const descriptionInput = document.getElementById("description");
  const categoryExpenses = document.getElementById("category__expenses");
  const categoryIncome = document.getElementById("category__income");
  const selectedCategory = typeSelect.value === "expenses" ? categoryExpenses.value: categoryIncome.value;
  const dateInput = document.getElementById("date");

  const newRow = createTable.insertRow();
  const typeCell = newRow.insertCell();
  typeCell.textContent = typeSelect.value;
  const amountCell = newRow.insertCell();
  amountCell.textContent = amountInput.value;
  const descriptionCell = newRow.insertCell();
  descriptionCell.textContent = descriptionInput.value;
  const categoryCell = newRow.insertCell();
  categoryCell.textContent = selectedCategory;
  const dateCell = newRow.insertCell();
  dateCell.textContent = dateInput.value;

  typeSelect.value = "expenses";
  amountInput.value = "";
  descriptionInput.value = "";
  categoryExpenses.value = "";
  categoryIncome.value = "";
  dateInput.value = "";
});