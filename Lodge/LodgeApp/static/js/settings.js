// Store the initial state of the card profiles
var initialCardProfilesHTML = document.getElementById('card-profiles-container').innerHTML;

document.body.addEventListener('click', function (event) {
  if (event.target.classList.contains('editButton')) {
    var editButton = event.target;
    var isEditing = editButton.textContent === 'Edit';

    if (isEditing) {
      editButton.textContent = 'Cancel';

      // Loop through all card-profile elements
      document.querySelectorAll('.card-profile').forEach(function (cardProfile) {
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
      });
    } else {
      editButton.textContent = 'Edit';

      // Loop through all card-profile elements to reset them
      document.querySelectorAll('.card-profile').forEach(function (cardProfile) {
        var formFloatingDiv = cardProfile.querySelector('.form-floating');
        var inputBox = formFloatingDiv.querySelector('input');
        var currentText = inputBox.value;

        var span = document.createElement('span');
        span.className = 'current-text';
        span.textContent = currentText;

        formFloatingDiv.replaceWith(span);
      });
    }
  }

  if (event.target.id === 'settings-add-suite') {
    addNewSuite();
  }

  if (event.target.id === 'reset-button') {
    resetPage();
  }
});

function addNewSuite() {
  var newId = 'new';

  var newSuiteRow = document.createElement('div');
  newSuiteRow.className = 'row suite-row'; // Add class suite-row for dynamically added rows

  var suiteTypes = [
    { label: 'Suite Type', icon: 'bi bi-door-open' },
    { label: 'Rooms', icon: 'bi bi-grid-3x3-gap' },
    { label: 'Current Price', icon: 'custom-icon', text: '₦' }
  ];

  suiteTypes.forEach(function (suiteType, index) {
    var colDiv = document.createElement('div');
    colDiv.className = 'col-md-4';

    var cardProfileDiv = document.createElement('div');
    cardProfileDiv.className = 'card-profile';
    cardProfileDiv.dataset.id = newId;
    cardProfileDiv.dataset.label = suiteType.label;

    var profileBoxDiv = document.createElement('div');
    profileBoxDiv.className = 'profile-box';

    var icon = document.createElement('i');
    icon.className = suiteType.icon;
    profileBoxDiv.appendChild(icon);

    if (suiteType.text) {
      var customIcon = document.createElement('i');
      customIcon.className = 'custom-icon';
      customIcon.textContent = suiteType.text;
      profileBoxDiv.appendChild(customIcon);
    }

    var span = document.createElement('span');
    span.className = 'current-text';
    span.textContent = suiteType.label;
    profileBoxDiv.appendChild(span);

    cardProfileDiv.appendChild(profileBoxDiv);
    colDiv.appendChild(cardProfileDiv);
    newSuiteRow.appendChild(colDiv);
  });

  // Check if the heading already exists
  var heading = document.querySelector('.new-suites-heading');
  if (!heading) {
    heading = document.createElement('p');
    heading.className = 'text-center card-subtitle mb-3 text-muted small new-suites-heading';
    heading.textContent = 'Newly added suites';
    document.querySelector('#button-group-row').before(heading);
  }


  document.querySelector('#button-group-row').before(newSuiteRow);

  // Check if currently in edit mode
  var editButton = document.querySelector('.editButton');
  if (editButton && editButton.textContent === 'Cancel') {
    // Convert new suite row to edit mode
    newSuiteRow.querySelectorAll('.card-profile').forEach(function (cardProfile) {
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
    });
  }
}

