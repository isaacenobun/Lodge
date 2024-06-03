document.addEventListener('DOMContentLoaded', (event) => {
  // Function to toggle row highlight
  function toggleHighlight(row, isHighlighted) {
    if (isHighlighted) {
      row.classList.add('table-active');
    } else {
      row.classList.remove('table-active');
    }
  }

  // Function to get selected row details
  function getSelectedRowDetails() {
    const selectedRowsDetails = [];
    const checkboxes = document.querySelectorAll('.form-check-input:checked'); // Get only checked checkboxes

    checkboxes.forEach(checkbox => {
      const row = checkbox.closest('tr');
      const rowData = {
        guestName: row.cells[2].textContent,
        roomNumber: row.cells[4].textContent
      };
      selectedRowsDetails.push(rowData);
    });

    return selectedRowsDetails;
  }

  // Get all checkboxes
  const checkboxes = document.querySelectorAll('.form-check-input');

  // Add event listeners to checkboxes
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function () {
      const row = this.closest('tr'); // Get the parent row
      toggleHighlight(row, this.checked); // Call the function to toggle highlight
    });
  });

  // Event listener for checkout button
  document.querySelector('#table-checkout').addEventListener('click', () => {
    const details = getSelectedRowDetails();
    const detailsDiv = document.getElementById('guestlist-modal');
    detailsDiv.innerHTML = '<strong>The following guest/guests will be checked out:</strong><br>'; // Clear previous content and add header

    details.forEach(detail => {
      const detailString = `Guest: ${detail.guestName}, Room: ${detail.roomNumber}<br>`;
      detailsDiv.innerHTML += detailString;
    });
  });
});




document.addEventListener('DOMContentLoaded', (event) => {
  // Get the button element
  const button = document.getElementById('table-checkout'); // Replace with your actual button ID

  // Get all checkboxes
  const checkboxes = document.querySelectorAll('.form-check-input');

  // Function to check if any checkbox is checked
  function updateButtonState() {
    const isAnyCheckboxChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
    if (isAnyCheckboxChecked) {
      button.classList.remove('disabled'); // Remove the disabled class from the button
    } else {
      button.classList.add('disabled'); // Add the disabled class back if no checkboxes are checked
    }
  }

  // Add event listeners to checkboxes
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', updateButtonState);
  });

  // Initial check in case the page is loaded with some checkboxes already checked
  updateButtonState();
});