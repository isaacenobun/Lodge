// Flag to control the update behavior
let allowUpdate = true;

let suitesArray = [];


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
    const addSuiteBtn = document.getElementById('add-suite');
    const table = document.querySelector('.table-bordered tbody');
    const tablestyle = document.querySelector('.table-bordered');
    const submitButton = document.querySelector('#submitButton');

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
        checkTableEmpty();
    }


    // Function to check if the table body is empty and hide the header if it is
    function checkTableEmpty() {
        if (suitesArray.length === 0) { // Check if the suitesArray is empty
            document.querySelector('.table thead').style.display = 'none';
        } else {
            document.querySelector('.table thead').style.display = '';
            // If not empty, remove the 'disabled' class
            submitButton.classList.remove('disabled');
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





    // Event listener for the Add another suite button
    addSuiteBtn.addEventListener('click', function () {
        const suiteType = document.getElementById('suite_type_1').value;
        const suiteRooms = document.getElementById('suite_rooms_1').value;
        const suitePrice = document.getElementById('suite_price_1').value;
        const companyName = document.getElementById('company_name').value;


        // Validate the form fields
        if (suiteType && suiteRooms && suitePrice && companyName) {
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
            alert('Please fill out all the fields before adding a suite.');
        }
    });


    // Function to display suitesArray in the table body of the modal
    function displaySuitesInModal() {
        // Get the value of the input field with id="company_name"
        var companyName = document.getElementById('company_name').value;

        var modalTitle = document.querySelector('.modal-title');

        var modalBody = document.querySelector('.modal-body .card-subtitle');

        modalBody.textContent = "Please confirm the following details";

        // Set the text content of the element
        modalTitle.textContent = companyName;



        // Get the table body within the modal
        const tableBody = document.querySelector('#verticalycentered .modal-body tbody');

        // Clear any existing rows in the table body
        tableBody.innerHTML = '';

        // Get the table body within the modal
        const tableHead = document.querySelector('#verticalycentered .modal-body table thead');
        // Clear any existing rows in the table body
        tableHead.innerHTML = `<tr>
                                    <th scope="col">#</th>
                                    <th scope="col">Type</th>
                                    <th scope="col">Rooms</th>
                                    <th scope="col">Price</th>
                                  </tr>`;

        // Iterate over the suitesArray and create table rows
        suitesArray.forEach((suite, index) => {
            const row = tableBody.insertRow();
            row.innerHTML = `
                <tr>
                    <th scope="row">${index + 1}</th>
                    <td>${suite.type}</td>
                    <td>${suite.rooms}</td>
                    <td>${suite.price}</td>
                    <input type="hidden" name="suite_type_${index + 1}" value="${suite.type}"/>
                    <input type="hidden" name="suite_rooms_${index + 1}" value="${suite.rooms}"/>
                    <input type="hidden" name="suite_price_${index + 1}" value="${suite.price}"/>
                </tr>
            `;
        });

        // Show the table if it was previously hidden
        const table = document.querySelector('#verticalycentered .modal-body table');
        table.style.display = 'table';

    }

    // Attach the displaySuitesInModal function to the submit button's click event
    document.querySelector('.btn.btn-dark.btn-lg.w-100[type="submit"]').addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Check if suitesArray is empty before displaying the modal
        if (suitesArray.length === 0) {
            // Access the element
            var element = document.getElementById('verticalycentered');

            // Change the value of the 'class' attribute
            element.style.display = '';

            updateModalContent();
        } else {
            // If suitesArray is not empty, display the modal with the suite details
            displaySuitesInModal();
            console.log(suitesArray.length)
        }
    });

});


// Function to update modal content
function updateModalContent() {
    // Update the text inside the <span> element
    var modalBody = document.querySelector('.modal-body .card-subtitle');

    modalBody.textContent = 'You have not added any suites, Please click on the add suite button to add a suite';


    // Get the table body within the modal
    const tableHead = document.querySelector('#verticalycentered .modal-body table thead');
    // Clear any existing rows in the table body
    tableHead.innerHTML = '';

    // Get the table body within the modal
    const tableBody = document.querySelector('#verticalycentered .modal-body table tbody');
    // Clear any existing rows in the table body
    tableBody.innerHTML = '';
}


document.addEventListener('DOMContentLoaded', function () {
    // Get a reference to the button element


    // Check if suitArray is empty
    if (Array.isArray(suitesArray) && suitesArray.length === 0) {
        // If empty, add the 'disabled' class
        submitButton.classList.add('disabled');
    } else {
        // If not empty, remove the 'disabled' class
        submitButton.classList.remove('disabled');
    }
});
