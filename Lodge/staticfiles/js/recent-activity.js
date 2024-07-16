// Sample data for demonstration purposes
const activities = [
  { label: '32 min', type: 'checkout', guest: 'John Doe' },
  { label: '2 hrs', type: 'visitor', guest: 'John Doe' },
  { label: '1 day', type: 'reservation' },
  { label: '2 days', type: 'check-in' },
  { label: '4 weeks', type: 'room_service' },
];

// Function to calculate time difference
function getTimeDifference(checkInTimestamp) {
  const now = new Date();
  const checkInTime = new Date(checkInTimestamp);
  const diffInMilliseconds = now - checkInTime;
  const minutes = Math.floor(diffInMilliseconds / (1000 * 60));
  return minutes;
}

// Example usage: Assuming check-in time is stored as a timestamp
const checkInTimestamp = Date.parse('2024-05-31T10:00:00'); // Replace with actual timestamp

// Update activity list dynamically
activities.forEach((activity) => {
  const activityLabel = document.querySelector(`.activite-label:contains("${activity.label}")`);
  if (activityLabel) {
    const timeDifference = getTimeDifference(checkInTimestamp);
    activityLabel.textContent = `${timeDifference} min`;

    const activityContent = activityLabel.nextElementSibling;
    switch (activity.type) {
      case 'checkout':
        activityContent.innerHTML = `Guest <a href="#" class="fw-bold text-dark">${activity.guest}</a> checked out of room.`;
        break;
      case 'visitor':
        activityContent.innerHTML = `Guest <a href="#" class="fw-bold text-dark">${activity.guest}</a> is received a visitor.`;
        break;
      case 'reservation':
        activityContent.textContent = `Guest <a href="#" class="fw-bold text-dark">${activity.guest}</a> made a reservation.`;
        break;
      case 'check-in':
        activityContent.innerHTML = `Guest <a href="#" class="fw-bold text-dark">${activity.guest}</a> checked into room X.`;
        break;
      case 'room_service':
        activityContent.textContent = `Guest <a href="#" class="fw-bold text-dark">${activity.guest}</a> ordered room service.`;
        break;
      default:
        break;
    }
  }
});
