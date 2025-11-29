const classSelect = document.getElementById('class');
const academicSessionSelect = document.getElementById('academicSession');
const StudentsSelect = document.getElementById('Students');
const userInput = document.querySelector('#studentId');

userInput.addEventListener('input', processinput)
function processinput() {
     // Get the input element
     const processedValue = userInput.value.toUpperCase().replace(/\s/g, '');
     userInput.value = processedValue;
}

classSelect.addEventListener('input',populateClass);
academicSessionSelect.addEventListener('input', populateClass);

function populateClass() {
    const classname = classSelect.value;
    const session = academicSessionSelect.value;

    // Only run request if BOTH are selected
    if (classname && session) {
        fetch(`/Student_Portal/${classname}?session=${session}`)
            .then(response => response.json())
            .then(data => {
                StudentsSelect.innerHTML = '';
                data.forEach(student => {
                    const option = document.createElement('option');
                    option.value = student.student_name;
                    option.textContent = student.student_name;
                    StudentsSelect.appendChild(option);
                });
            })
            .catch(error => console.error(error));
    } else {
        // Clear list if either is missing
        StudentsSelect.innerHTML = '';
    }
}

