const classSelect = document.getElementById('class');
const StudentsSelect = document.getElementById('Students');
const userInput = document.querySelector('#studentId');

userInput.addEventListener('input', processinput)
function processinput() {
     // Get the input element
     const processedValue = userInput.value.toLowerCase().replace(/\s/g, '');
     userInput.value = processedValue;
}

classSelect.addEventListener('input',populateClass);

function populateClass() {
   const classname = classSelect.value;
     if (classname) {
          fetch(`/Result_portal/${classname}`)
               .then(response => response.json())
               .then(data => {
                    StudentsSelect.innerHTML = '';
                    console.log(data)
                    data.forEach(student => {
                         const option = document.createElement('option');
                         option.value = student.student_name;
                         option.textContent = student.student_name;
                         StudentsSelect.appendChild(option);
                    });
               })
               .catch(error => console.error(error));
     } else {
          StudentsSelect.innerHTML = '';
     }  
}
