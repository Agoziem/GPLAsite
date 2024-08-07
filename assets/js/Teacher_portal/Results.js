// ---------------------------------------------------------
// Imports
// ---------------------------------------------------------
import StudentDataHandler from "./utils/StudentResulthandler.js";
import DataTable from "./datatable/StudentResultDatatable.js";
import {
  getstudentdata,
  updatestudentresult,
  submitallstudentresult,
} from "./utils/serveractions.js";

//   -----------------------------------------------------------
// DOM elements
// -----------------------------------------------------------
const inputStudentResultModal = document.querySelector(
  "#inputStudentResultModal"
);
const inputform = inputStudentResultModal.querySelector(
  "#inputStudentResultform"
);
const getstudentresultform = document.querySelector("#getstudentresultform");
const subjectselect = getstudentresultform.querySelector("select");
const classinput = getstudentresultform.querySelector("input");
const termSelect = document.getElementById("termSelect");
const academicSessionSelect = document.getElementById("academicSessionSelect");
const rowcheckboxes = document.querySelector(".rowgroup");
document
  .querySelector("#publishbtn")
  .addEventListener("click", exportTableToJSON);
const alertcontainer = document.querySelector(".alertcontainer");

// -----------------------------------------------------------
// Global variables
// -----------------------------------------------------------
let classdata = {
  studentclass: classinput.value,
};
let studentResult = [];
let state;

// -----------------------------------------------------------
// Set Event listeners
// -----------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  loadsavedSelection();
});

document.addEventListener("DOMContentLoaded", () => {
  getstudentresultform.addEventListener("submit", (e) => {
    e.preventDefault();
    saveformSelections();
  });
});

document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("inputStudentResultform")
    .addEventListener("submit", (e) => {
      e.preventDefault();
      const formData = new FormData(inputform);
      const formDataObject = {};
      formData.forEach((value, key) => {
        formDataObject[key] = value;
      });
      classdata.studentsubject =
        subjectselect.options[subjectselect.selectedIndex].value;
      (classdata.selectedTerm = termSelect.value),
        (classdata.selectedAcademicSession = academicSessionSelect.value);
      const url = "/Teachers_Portal/updatestudentresults/";
      updatestudentresult(
        url,
        formDataObject,
        classdata,
        readJsonFromFile,
        displayalert
      );
      $(inputStudentResultModal).modal("hide");
    });
});

// -----------------------------------------------------------
// Function to save selected values to localStorage
// -----------------------------------------------------------
function saveformSelections() {
  localStorage.setItem("selectedresultTerm", termSelect.value);
  localStorage.setItem(
    "selectedresultAcademicSession",
    academicSessionSelect.value
  );
  localStorage.setItem("selectedresultsubject", subjectselect.value);
  classdata.selectedTerm = termSelect.value;
  classdata.selectedAcademicSession = academicSessionSelect.value;
  classdata.studentsubject =
    subjectselect.options[subjectselect.selectedIndex].value;
  readJsonFromFile();
}

// -----------------------------------------------------------
// Function to load saved values from localStorage
// -----------------------------------------------------------
function loadsavedSelection() {
  const savedTerm = localStorage.getItem("selectedresultTerm");
  const savedAcademicSession = localStorage.getItem(
    "selectedresultAcademicSession"
  );
  const savedsubject = localStorage.getItem("selectedresultsubject");

  if (savedTerm !== null) {
    termSelect.value = savedTerm;
    classdata.selectedTerm = termSelect.value;
  } else {
    classdata.selectedTerm = termSelect.value;
  }

  if (savedAcademicSession !== null) {
    academicSessionSelect.value = savedAcademicSession;
    classdata.selectedAcademicSession = academicSessionSelect.value;
  } else {
    classdata.selectedAcademicSession = academicSessionSelect.value;
  }

  if (savedsubject !== null) {
    subjectselect.value = savedsubject;
    classdata.studentsubject = subjectselect.value;
  } else {
    classdata.studentsubject = subjectselect.value;
  }

  readJsonFromFile();
}

