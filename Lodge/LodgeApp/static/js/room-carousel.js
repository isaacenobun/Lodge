
// New combined function
function updateUI(selectedSuite) {
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


// Function to show the modal with the appropriate message
function showModalWithOccupancyStatus(roomNumber, isOccupied, guestId, guestName, guestCheckout, roomQueryset) {
  // Get the modal elements
  const modal = document.getElementById('verticalycentered');
  const modalBody = modal.querySelector('.modal-body');
  const modalFooter = modal.querySelector('.modal-footer');

  // Set the content for the modal body based on occupancy
  const modalBodyContent = isOccupied
    ? `<div class= "breadcrumb">
        <div>This room is currently occupied by: <span id="guestName" style = "color: #00796b; font-weight: bold">${guestName}</span></div>
        <div>Current Checkout Date: <span id="currentCheckoutDate" style = "color: #00796b; font-weight: bold">${guestCheckout}</span></div>
       </div>`
    : `${roomNumber} is available.`;

  // Update the modal body with the new content
  modalBody.innerHTML = modalBodyContent;

  // Update the modal footer with the appropriate buttons based on occupancy
  const modalFooterContent = isOccupied
    ? `<form action="${checkOutUrl}" method="POST">
         <input type="hidden" name="guest_ids" value="${guestId}">
         <button type="submit" class="btn btn-outline-danger" data-bs-dismiss="modal">Checkout</button>
       </form>
       <button class="btn btn-dark" id="extendStayBtn" onclick="handleExtendStay(${guestId},${extendUrl})">Extend Stay</button>`
    : `<button type="button" class="btn btn-success" data-bs-toggle="modal"
            data-bs-target="#basicModal">
         <i class="bi bi-check-circle me-1"></i> Check-in a Guest
       </button>`;
  modalFooter.innerHTML = modalFooterContent;

  // Store the initial content in global variables
  window.initialModalBodyContent = modalBodyContent;
  window.initialModalFooterContent = modalFooterContent;

  // Show the modal using Bootstrap's modal method
  new bootstrap.Modal(modal).show();

}

// Function to handle the Extend Stay button click
function handleExtendStay(guestId,extendUrl) {
  const modal = document.getElementById('verticalycentered');
  const modalBody = modal.querySelector('.modal-body');
  const modalFooter = modal.querySelector('.modal-footer');

  // Replace modal body content with an input field
  modalBody.innerHTML += `<input type="number" min="1" id="extendStayInput" class="form-control" placeholder="Enter new stay duration" required>`;

  // Replace modal footer buttons with Cancel and Confirm buttons
  modalFooter.innerHTML = `
    <button class="btn btn-secondary" id="cancelBtn" onclick="cancelExtendStay()">Cancel</button>
    <button class="btn btn-primary" id="confirmBtn" onclick="confirmExtendStay(${guestId},${extendUrl})" disabled>Confirm</button>
  `;
  // Enable the confirm button only if there is a value in the input box
  document.getElementById('extendStayInput').addEventListener('input', function () {
    document.getElementById('confirmBtn').disabled = !this.value.trim();
  });
}



// Function to handle the Cancel button click
function cancelExtendStay() {
  const modal = document.getElementById('verticalycentered');
  const modalBody = modal.querySelector('.modal-body');
  const modalFooter = modal.querySelector('.modal-footer');

  // Restore the initial modal content
  modalBody.innerHTML = window.initialModalBodyContent;
  modalFooter.innerHTML = window.initialModalFooterContent;
}

// Function to handle the Confirm button click
function confirmExtendStay(guestId,extendUrl) {
  const newStayDuration = document.getElementById('extendStayInput').value;
  const modal = document.getElementById('verticalycentered');
  const modalBody = modal.querySelector('.modal-body');
  const modalFooter = modal.querySelector('.modal-footer');

  // Update the modal body with the new checkout date
  const updatedContent = `${window.initialModalBodyContent} <div class= "breadcrumb">New checkout date:  <span id= "newCheckoutDate" style = "color: #00796b; font-weight: bold"> ${newStayDuration} days from now</span></div>`;
  modalBody.innerHTML = updatedContent;


  // Update the global variable with the new checkout date
  // window.initialModalBodyContent = updatedContent;

  // Restore the initial modal footer content
  modalFooter.innerHTML = `<button class="btn btn-secondary" id="cancelBtn"   onclick="cancelExtendStay()">Cancel</button>
                          <form action="${extendUrl}" method="POST">
                          <input type="hidden" name="guest_id" value="${guestId}">
                          <input type="hidden" name="new_duration" value="${newStayDuration}">
                          <button type="submit" class="btn btn-primary" id="confirmBtn"">Confirm New Date</button>
                        </form>`;
}


function confirmExtend() {
  const modal = document.getElementById('verticalycentered');
  const modalBody = modal.querySelector('.modal-body');
  const modalFooter = modal.querySelector('.modal-footer');
  const newCheckoutDate = document.getElementById('newCheckoutDate').innerHTML;
  const guestName = document.getElementById('guestName').innerHTML;


  // Restore the initial modal content
  modalBody.innerHTML = `<div class= "breadcrumb">
        <div>This room is currently occupied by: <span style = "color: #00796b; font-weight: bold">` + guestName + `</span></div>
        <div>Current Checkout Date: <span id="currentCheckoutDate" style = "color: #00796b; font-weight: bold">` + newCheckoutDate + `</span></div>
       </div>`;
  modalFooter.innerHTML = window.initialModalFooterContent;



  // Change the content of the span
  spanElement.innerHTML = newStayDuration;


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
    const guestCheckoutInput = this.querySelector('input[name="guest_checkout"]');
    const roomQuerysetInput = this.querySelector('input[name="room_queryset"]');
    const guestId = guestIdInput ? guestIdInput.value : null;
    const guestName = guestNameInput ? guestNameInput.value : null;
    const guestCheckout = guestCheckoutInput ? guestCheckoutInput.value : null;
    const roomQueryset = roomQuerysetInput ? roomQuerysetInput.value : null;

    // Show the modal with the occupancy status and guest ID
    showModalWithOccupancyStatus(roomNumber, isOccupied, guestId, guestName, guestCheckout, roomQueryset);
  });
});



