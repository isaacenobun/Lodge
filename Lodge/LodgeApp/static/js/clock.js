function showTime() {
  var date = new Date();
  var days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  var shortDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var day = days[date.getDay()];
  var shortDay = shortDays[date.getDay()];
  var dayOfMonth = date.getDate();
  var month = date.getMonth() + 1; // Months are zero-based
  var year = date.getFullYear();
  var h = date.getHours(); // 0 - 23
  var m = date.getMinutes(); // 0 - 59
  var session = "AM";

  if (h == 0) {
    h = 12;
  }

  if (h > 12) {
    h = h - 12;
    session = "PM";
  }

  h = (h < 10) ? "0" + h : h;
  m = (m < 10) ? "0" + m : m;

  var fullTime = day + ", " + month + "/" + dayOfMonth + "/" + year + " " + h + ":" + m + " " + session;
  var mobileTime = shortDay + ", " + month + "/" + dayOfMonth + "/" + year;

  document.getElementById("MyClockDisplay").innerHTML =
    `<span class="mobile-display">${mobileTime}</span><span class="full-display">${fullTime}</span>`;

  setTimeout(showTime, 1000);
}

showTime();
