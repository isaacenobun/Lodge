
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



document.addEventListener('DOMContentLoaded', function () {
  const selectElement = document.getElementById('suite');
  const showcaseElement = document.querySelector('.showcase');
  const editButton = document.createElement('button');
  const saveButton = document.createElement('button');
  const modalElement = document.getElementById('verticalycentered');

  // Prevent the modal from showing if it is disabled
  modalElement.addEventListener('show.bs.modal', function (event) {
    if (modalElement.classList.contains('disabled')) {
      event.preventDefault();
    }
  });

  let originalContent = {};

  function disableModal() {
    modalElement.classList.add('disabled');
  }

  // Function to enable the modal
  function enableModal() {
    modalElement.classList.remove('disabled');
  }

  editButton.type = 'button';
  editButton.id = 'editButton'
  editButton.className = 'btn btn-link';
  editButton.textContent = 'Edit tags';
  editButton.style.display = 'none'; // Initially hidden

  saveButton.type = 'button';
  saveButton.className = 'btn btn-link';
  saveButton.textContent = 'Save Changes';
  saveButton.style.display = 'none'; // Initially hidden

  selectElement.addEventListener('change', function () {
    if (selectElement.value) {
      editButton.style.display = 'block';
    } else {
      editButton.style.display = 'none';
      saveButton.style.display = 'none';
      resetContent();
    }
  });

  editButton.addEventListener('click', function () {
    disableModal();
    saveButton.style.display = 'inline-block';
    document.body.classList.add('no-hover');

    document.querySelectorAll('.room-tag').forEach(div => {
      originalContent[div.dataset.id] = div.innerHTML;
      div.contentEditable = true;
      div.classList.add('editable');
    });
  });

  saveButton.addEventListener('click', function () {

    saveButton.style.display = 'none';
    document.body.classList.remove('no-hover');
    document.querySelectorAll('.room').forEach(div => {
      div.classList.remove('no-click');
    });
    document.querySelectorAll('.room-tag').forEach(div => {
      div.contentEditable = false;
      div.classList.remove('editable');
    });
    enableModal();
    var form = document.getElementById('edit-form');
    form.submit();
  });

  document.querySelectorAll('.room-tag').forEach(div => {

    // Get the hidden input field within the same div
    var hiddenInput = div.querySelector('input[name="room_tags"]');

    // Listen for input events on the div
    div.addEventListener('input', function () {
        // Update the hidden input value with the edited content of the div
        hiddenInput.value = div.textContent.trim();
    });
});

  function resetContent() {
    document.body.classList.remove('no-hover');
    document.querySelectorAll('.room').forEach(div => {
      div.classList.remove('no-click');
    });
    document.querySelectorAll('.room-tag').forEach(div => {
      div.innerHTML = originalContent[div.dataset.id];
      div.contentEditable = false;
      div.classList.remove('editable');
    });
  }

  showcaseElement.parentNode.insertBefore(editButton, showcaseElement.nextSibling);
  showcaseElement.parentNode.insertBefore(saveButton, showcaseElement.nextSibling);
});








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
        <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
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
function handleExtendStay(guestId, extendUrl) {
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
function confirmExtendStay(guestId, extendUrl) {
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
                          <form id="extend-form" action="${extendUrl}" method="POST">
                          <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                          <input type="hidden" name="guest_id" value="${guestId}">
                          <input type="hidden" name="new_duration" value="${newStayDuration}">
                          <button type="button" onclick="submitExtendForm(${extendUrl},${guestId},${newStayDuration})" class="btn btn-primary" id="confirmBtn">Confirm New Date</button>
                        </form>`;
}

function submitExtendForm(extendUrl,guestId,newDuration) {
  // Create a new form element
  var form = document.createElement('form');
  form.setAttribute('method', 'POST');
  form.setAttribute('action', extendUrl);
  
  // Get CSRF token
  var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Create hidden input elements for each value you want to submit
  var csrfInput = document.createElement('input');
  csrfInput.setAttribute('type', 'hidden');
  csrfInput.setAttribute('name', 'csrfmiddlewaretoken');
  csrfInput.setAttribute('value', csrftoken);
  form.appendChild(csrfInput);

  var guestIdInput = document.createElement('input');
  guestIdInput.setAttribute('type', 'hidden');
  guestIdInput.setAttribute('name', 'guest_id');
  guestIdInput.setAttribute('value', guestId);
  form.appendChild(guestIdInput);

  var newDurationInput = document.createElement('input');
  newDurationInput.setAttribute('type', 'hidden');
  newDurationInput.setAttribute('name', 'new_duration');
  newDurationInput.setAttribute('value', newDuration);
  form.appendChild(newDurationInput);

  // Append the form to the body (it's necessary for submission)
  document.body.appendChild(form);

  // Submit the form
  form.submit();

  // Remove the form from the DOM
  document.body.removeChild(form);
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



