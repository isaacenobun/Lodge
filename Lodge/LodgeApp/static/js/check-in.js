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


      // Assuming you have three input elements (you can adjust this based on your actual HTML)
      const [value1, guestName, guestEmail, guestNumber] = Array.from(inputElements).map(input => input.value);

      selected.innerHTML = o.querySelector("label").innerHTML;
      optionsContainer.classList.remove("active");

      // Populate the form fields
      document.getElementById("registeredName").value = guestName;
      document.getElementById("registeredEmail").value = guestEmail;
      document.getElementById("inputNumber").value = guestNumber;

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
