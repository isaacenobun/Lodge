

// document.getElementById('add-suite').addEventListener('click', function () {
//     const suitesContainer = document.getElementById('suites-container');
//     const suiteCount = suitesContainer.getElementsByClassName('suite').length;
//     const newSuiteIndex = suiteCount + 1;

//     const newSuiteDiv = document.createElement('div');
//     newSuiteDiv.classList.add('suite');

//     newSuiteDiv.innerHTML = `
//         <label for="suite_type_${newSuiteIndex}">Suite Type</label>
//         <input type="text" name="suite_type_${newSuiteIndex}" required>

//         <label for="suite_price_${newSuiteIndex}">Suite Price</label>
//         <input type="number" name="suite_price_${newSuiteIndex}" min="0" required>

//         <label for="suite_rooms_${newSuiteIndex}">Number of Rooms for this Suite</label>
//         <input type="number" name="suite_rooms_${newSuiteIndex}" min="0" class="room-count" data-suite-index="${newSuiteIndex}" required>

//         <div class="room-tags" id="room_tags_${newSuiteIndex}"></div>
//     `;

//     suitesContainer.appendChild(newSuiteDiv);
// });


document.getElementById('customRoomTags').addEventListener('click', function () {
    const roomCountInputs = document.querySelectorAll('.room-count');
    roomCountInputs.forEach(function (input) {
        const suiteIndex = input.dataset.suiteIndex;
        const roomCount = parseInt(input.value);
        const roomTagsDiv = document.getElementById(`room_tags_${suiteIndex}`);

        // Clear existing room tags
        roomTagsDiv.innerHTML = '';

        // Add new room tag fields
        for (let i = 1; i <= roomCount; i++) {
            const roomTagInput = document.createElement('div');
            roomTagInput.innerHTML = `
                <label for="room_tag_${suiteIndex}_${i}">Room Tag ${i}</label>
                <input type="text" name="room_tag_${suiteIndex}_${i}" required>
            `;
            roomTagsDiv.appendChild(roomTagInput);
        }
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
                  </tr>
        `;
    }

    // Function to reset the form fields
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

        // Validate the form fields
        if (suiteType && suiteRooms && suitePrice) {
            const suite = {
                type: suiteType,
                rooms: suiteRooms,
                price: suitePrice
            };

            // Insert the suite details into the table
            insertSuiteDetailsIntoTable(suite);

            // Reset the form fields for new entry
            resetFormFields();
        } else {
            alert('Please fill out all the fields before adding another suite.');
        }
    });

    // Event listener for the form submission
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        // Here you would typically gather all the form data
        // and send it to the server using AJAX or a similar method.
        // For demonstration purposes, we'll just log the data to the console.
        const formData = new FormData(form);
        for (const [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }
        // Send the form data to the backend
        // Example: axios.post('/your-endpoint', formData);
    });
});