function resetPage() {
  // Remove all dynamically added rows
  const addedRows = document.querySelectorAll('.suite-row');
  addedRows.forEach(row => row.remove());

  // Remove the heading if it exists
  const heading = document.querySelector('.new-suites-heading');
  if (heading) {
    heading.remove();
  }


  // Reset the existing card profiles to their original state
  document.querySelectorAll('.card-profile').forEach(function (cardProfile) {
    var formFloatingDiv = cardProfile.querySelector('.form-floating');
    if (formFloatingDiv) {
      var inputBox = formFloatingDiv.querySelector('input');
      var currentText = inputBox.value;

      var span = document.createElement('span');
      span.className = 'current-text';
      span.textContent = currentText;

      formFloatingDiv.replaceWith(span);
    }
  });

  // Reset the edit button text
  var editButton = document.querySelector('.editButton');
  if (editButton) {
    editButton.textContent = 'Edit';
  }
  window.location.reload();
}

document.querySelectorAll('.editStaffButton, .addstaffButton').forEach(button => {
  button.addEventListener('click', function () {
    const staffName = this.getAttribute('data-staff');
    if (this.classList.contains('editStaffButton')) {
      document.getElementById('modalTitle').innerText = `Editing details for ${staffName}`;
      document.getElementById('modal-footer').innerHTML = `<button type="button" class="btn btn-outline-dark" data-bs-dismiss="modal">Close</button>
                  <button type="button" class="btn btn-dark">Save changes</button>`;
      document.getElementById('modalContent').innerHTML = `<form 
                      class="row g-3 needs-validation"
                      novalidate
                      method="post"
                      action="{% url 'sign-up' %}">

                      <div class="col-12">
                        <label for="yourEmail" class="form-label">Username</label>
                        <input type="text" name="username" class="form-control" id="yourUsername" required />
                        <div class="invalid-feedback">Please enter a username!</div>
                      </div>
                      
                      <div class="col-12">
                        <label for="yourEmail" class="form-label">Email</label>
                        <input type="email" name="email" class="form-control" id="yourEmail" required />
                        <div class="invalid-feedback">Please enter a valid Email address!</div>
                      </div>

                      <div class="col-12">
                        <label for="yourPassword" class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" id="yourPassword" required>
                        <div class="invalid-feedback">Please enter your password!</div>
                      </div>

                      <div class="col-12">
                        <div class="form-check">
                          <input class="form-check-input" name="terms" type="checkbox" value="" id="adminStatus" required>
                          <label class="form-check-label" for="adminStatus">Assign Admin Status</label>
                        </div>
                      </div>
                    </form>`;
    } else if (this.classList.contains('addstaffButton')) {
      document.getElementById('modalTitle').innerText = 'Add New Staff';
      document.getElementById('modal-footer').innerHTML = `<button type="button" class="btn btn-outline-dark" data-bs-dismiss="modal">Close</button>
                  <button type="button" class="btn btn-dark">Submit</button>`;
      document.getElementById('modalContent').innerHTML = `<form 
                      class="row g-3 needs-validation"
                      novalidate
                      method="post"
                      action="{% url 'sign-up' %}">

                      <div class="col-12">
                        <label for="newName" class="form-label">Name</label>
                        <input type="text" name="userName" class="form-control" id="newName" required />
                        <div class="invalid-feedback">Please enter a username!</div>
                      </div>

                      <div class="col-12">
                        <label for="newUsername" class="form-label">Username</label>
                        <input type="text" name="username" class="form-control" id="newUsername" required />
                        <div class="invalid-feedback">Please enter a username!</div>
                      </div>
                      
                      <div class="col-12">
                        <label for="newEmail" class="form-label">Email</label>
                        <input type="email" name="email" class="form-control" id="newEmail" required />
                        <div class="invalid-feedback">Please enter a valid Email address!</div>
                      </div>

                      <div class="col-12">
                        <label for="newPassword" class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" id="newPassword" required>
                        <div class="invalid-feedback">Please enter your password!</div>
                      </div>

                      <div class="col-12">
                        <div class="form-check">
                          <input class="form-check-input" name="terms" type="checkbox" value="" id="newAdminStatus" required>
                          <label class="form-check-label" for="newAdminStatus">Assign Admin Status</label>
                        </div>
                      </div>
                    </form>`;
    }
    $('#verticalycentered').modal('show');
  });
});

