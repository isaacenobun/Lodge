const selected = document.querySelector(".selected-category");
const optionsContainer = document.querySelector(".expense-options-container");
const searchBox = document.querySelector(".expense-search-box input");
const optionsList = document.querySelectorAll(".expense-option");
const tableBody = document.querySelector(".expense-table");

selected.addEventListener("click", () => {
  optionsContainer.classList.toggle("active");

  searchBox.value = "";
  filterList("");

  if (optionsContainer.classList.contains("active")) {
    searchBox.focus();
  }
});

optionsList.forEach(o => {
  o.addEventListener("click", () => {
    selected.innerHTML = o.querySelector("label").innerHTML;
    optionsContainer.classList.remove("active");

    // Render the form
    renderForm();
  });
});

searchBox.addEventListener("keyup", function (e) {
  filterList(e.target.value);
});

const filterList = searchTerm => {
  searchTerm = searchTerm.toLowerCase();
  optionsList.forEach(option => {
    let label = option.firstElementChild.nextElementSibling.innerText.toLowerCase();
    if (label.indexOf(searchTerm) != -1) {
      option.style.display = "block";
    } else {
      option.style.display = "none";
    }
  });
};

const renderForm = () => {
  const formHTML = `
    <form id="expense-form">
      <div class="form-floating mb-3">
        <input type="text" class="form-control" id="expenseTitle" placeholder="Expense Title">
        <label for="expenseTitle">Expense Title</label>
      </div>
      <div class="input-group mb-3">
        <span class="input-group-text">&#8358</span>
        <input type="text" class="form-control" id="expenseAmount" placeholder="Amount">
        <span class="input-group-text">.00</span>
      </div>
      <div class="input-group">
        <span class="input-group-text">Description</span>
        <textarea class="form-control" id="expenseDescription" placeholder="Description"></textarea>
      </div>
      <div class="">
        <div class="form-check form-switch">
          <input class="form-check-input" type="checkbox" id="flexSwitchCheckDefault">
          <label class="form-check-label" for="flexSwitchCheckDefault">Set as recurring expense</label>
        </div>
      </div>
      
      <button type="button" class="btn btn-dark form-control mt-3 add-expenses-btn">Add Expense</button>
    </form>
  `;

  // Append the form to the container or any specific element
  document.querySelector(".form-container").innerHTML = formHTML;

  document.querySelector(".add-expenses-btn").addEventListener("click", addExpense);
};




