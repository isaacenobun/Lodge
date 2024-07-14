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
    o.addEventListener("click", async (event) => {
      const clickedElement = event.target;
      const clickedId = clickedElement.id;

      // Fetch guest details based on the clickedId (you'll need to implement this)
      const guestData = await fetchGuestData(clickedId);

      // Populate the form fields
      document.getElementById("yourName").value = guestData.name;
      document.getElementById("yourEmail").value = guestData.email;
      document.getElementById("inputNumber").value = guestData.number;

      // Show the form
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
