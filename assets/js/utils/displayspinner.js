function showSpinner(spinnerID,textID,text) {
  const textelement = document.getElementById(textID);
  textelement.innerHTML = text;
  const spinner = document.getElementById(spinnerID);
  spinner.classList.remove("d-none");
}

function hideSpinner(spinnerID,textID,text) {
  const textelement = document.getElementById(textID);
  textelement.innerHTML = text;
  const spinner = document.getElementById(spinnerID);
  spinner.classList.add("d-none");
}

export { showSpinner, hideSpinner };
