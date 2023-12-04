// Get the Date and Time now 
const currentDate = new Date()

// // Get the date components (year, month, day)
const year = currentDate.getFullYear();
const month = currentDate.getMonth() + 1; // Month is zero-indexed, so adding 1
const day = currentDate.getDate();
const hour = currentDate.getHours();
const minute = currentDate.getMinutes();
const seconds = currentDate.getSeconds();

const formattedDate = `${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`;
const formattedTime =`${hour}:${minute < 10 ? '0':''}${minute}:${seconds < 10 ? '0': ''}${seconds}`;
const infoform = document.getElementById('student_info')

infoform.addEventListener('submit', (e) => {
    e.preventDefault
    document.getElementById('time').value = formattedTime;
    document.getElementById('date').value = formattedDate;
    this.submit();
})

