import { showSpinner, hideSpinner } from "../../utils/displayspinner.js";

// -----------------------------------------------------------
// getting from the server
// -----------------------------------------------------------
async function getstudentdata(url,classdata) {
  if (
    classdata.selectedTerm === "" ||
    classdata.selectedAcademicSession === "" ||
    classdata.studentsubject === ""
  ) {
    return;
  }
  showSpinner("updatesubjectspinner", "subjectbtnmessage", "Loading...");
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(classdata),
  });
  const data = await response.json();
  hideSpinner("updatesubjectspinner", "subjectbtnmessage", "load Results");
  return data;
}

// ---------------------------------------------------
// function to get Student Annual Result
// ---------------------------------------------------
async function getannualresultdata(url,classdata) {
  showSpinner("updatesubjectspinner", "subjectbtnmessage", "Loading...");
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(classdata),
  });
  const data = await response.json();
  hideSpinner("updatesubjectspinner", "subjectbtnmessage", "load Results");
  return data;
}

// -----------------------------------------------------
// Function to get Class Annual Result
// ------------------------------------------------------
async function getannualclassresult(classdata) {
  const response = await fetch(`/Teachers_Portal/annualclassresultcomputation/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(classdata),
  });
  const data = await response.json();
  return data;
}

// -----------------------------------------------------------
// Function to update student result on the server
// -----------------------------------------------------------
function updatestudentresult(
  url,
  formDataObject,
  classdata,
  readJsonFromFile,
  displayalert
) {
  if (
    classdata.selectedTerm === "" ||
    classdata.selectedAcademicSession === "" ||
    classdata.studentsubject === ""
  ) {
    return;
  }
  const fullresultdata = {
    formDataObject,
    classdata,
  };
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(fullresultdata),
  })
    .then((response) => response.json())
    .then((data) => {
      readJsonFromFile();
      const type = "alert-success";
      const message = data;
      displayalert(type, message);
    })
    .catch((error) => console.error("Error:", error));
}

// -----------------------------------------------------------
// Function to submit all students result to the server
// -----------------------------------------------------------
function submitallstudentresult(url, data, classdata, displayalert) {
  const resulttosubmit = {
    data,
    classdata,
  };
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(resulttosubmit),
  })
    .then((response) => response.json())
    .then((data) => {
      const type = "alert-success";
      const message = data;
      displayalert(type, message);
    })
    .catch((error) => console.error("Error:", error));
}

// -----------------------------------------------------------
// function to get class result
// -----------------------------------------------------------
async function getstudentresult(url,classdata) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(classdata),
  });
  const data = await response.json();
  return data;
}

// -----------------------------------------------------------
// Function to publish class result
// -----------------------------------------------------------
function publishstudentresult(url, data, classdata, displayalert) {
  const fulldata = {
    data,
    classdata,
  };
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify(fulldata),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.type === "success") {
        const type = "alert-success";
        const message = data.message;
        displayalert(type, message);
      } else if (data.type === "error") {
        const type = "alert-danger";
        const message = data.message;
        displayalert(type, message);
      } else {
        console.error("Unexpected response type:", data.type);
      }
    })
    .catch((error) => console.error("Error:", error));
}

export {
  getstudentdata,
  getannualclassresult,
  getannualresultdata,
  updatestudentresult,
  submitallstudentresult,
  getstudentresult,
  publishstudentresult,
};
