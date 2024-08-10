import AnnualClassResultHandler from "./utils/AnnualClassResulthandler.js";
import AnnualClassResultDataTable from "./datatable/AnnualClassResultDatatable.js";
import {
  getannualclassresult,
  publishstudentresult,
} from "./utils/serveractions.js";

// ---------------------------------------------------
// DOM elements
// ---------------------------------------------------
const classinput = document.querySelector(".classinput");
const subjectlistinput = document.querySelector(".subjectlist");
const subjectlist = subjectlistinput.value;
const modifiedList = subjectlist.replace(/'/g, '"');
let jsonstring = `${modifiedList}`;
let mainsubjectlist = JSON.parse(jsonstring);
const alertcontainer = document.querySelector(".alertcontainer");
const academicSessionSelect = document.getElementById("academicSessionSelect");
const publishButton = document.getElementById("publishbtn");

// ---------------------------------------------------
// Global variables
// ---------------------------------------------------

academicSessionSelect.addEventListener("change", function () {
  saveSelection();
});

window.addEventListener("DOMContentLoaded", () => {
  loadSelection();
});

publishButton.addEventListener("click", () => {
  publishResult();
});

// ---------------------------------------------------
// Event listener for the form submission
// ---------------------------------------------------

let ClassResult = [];

let classdata = {
  studentclass: classinput.value,
};

let state;

// ---------------------------------------------------
// Function to save selected values to localStorage
// ---------------------------------------------------
function saveSelection() {
  localStorage.setItem("selectedAcademicSession", academicSessionSelect.value);
  classdata.selectedAcademicSession = academicSessionSelect.value;
  readJsonFromFile();
}

// ---------------------------------------------------
// Function to load saved values from localStorage
// ---------------------------------------------------
function loadSelection() {
  const savedAcademicSession = localStorage.getItem("selectedAcademicSession");
  if (savedAcademicSession !== null) {
    academicSessionSelect.value = savedAcademicSession;
    classdata.selectedAcademicSession = academicSessionSelect.value;
  } else {
    classdata.selectedAcademicSession = academicSessionSelect.value;
  }
  readJsonFromFile();
}

// ---------------------------------------------------
// function to get Student Result
// ---------------------------------------------------
async function readJsonFromFile() {
  try {
    const jsonData = await getannualclassresult(classdata);
    const studentHandler = new AnnualClassResultHandler(jsonData);
    const studentsWithCalculatedFields = studentHandler.getStudents();
    ClassResult = studentsWithCalculatedFields;
    updateResultBadge("update", studentsWithCalculatedFields[0]);
    showStudentSubjectResults(studentsWithCalculatedFields[0]);
    populatetable(studentsWithCalculatedFields);
    const dataTable = new AnnualClassResultDataTable();
  } catch (error) {
    console.error("Error reading JSON file:", error);
  }
}

// ---------------------------------------------------
// function to Populate the Table
// ---------------------------------------------------
function populatetable(tabledata) {
  const tbody = document.querySelector("#dataTable").lastElementChild;
  tbody.innerHTML = tabledata
    .map(
      (data, index) =>
        `
        <tr>
            <td>${index + 1}</td>
            <td class="text-primary">${data.Name}</td>
            ${data.subjects.map(
              (subject) =>
                `<td>${subject.Average !== "-" ? subject.Average : ""}</td>`
            )}
            <td>${data.Total}</td>
            <td>${data.Average}</td>
            <td>${data.Grade}</td>
            <td>${data.Position}</td>
            <td>${data.Remarks}</td>
            <td>${data.Verdict}</td>
        </tr>`
    )
    .join("");
}

// ------------------------------------------------------------------
// function to publish Result /////////////////////////////////////
// ------------------------------------------------------------------
function publishResult() {
  const url =
    state === "published"
      ? "/Teachers_Portal/unpublishannualclassresult/"
      : "/Teachers_Portal/publishannualclassresult/";

  if (ClassResult.length === 0) {
    displayalert("alert-warning", "No result to publish");
    return;
  }
  const data = ClassResult;
  (classdata.studentclass = classinput.value),
    (classdata.selectedAcademicSession = academicSessionSelect.value),
    publishstudentresult(url, data, classdata, displayalert);
  updateResultBadge("setbadge", data[0]);
}

// ----------------------------------------------------------------------------------
// functions to disable the button when the Term and Academic Session have not been
// ----------------------------------------------------------------------------------
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
                        <i class="fa-solid fa-circle-check me-2"></i>
                        <div>
                           ${message}
                        </div>
                        `;
  alertcontainer.appendChild(alertdiv);

  setTimeout(() => {
    alertdiv.remove();
  }, 3000);
}

// -----------------------------------------------------------------------
// function to update the result badge and the button test //////////////
// -----------------------------------------------------------------------
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
        <span> Result Published </span>`
    : `<i class="fa-solid fa-circle-xmark me-2"></i>
        <span> Result Not Published </span>`;
  publishButton.innerHTML = studentresult.published
    ? "Unpublish Result"
    : "Publish Result";
}

// -----------------------------------------------------------------------
// function to show the Student Subject Results Published
// -----------------------------------------------------------------------
const showStudentSubjectResults = (student) => {
  const subjectsresultlist = document.querySelector("#resultspublished");
  const studentSubjectResultData = student.subjects.map(
    (subject, index) => {
      if (subject.published) {
        return `<li
            class="list-group-item d-flex justify-content-between align-items-center text-success fw-bold"
          >
          <div>
            <span class="me-2">${index + 1}.</i>
            ${subject.subject_name}
          </div>
            <i class="fa-solid fa-check me-3 fw-bold "></i>
          </li>`;
      } else {
        return `<li
            class="list-group-item d-flex justify-content-between align-items-center text-danger fw-bold"
          >
             <div>
                <span class="me-2">${index + 1}.</i>
                ${subject.subject_name}
              </div>
            <i class="fa-solid fa-xmark me-3 fw-bold "></i>
          </li>`;
      }
    }
  );
  subjectsresultlist.innerHTML = studentSubjectResultData.join("");
};
