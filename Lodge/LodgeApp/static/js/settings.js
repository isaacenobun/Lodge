document.body.addEventListener('click', function(event) {
  if (event.target.classList.contains('editButton')) {
    var cardProfile = event.target.closest('.card-profile');
    var span = cardProfile.querySelector('.current-text');
    var currentText = span.textContent;
    var labelText = cardProfile.dataset.label;
    var uniqueId = 'input_' + cardProfile.dataset.id;

    var inputBox = document.createElement('input');
    inputBox.type = 'text';
    inputBox.className = 'form-control';
    inputBox.name = uniqueId;
    inputBox.id = uniqueId; // Set the unique id for the input box
    inputBox.value = currentText; // Set the value of the input box to the current text

    var label = document.createElement('label');
    label.className = 'form-label small';
    label.htmlFor = uniqueId; // Associate the label with the input box
    label.textContent = labelText;

    var invalidFeedback = document.createElement('div');
    invalidFeedback.className = 'invalid-feedback';
    invalidFeedback.textContent = 'Please, enter a value!';

    var formFloatingDiv = document.createElement('div');
    formFloatingDiv.className = 'form-floating';
    formFloatingDiv.appendChild(inputBox);
    formFloatingDiv.appendChild(label);
    formFloatingDiv.appendChild(invalidFeedback);

    span.replaceWith(formFloatingDiv);

    // Change the edit button to a cancel button
    var cancelButton = document.createElement('button');
    cancelButton.type = 'button';
    cancelButton.className = 'btn btn-link small cancelButton';
    cancelButton.textContent = 'Cancel';
    event.target.replaceWith(cancelButton);

    // Add event listener to the cancel button to restore the original state
    cancelButton.addEventListener('click', function() {
      formFloatingDiv.replaceWith(span);
      cancelButton.replaceWith(event.target);
    });
  }
});

document.getElementById('settings-add-suite').addEventListener('click', function() {
  const buttonGroupRow = document.getElementById('button-group-row');

  const newRow = document.createElement('div');
  newRow.className = 'row suite-row';

  newRow.innerHTML = `
    <div class="col-md-4">
      <div class="card-profile" data-id="2" data-label="Suite Type">
        <div class="profile-box"><i class="bi bi-door-open"></i><span class="current-text">Suite Type</span></div>
        <button type="button" class="btn btn-link small editButton">Edit</button>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card-profile" data-id="3" data-label="Rooms">
        <div class="profile-box"><i class="bi bi-grid-3x3-gap"></i><span class="current-text">Rooms</span></div>
        <button type="button" class="btn btn-link small editButton">Edit</button>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card-profile" data-id="4" data-label="Current Price">
        <div class="profile-box"><i class="custom-icon">₦</i><span class="current-text">Price</span></div>
        <button type="button" class="btn btn-link small editButton">Edit</button>
      </div>
    </div>
  `;

  buttonGroupRow.parentNode.insertBefore(newRow, buttonGroupRow);
});

document.getElementById('reset-button').addEventListener('click', function() {
  // Remove all dynamically added rows
  const addedRows = document.querySelectorAll('.suite-row');
  addedRows.forEach(row => row.remove());

  // Reset the form fields
  const form = document.querySelector('form');
  form.reset();
});


// document.addEventListener('click', function (event) {
//   if (event.target && event.target.classList.contains('editButton')) {
//     const cardProfile = event.target.closest('.card-profile');
//     const formFloating = event.target.getAttribute('data-form');
//     cardProfile.outerHTML = formFloating;
//   }
// });


// document.addEventListener('DOMContentLoaded', function () {
//   const addSuiteButton = document.getElementById('settings-add-suite');
//   const form = document.querySelector('.row.g-2');

//   addSuiteButton.addEventListener('click', function () {
//     const newRow = document.createElement('div');
//     newRow.classList.add('row');

//     newRow.innerHTML = `
//         <!-- Suite Type -->
//         <div class="col-md-4">
//           <div class="card-profile">
//             <div class="profile-box"><i class="bi bi-door-open"></i><span> New Suite</span></div>
//             <button type="button" class="btn btn-link small editButton" data-form='<div class="form-floating">
//             <input
//               type="text"
//               class="form-control"
//               name="suite_type"
//               placeholder="Suite type"
//             />
//             <label class="form-label small">Suite type</label>
//             <div class="invalid-feedback">
//               Please, enter a value!
//             </div>
//             </div>'>Edit</button>
//           </div>
//         </div>
      
//         <!-- No of rooms -->
//         <div class="col-md-4">
//           <div class="card-profile">
//             <div class="profile-box"><i class="bi bi-grid-3x3-gap"></i><span>Rooms</span></div>
//             <button type="button" class="btn btn-link small editButton" data-form='<div class="form-floating">
//             <input
//               type="number"
//               name="suite_rooms"
//               min="1"
//               class="room-count form-control"
//               placeholder="Rooms in suite"
//             />
//             <label class="form-label small">Rooms in Suite</label>
//             <div class="invalid-feedback">
//               Please, enter a value!
//             </div>
//             </div>'>Edit</button>
//           </div>
//         </div>

//         <!-- Current price -->
//         <div class="col-md-4">
//           <div class="card-profile">
//             <div class="profile-box"><i class="custom-icon">₦</i><span>Price</span></div>
//             <button type="button" class="btn btn-link small editButton" data-form='<div class="form-floating">
//             <input
//               type="number"
//               class="form-control"
//               name="suite_price"
//               min="0"
//               placeholder="Price"
//             />
//             <label class="form-label small">Price</label>
//             <div class="invalid-feedback">
//               Please, enter a value!
//             </div>
//             </div>'>Edit</button>
//           </div>
//         </div>
//       `;

//     form.insertBefore(newRow, form.querySelector('.btn-group').parentNode);
//   });
// });

