import AnnualResulthandler from "./utils/AnnualResulthandler.js";
import AnnualStudentResultDatatable from "./datatable/AnnualResultDatatable.js";
import {
  getannualresultdata,
  submitallstudentresult,
} from "./utils/serveractions.js";

// ---------------------------------------------------
// DOM elements
// ---------------------------------------------------
const getstudentresultform = document.getElementById("getstudentresultform");
const subjectselect = getstudentresultform.querySelector("select");
const classinput = getstudentresultform.querySelector("#classinput");
const classsession = getstudentresultform.querySelector("#classsession");
const academicSessionSelect = document.getElementById("academicSessionSelect");
const alertcontainer1 = document.querySelector(".alertcontainer1"); // for small screen
const alertcontainer2 = document.querySelector(".alertcontainer2"); // for large screen

document.querySelectorAll(".publishbtn").forEach((btn) => {
  btn.addEventListener("click", exportTableToJSON);
});

// ---------------------------------------------------
// Global variables
// ---------------------------------------------------
let classdata = {
  studentclass: classinput.value,
};

let studentResult = [];
let state;

// ---------------------------------------------------
// Event listeners
// ---------------------------------------------------

// get student result
document.addEventListener("DOMContentLoaded", () => {
  getstudentresultform.addEventListener("submit", (e) => {
    e.preventDefault();
    saveformSelections();
  });
});

// load saved selection
document.addEventListener("DOMContentLoaded", () => {
  loadsavedSelection();
});

// ---------------------------------------------------
// Function to save selected values to localStorage
// ---------------------------------------------------
function saveformSelections() {
  localStorage.setItem(
    "selectedresultAcademicSession",
    academicSessionSelect.value
  );
  localStorage.setItem("selectedresultsubject", subjectselect.value);
  classdata.selectedAcademicSession = academicSessionSelect.value;
  classdata.studentsubject =
    subjectselect.options[subjectselect.selectedIndex].value;
  readJsonFromFile();
}

// -----------------------------------------------------
// Function to load saved values from localStorage
// ------------------------------------------------------
function loadsavedSelection() {
  const savedAcademicSession = localStorage.getItem(
    "selectedresultAcademicSession"
  );
  const savedsubject = localStorage.getItem("selectedresultsubject");

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

// -----------------------------------------------------
// Function to read JSON file and populate the table
// ------------------------------------------------------
async function readJsonFromFile() {
  try {
    let url;
    if (classsession.value === "Primary") {
      url = "/Teachers_Portal/primaryannualresultcomputation/";
    } else {
      url = "/Teachers_Portal/annualresultcomputation/";
    }
    const jsonData = await getannualresultdata(url,classdata);
    const studentHandler = new AnnualResulthandler(jsonData);
    const studentsWithCalculatedFields = studentHandler.getStudents();
    studentResult = studentsWithCalculatedFields;
    updateResultBadge("update", studentsWithCalculatedFields[0]);
    populatetable(studentsWithCalculatedFields);
    const dataTable = new AnnualStudentResultDatatable();
  } catch (error) {
    console.error("Error reading JSON file:", error);
  }
}

// -----------------------------------------------------
// Function to populate the table with data
// ------------------------------------------------------
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
            <td>${data["terms"]["1st Term"] || "-"}</td>
            <td>${data["terms"]["2nd Term"] || "-"}</td>
            <td>${data["terms"]["3rd Term"] || "-"}</td>
            <td>${data["Total"] || "-"}</td>
            <td>${data["Average"] || "-"}</td>
            <td>${data["Grade"] || "-"}</td>
            <td>${data["Position"] || "-"}</td>
            <td>${data["Remarks"] || "-"}</td>
         
        </tr>`
    )
    .join("");
}

// -----------------------------------------------------
// Function to export table data to JSON
// ------------------------------------------------------
function exportTableToJSON() {
  const url =
    state === "published"
      ? "/Teachers_Portal/unpublishannualresults/"
      : "/Teachers_Portal/publishannualresults/";
  const datatosubmit = studentResult;
  classdata.studentsubject =
    subjectselect.options[subjectselect.selectedIndex].value;
  classdata.studentclass = classinput.value;
  classdata.selectedAcademicSession = academicSessionSelect.value;
  submitallstudentresult(url, datatosubmit, classdata, displayalert);
  updateResultBadge("setbadge", datatosubmit[0]);
}

// -----------------------------------------------------
// Function to display alert messages
// ------------------------------------------------------
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
  // check for Screen Size and append alert message to the appropriate container
  if (window.innerWidth < 768) {
    alertcontainer1.appendChild(alertdiv);
  } else {
    alertcontainer2.appendChild(alertdiv);
  }
  setTimeout(() => {
    alertdiv.remove();
  }, 5000);
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
