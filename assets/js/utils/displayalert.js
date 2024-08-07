// -----------------------------------------------------
// Function to display alert messages
// ------------------------------------------------------
function displayalert(type, message, parentalertelementID) {
  const alertdiv = document.createElement("div");
  alertdiv.classList.add(
    "alert",
    `${type}`,
    "d-flex",
    "align-items-center",
    "mt-3"
  );
  alertdiv.setAttribute("role", "alert");
  alertdiv.innerHTML = `
                          <i class="fa-solid fa-circle-check me-2"></i>
                          <div>
                             ${message}
                          </div>
                          `;

  const parentalertelement = document.getElementById(parentalertelementID);
  parentalertelement.appendChild(alertdiv);
  setTimeout(() => {
    alertdiv.remove();
  }, 5000);
}

export { displayalert };
