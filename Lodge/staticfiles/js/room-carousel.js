// // Room selector display
// const container = document.querySelector('.container-room-select');
// const seats = document.querySelectorAll('.row .seat:not(.occupied)');
// const count = document.getElementById('count');
// const total = document.getElementById('total');
// const movieSelect = document.getElementById('floor');


// let ticketPrice = +movieSelect.value;

// New combined function
function updateUI(selectedSuite) {
  // Update selected seats count and total price
  // const selectedSeats = document.querySelectorAll('.row .seat.selected');
  // const selectedSeatsCount = selectedSeats.length;
  // count.innerText = selectedSeatsCount;
  // total.innerText = selectedSeatsCount * ticketPrice;

  // suite display option

  // Hide all suite-info divs
  document.querySelectorAll('.suite-info').forEach(div => {
    div.classList.remove('activated');
  });

  // Show the selected suite's info div
  const suiteId = selectedSuite.value;
  const suiteDiv = document.getElementById(suiteId + '-suite');
  if (suiteDiv) {
    suiteDiv.classList.add('activated');
  }
}

// // Movie Select Event
// movieSelect.addEventListener('change', e => {
//   ticketPrice = +e.target.value;
//   updateUI();
// });

// // Seat click event
// container.addEventListener('click', e => {
//   if (e.target.classList.contains('seat') && !e.target.classList.contains('occupied')) {
//     e.target.classList.toggle('selected');
//   }
//   updateUI();
// });


// function showProfile(name) {
//   // Replace this with your logic to load the profile page dynamically
//   // For demonstration purposes, we'll just navigate to a different URL
//   // based on the person's name.
//   const profileUrl = `${name}.html`;
//   window.location.href = profileUrl;
// }



// Function to show the modal with the appropriate message
function showModalWithOccupancyStatus(roomNumber, isOccupied, guestId, guestName, roomQueryset) {
  // Get the modal elements
  const modal = document.getElementById('verticalycentered');
  const modalBody = modal.querySelector('.modal-body');
  const modalFooter = modal.querySelector('.modal-footer');

  // Set the content for the modal body based on occupancy
  const modalBodyContent = isOccupied
    ? `This room is currently occupied by: ${guestName}`
    : `${roomNumber} is available.`;

  // Update the modal body with the new content
  modalBody.textContent = modalBodyContent;

  // Update the modal footer with the appropriate buttons based on occupancy
  const modalFooterContent = isOccupied
    ? `<form action="${checkOutUrl}" method="POST">
        
         <input type="hidden" name="guest_ids" value="${guestId}">
         <button type="submit" class="btn btn-outline-danger" data-bs-dismiss="modal">Checkout</button>
       </form>`
    : `<button type="button" class="btn btn-success" data-bs-toggle="modal"
            data-bs-target="#basicModal">
         <i class="bi bi-check-circle me-1"></i> Check-in a Guest
       </button>`;
  modalFooter.innerHTML = modalFooterContent;

  // Show the modal using Bootstrap's modal method
  new bootstrap.Modal(modal).show();
}

// Add event listeners to all seats
document.querySelectorAll('.room').forEach(room => {
  room.addEventListener('click', function () {
    // Get the room number from the clicked room
    const roomNumber = this.querySelector('.room-number').textContent;
    
    // Check if the room is occupied
    const isOccupied = this.classList.contains('occupied');
    
    // Get the guest ID from the hidden input within the clicked room
    const guestIdInput = this.querySelector('input[name="guest_id"]');
    const guestNameInput = this.querySelector('input[name="guest_name"]');
    const roomQuerysetInput = this.querySelector('input[name="room_queryset"]');
    const guestId = guestIdInput ? guestIdInput.value : null;
    const guestName = guestNameInput ? guestNameInput.value : null;
    const roomQueryset = roomQuerysetInput ? roomQuerysetInput.value : null;
    
    // Show the modal with the occupancy status and guest ID
    showModalWithOccupancyStatus(roomNumber, isOccupied, guestId, guestName, roomQueryset);
  });
});



