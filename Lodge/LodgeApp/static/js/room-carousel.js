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

// Movie Select Event
movieSelect.addEventListener('change', e => {
  ticketPrice = +e.target.value;
  updateUI();
});

// Seat click event
container.addEventListener('click', e => {
  if (e.target.classList.contains('seat') && !e.target.classList.contains('occupied')) {
    e.target.classList.toggle('selected');
  }
  updateUI();
});


function showProfile(name) {
  // Replace this with your logic to load the profile page dynamically
  // For demonstration purposes, we'll just navigate to a different URL
  // based on the person's name.
  const profileUrl = `${name}.html`;
  window.location.href = profileUrl;
}



