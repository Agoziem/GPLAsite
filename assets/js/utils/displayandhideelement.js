function toggleVisibility(elementId) {
  const element = document.getElementById(elementId);
  if (element.classList.contains("d-none")) {
    element.classList.remove("d-none");
  } else {
    element.classList.add("d-none");
  }
}

function hideAfterTimeout(elementId, timeout) {
  const element = document.getElementById(elementId);
  setTimeout(() => {
    element.classList.add("d-none");
  }, timeout);
}

export { toggleVisibility, hideAfterTimeout };
