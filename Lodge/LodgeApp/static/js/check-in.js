document.addEventListener("DOMContentLoaded", () => {
  const selected = document.querySelector(".selected-guest");
  const optionsContainer = document.querySelector(".options-container");
  const searchBox = document.querySelector(".search-box input");
  const returningForm = document.querySelector(".returning-form");

  const optionsList = document.querySelectorAll(".option");

  selected.addEventListener("click", () => {
    optionsContainer.classList.toggle("active");
    returningForm.classList.remove("active");

    searchBox.value = "";
    filterList("");

    if (optionsContainer.classList.contains("active")) {
      searchBox.focus();
    }
  });

  optionsList.forEach(o => {
    o.addEventListener("click", (event) => {
      const inputElements = o.querySelectorAll("input");
      const returningForm = document.querySelector(".returning-form");

      // Assuming you have three input elements (you can adjust this based on your actual HTML)
      const [Value1, guestName, guestEmail, guestNumber] = Array.from(inputElements).map(input => input.value);

      selected.innerHTML = o.querySelector("label").innerHTML;
      optionsContainer.classList.remove("active");

      // Populate the form fields
      returningForm.querySelector("#yourName").value = guestName;
      returningForm.querySelector("#yourEmail").value = guestEmail;
      returningForm.querySelector("#yourPhone").value = guestNumber;

      returningForm.classList.add("active");
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
});


document.addEventListener('DOMContentLoaded', function () {
  var newGuestTab = document.getElementById('new-guest-justified');
  var checkInTab = document.getElementById('check-in-justified');

  // Function to get the initial state of a tab
  function getInitialState(tab) {
    var inputs = tab.querySelectorAll('input, select');
    var initialState = {};
    inputs.forEach(function (input) {
      if (input.type === 'radio' || input.type === 'checkbox') {
        initialState[input.id] = input.checked;
      } else {
        initialState[input.id] = input.value;
      }
    });
    return initialState;
  }

  // Function to reset the tab content to its initial state
  function resetTabContent(tab, initialState) {
    var inputs = tab.querySelectorAll('input, select');
    inputs.forEach(function (input) {
      if (input.type === 'radio' || input.type === 'checkbox') {
        input.checked = initialState[input.id];
      } else {
        input.value = initialState[input.id];
      }
    });
  }

  // Store the initial state of the tabs
  var newGuestInitialState = getInitialState(newGuestTab);
  var checkInInitialState = getInitialState(checkInTab);

  // Listen for the hidden event on the tabs
  var newGuestButton = document.getElementById('new-guest-tab');
  var checkInButton = document.getElementById('check-in-tab');

  newGuestButton.addEventListener('hidden.bs.tab', function () {
    const returningForm = document.querySelector(".returning-form");
    returningForm.classList.remove("active");
    resetTabContent(newGuestTab, newGuestInitialState);
  });

  checkInButton.addEventListener('hidden.bs.tab', function () {
    resetTabContent(checkInTab, checkInInitialState);
  });
});

