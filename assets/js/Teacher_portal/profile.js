(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })
})()


const roleSelect = document.getElementById("roleSelect")

roleSelect?.addEventListener("input", () => {
  toggleClassFormed(roleSelect)
})

function toggleClassFormed(roleSelect) {
  const classFormedContainer = document.getElementById("classFormedContainer");
  if (roleSelect.value === "ClassTeacher") {
    classFormedContainer.style.display = "block";
    document.getElementById("classFormedSelect").required = true;
  } else {
    classFormedContainer.style.display = "none";
    document.getElementById("classFormedSelect").required = false;
  }
}

// Call the function on page load to set the initial state
document.addEventListener("DOMContentLoaded", function () {
  const roleSelect = document.getElementById("roleSelect");
  toggleClassFormed(roleSelect);
});
