// Flag to control the update behavior
let allowUpdate = true;


document.getElementById('customRoomTags').addEventListener('click', function () {

    // Re-enable updates
    allowUpdate = true;

    const roomCountInputs = document.querySelectorAll('.room-count');
    roomCountInputs.forEach(function (input) {
        // Add event listener for 'input' event
        input.addEventListener('input', updateRoomTags);

        // Initial call to set up the room tags
        updateRoomTags.call(input);
    });
});

function updateRoomTags() {
    // Exit the function if updates are not allowed
    if (!allowUpdate) return;

    const suiteIndex = this.dataset.suiteIndex;
    const roomCount = parseInt(this.value);
    const roomTagsDiv = document.getElementById(`suites-container`);
    roomTagsDiv.style.display = 'flex';
    roomTagsDiv.style.flexWrap = 'wrap';
    roomTagsDiv.style.justifyContent = 'center';

    // Clear existing room tags
    roomTagsDiv.innerHTML = '';


    // Add new room tag fields only if updates are allowed
    if (allowUpdate) {
        // Add new room tag fields
        for (let i = 1; i <= roomCount; i++) {
            const roomTagInput = document.createElement('div');
            roomTagInput.classList.add('form-floating');
            roomTagInput.classList.add('small');
            roomTagInput.style.maxWidth = '15%';
            roomTagInput.style.minWidth = '15%';
            roomTagInput.style.margin = '2px 2px';
            roomTagInput.innerHTML = `
                <input class="form-control" type="text" id="room_tag_${suiteIndex}_${i}" placeholder="Tag ${i}" name="room_tag_${suiteIndex}_${i}" required>
                <label class="form-label" for="room_tag_${suiteIndex}_${i}">Tag ${i}</label>
            `;
            roomTagsDiv.appendChild(roomTagInput);
        }
    }
}


// Event listener for the 'Add another suite' button
document.getElementById('add-suite').addEventListener('click', function () {
    // Disable updates
    allowUpdate = false;

    // clear all room tags divs
    const roomTagsDivs = document.querySelectorAll('[id^="suites-container"]');
    roomTagsDivs.forEach(function (div) {
        div.innerHTML = ''; // Clear the content of each room tags div
    });
});



document.addEventListener('DOMContentLoaded', function () {
    const suitesContainer = document.getElementById('suites-container');
    const addSuiteBtn = document.getElementById('add-suite');
    const form = document.querySelector('form');
    const table = document.querySelector('.table-bordered tbody');
    const tablestyle = document.querySelector('.table-bordered');

    let suiteCount = 0;

    // Function to display suite details
    function insertSuiteDetailsIntoTable(suite) {
        tablestyle.style.display = '';
        suiteCount++;
        const row = table.insertRow();
        row.innerHTML = `
                  <tr>
                    <th scope="row">${suiteCount}</th>
                    <td>${suite.type}</td>
                    <td>${suite.rooms}</td>
                    <td>${suite.price}</td>
                    <button
                        type="button"
                        class="btn-close btn-lg text-center"
                        data-bs-dismiss="row"
                        aria-label="Close"
                    ></button>
                  </tr>
        `;

        // Find the close button in the row and add a click event listener
        const closeButton = row.querySelector('.btn-close');
        closeButton.addEventListener('click', function () {
            // Find the index of the row
            const rowIndex = Array.from(row.parentNode.children).indexOf(row);

            // This will remove the row containing the button
            row.remove();

            // Remove the suite details from the array using the index
            suitesArray.splice(rowIndex, 1);
            console.log('Suite removed at index:', rowIndex);
            console.log('Updated suitesArray:', suitesArray);





            // Decrement the suiteCount since a row has been deleted
            suiteCount--;

            // Update the suite numbers for all remaining rows
            const allRows = table.querySelectorAll('tbody tr');
            allRows.forEach((row, index) => {
                row.querySelector('th').textContent = index + 1;
            });
            // Call checkTableEmpty to determine if the header should be shown or hidden
            checkTableEmpty();
        });
    }


    // Function to check if the table body is empty and hide the header if it is
    function checkTableEmpty() {
        const tableBody = document.querySelector('.table tbody');
        if (tableBody.rows.length === 0) { // Check if there are no rows in the tbody
            document.querySelector('.table thead').style.display = 'none';
        } else {
            document.querySelector('.table thead').style.display = '';
        }
    }

    // Call checkTableEmpty when the document is loaded or when the table is initially populated
    document.addEventListener('DOMContentLoaded', checkTableEmpty);


    // Function to reset specific form fields
    function resetFormFields() {
        document.getElementById('suite_type_1').value = '';
        document.getElementById('suite_rooms_1').value = '';
        document.getElementById('suite_price_1').value = '';
    }


    let suitesArray = [];


    // Event listener for the Add another suite button
    addSuiteBtn.addEventListener('click', function () {
        const suiteType = document.getElementById('suite_type_1').value;
        const suiteRooms = document.getElementById('suite_rooms_1').value;
        const suitePrice = document.getElementById('suite_price_1').value;

        // Validate the form fields
        if (suiteType && suiteRooms && suitePrice) {
            const suite = {
                type: suiteType,
                rooms: suiteRooms,
                price: suitePrice
            }

            // Push the suite details into the array
            suitesArray.push(suite);
            console.log('Suite added:', suite);
            console.log('Current suitesArray:', suitesArray);


            // Insert the suite details into the table
            insertSuiteDetailsIntoTable(suite);

            // Reset the form fields for new entry
            resetFormFields();
        } else {
            alert('Please fill out all the fields before adding another suite.');
        }
    });




    // Function to display suitesArray in the table body of the modal
    function displaySuitesInModal() {
        // Get the value of the input field with id="company_name"
        var companyName = document.getElementById('company_name').value;

        var modalTitle = document.querySelector('.modal-title');

        // Set the text content of the element
        modalTitle.textContent = companyName;



        // Get the table body within the modal
        const tableBody = document.querySelector('#verticalycentered .modal-body tbody');

        // Clear any existing rows in the table body
        tableBody.innerHTML = '';

        // Iterate over the suitesArray and create table rows
        suitesArray.forEach((suite, index) => {
            const row = tableBody.insertRow();
            row.innerHTML = `
                <tr>
                    <th scope="row">${index + 1}</th>
                    <td>${suite.type}</td>
                    <td>${suite.rooms}</td>
                    <td>${suite.price}</td>
                </tr>
            `;
        });

        // Show the table if it was previously hidden
        const table = document.querySelector('#verticalycentered .modal-body table');
        table.style.display = 'table';
    }

    // Attach the displaySuitesInModal function to the submit button's click event
    document.querySelector('.btn.btn-primary.btn-lg.w-100[type="submit"]').addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default form submission
        displaySuitesInModal();
    });
});
