// Function to fetch and display the 5 most recent guests
function fetchAndDisplayguests() {
  // Fetch the 5 most recent guests from the API
  fetch('/api/guests?limit=20')
    .then(response => response.json())
    .then(guests => {
      // Get the HTML element where the guests will be displayed
      const tableBody = document.querySelector('.datatable tbody');

      // Clear previous contents
      tableBody.innerHTML = '';

      // Create a table row for each guest and append to the table body
      guests.forEach((guest, index) => {
        const row = tableBody.insertRow();

        // Insert cells (`td`) and fill them with data
        const cellNumber = row.insertCell(0);
        cellNumber.innerHTML = `<a href="#">#${guest.id}</a>`; // Assuming 'id' is a property of the guest

        const cellName = row.insertCell(1);
        cellName.textContent = guest.name; // Assuming 'guest' is a property of the guest

        const cellMail = row.insertCell(2);
        cellMail.innerHTML = `<a href="mailto:${guest.email}" class="text-primary">${guest.email}</a>`; // Assuming 'email' is a property of the guest

        const cellRoom = row.insertCell(3);
        cellRoom.textContent = `$${guest.room}`; // Assuming 'room' is a property of the guest

        const cellMobile = row.insertCell(4);
        cellMobile.textContent = `$${guest.mobile}`; // Assuming 'mobile' is a property of the guest
      });
    })
    .catch(error => {
      console.error('Error fetching guests:', error);
    });
}


// Call the function when the window loads
window.onload = fetchAndDisplayguests;