// -----------------------------------------------------------
// Function to read JSON data from Server
// -----------------------------------------------------------
async function readJsonFromFile() {
  try {
    const url = "/Teachers_Portal/getstudentresults/";
    const jsonData = await getstudentdata(url, classdata);
    console.log(jsonData);
    const studentHandler = new StudentDataHandler(jsonData);
    const studentsWithCalculatedFields = studentHandler.getStudents();
    //   populaterowcheckbox(studentsWithCalculatedFields)
    studentResult = studentsWithCalculatedFields;
    updateResultBadge("update", studentsWithCalculatedFields[0]);
    populatetable(studentsWithCalculatedFields);
    const dataTable = new DataTable(inputStudentResultModal, inputform);
  } catch (error) {
    console.error("Error reading JSON file:", error);
  }
}

// -----------------------------------------------------------
// Function to populate the table with data
// -----------------------------------------------------------
function populatetable(tabledata) {
  const tbody = document.querySelector("#dataTable").lastElementChild;
  tbody.innerHTML = tabledata
    .map(
      (data, index) => `
        <tr data-rowindex='${index + 1}'>
            <td>${index + 1}</td>
            <td class="text-primary text-uppercase"><a class="inputdetailsformmodelbtn text-decoration-none" style="cursor:pointer">${
              data.Name
            }</a></td>
            <td>${data["CA"]}</td>
            <td>${data["Exam"]}</td> 
            <td>${data["Total"] || "-"}</td>
            <td>${data["Grade"] || "-"}</td>
            <td>${data["Position"] || "-"}</td>
            <td>${data["Remarks"] || "-"}</td>
        </tr>`
    )
    .join("");
}

// -----------------------------------------------------------
// Function to export Student Results to JSON
// -----------------------------------------------------------
function exportTableToJSON() {
  const url =
    state === "published"
      ? "/Teachers_Portal/unsubmitallstudentresult/"
      : "/Teachers_Portal/submitallstudentresult/";
  const datatosubmit = studentResult;
  classdata.studentsubject =
    subjectselect.options[subjectselect.selectedIndex].value;
  classdata.studentclass = classinput.value;
  (classdata.selectedTerm = termSelect.value),
    (classdata.selectedAcademicSession = academicSessionSelect.value),
    submitallstudentresult(url, datatosubmit, classdata, displayalert);
  updateResultBadge("setbadge", datatosubmit[0]);
}

// -----------------------------------------------------------
// Function to display alert messages
// -----------------------------------------------------------
function displayalert(type, message) {
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
                          <i class="fa-solid fa-circle-check h6 me-2"></i>
                          <div>
                             ${message}
                          </div>
                          `;
  alertcontainer.appendChild(alertdiv);

  setTimeout(() => {
    alertdiv.remove();
  }, 3000);
}

// ------------------------------------------------------------------------------------------------
// function to update the result badge
// ------------------------------------------------------------------------------------------------
function updateResultBadge(type, studentresult) {
  if (type === "setbadge") {
    studentresult.published = !studentresult.published;
  }
  state = studentresult.published ? "published" : "unpublished";
  const badge = document.querySelector("#resultbadge");
  studentresult.published
    ? badge.classList.replace("bg-secondary", "bg-success")
    : badge.classList.replace("bg-success", "bg-secondary");
  badge.innerHTML = studentresult.published
    ? `<i class="fa-solid fa-check-circle me-2"></i>
         Result Published`
    : `<i class="fa-solid fa-circle-plus me-2"></i>
         Result Not Published`;

  document.querySelectorAll(".publishbtn").forEach((btn) => {
    btn.innerHTML = studentresult.published
      ? `UnPublish Result <i class="fa-solid fa-right-from-bracket ms-2"></i>`
      : `Publish Result <i class='fa-solid fa-left-from-bracket ms-2'></i>`;
  });
}
