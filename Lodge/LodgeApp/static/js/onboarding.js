

document.getElementById('add-suite').addEventListener('click', function() {
    const suitesContainer = document.getElementById('suites-container');
    const suiteCount = suitesContainer.getElementsByClassName('suite').length;
    const newSuiteIndex = suiteCount + 1;
    
    const newSuiteDiv = document.createElement('div');
    newSuiteDiv.classList.add('suite');
    
    newSuiteDiv.innerHTML = `
        <label for="suite_type_${newSuiteIndex}">Suite Type</label>
        <input type="text" name="suite_type_${newSuiteIndex}" required>
        
        <label for="suite_price_${newSuiteIndex}">Suite Price</label>
        <input type="number" name="suite_price_${newSuiteIndex}" min="0" required>
        
        <label for="suite_rooms_${newSuiteIndex}">Number of Rooms for this Suite</label>
        <input type="number" name="suite_rooms_${newSuiteIndex}" min="0" class="room-count" data-suite-index="${newSuiteIndex}" required>
        
        <div class="room-tags" id="room_tags_${newSuiteIndex}"></div>
    `;
    
    suitesContainer.appendChild(newSuiteDiv);
});

document.addEventListener('input', function(e) {
    if (e.target && e.target.classList.contains('room-count')) {
        const suiteIndex = e.target.dataset.suiteIndex;
        const roomCount = parseInt(e.target.value);
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
    }
});