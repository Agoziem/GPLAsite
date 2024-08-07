// --------------------------------------------------------------
// imports
// --------------------------------------------------------------
import { getClassPublishedResults } from "./serveractions.js";

// --------------------------------------------------------------
// UI Elements for Results
// --------------------------------------------------------------
const selectedclass = document.getElementById("school_classes");
const studentclassholder = document.getElementById("studentclassholder");
const selctedstudentclass =
  selectedclass.options[selectedclass.selectedIndex].value;
studentclassholder.innerText = selctedstudentclass;
const selectedsession = document.getElementById("session");
const selectedterm = document.getElementById("term");

const resultcredentialform = document.getElementById("resultcredentialform");
const subjectpublished = document.getElementById("subjectpublished");
const classresultpublishedbadge = document.getElementById(
  "classresultpublishedbadge"
);
const Publishedcounter = document.getElementById("Publishedcounter");
// ---------------------------------------------------------------------------------------------
// initails states
// ---------------------------------------------------------------------------------------------
let resultcredentials = {
  classname: "",
  session: "",
  term: "",
};

let Classsession;

// --------------------------------------------------------------
// Event Listeners ///////////////////////////////////////
// --------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  loadresultcredentials();
  selectedclass.addEventListener("change", (e) => {
    studentclassholder.innerText = e.target.value;
    const selectedOption = e.target.options[e.target.selectedIndex];
    Classsession = selectedOption.getAttribute("name");
    setresultcredentials(e);
  });
  selectedsession.addEventListener("change", (e) => {
    setresultcredentials(e);
  });
  selectedterm.addEventListener("change", (e) => {
    setresultcredentials(e);
  });

  let url;
  if (Classsession === "Secondary") {
    url = "/Teachers_Portal/getclasspublishedResults/";
  } else {
    url = "/Teachers_Portal/getprimaryclasspublishedResults/";
  }
  resultcredentialform.addEventListener("submit", (e) => {
    e.preventDefault();
    getClassPublishedResults(
      url,
      resultcredentials,
      displayResultPublishedbadge,
      displaypublishedResult
    );
  });
});

// ---------------------------------------------------------------------------------------------
// load result credentials from Local Storage if its there or set it to the initial state
// ---------------------------------------------------------------------------------------------
const loadresultcredentials = () => {
  let url;
  if (localStorage.getItem("resultcredentials")) {
    resultcredentials = JSON.parse(localStorage.getItem("resultcredentials"));
    Classsession =
      selectedclass.options[selectedclass.selectedIndex].getAttribute("name");
    selectedclass.value = resultcredentials.classname;
    studentclassholder.innerText = selectedclass.value;
    selectedsession.value = resultcredentials.session;
    selectedterm.value = resultcredentials.term;
    if (Classsession === "Secondary") {
      url = "/Teachers_Portal/getclasspublishedResults/";
    } else {
      url = "/Teachers_Portal/getprimaryclasspublishedResults/";
    }
    resultcredentials.classname !== "" &&
      resultcredentials.session !== "" &&
      resultcredentials.term !== "" &&
      getClassPublishedResults(
        url,
        resultcredentials,
        displayResultPublishedbadge,
        displaypublishedResult
      );
  } else {
    resultcredentials.classname =
      selectedclass.options[selectedclass.selectedIndex].value;
    Classsession =
      selectedclass.options[selectedclass.selectedIndex].getAttribute("name");
    studentclassholder.innerText = resultcredentials.classname;
    resultcredentials.session =
      selectedsession.options[selectedsession.selectedIndex].value;
    resultcredentials.term =
      selectedterm.options[selectedterm.selectedIndex].value;
    if (Classsession === "Secondary") {
      url = "/Teachers_Portal/getclasspublishedResults/";
    } else {
      url = "/Teachers_Portal/getprimaryclasspublishedResults/";
    }
    resultcredentials.classname !== "" &&
      resultcredentials.session !== "" &&
      resultcredentials.term !== "" &&
      getClassPublishedResults(
        url,
        resultcredentials,
        displayResultPublishedbadge,
        displaypublishedResult
      );
  }
};

// ---------------------------------------------------------------------------------------------
// function to set the result credentials
// ---------------------------------------------------------------------------------------------
const setresultcredentials = (e) => {
  resultcredentials = {
    ...resultcredentials,
    [e.target.name]: e.target.value,
  };
  localStorage.setItem("resultcredentials", JSON.stringify(resultcredentials));
};

// --------------------------------------
// function to display the result published badge
// --------------------------------------
function displayResultPublishedbadge(data) {
  classresultpublishedbadge.innerHTML = data.published
    ? `<i class="fa-solid fa-check-circle me-2"></i>
       Result Published`
    : `<i class="fa-solid fa-circle-plus me-2"></i>
       Result Not Published`;
  data.published
    ? classresultpublishedbadge.classList.replace("bg-secondary", "bg-success")
    : classresultpublishedbadge.classList.replace("bg-success", "bg-secondary");
}

// --------------------------------------
// function to display the published result
// --------------------------------------
function displaypublishedResult(data) {
  if (data.subjects && data.subjects.length > 0) {
    subjectpublished.innerHTML = data.subjects
      .map((subject, index) => {
        if (subject.published) {
          return `<li class="list-group-item d-flex justify-content-between align-items-center fw-bold text-success">
                    <div>
                        <span class="me-2">${index + 1}.</i>
                        ${subject.subject}
                    </div>
                    
                  <i class="fa-solid fa-check-double"></i>
                </li>`;
        } else {
          return `<li class="list-group-item d-flex justify-content-between align-items-center fw-bold text-danger">
                    <div>
                        <span class="me-2">${index + 1}.</i>
                        ${subject.subject}
                    </div>
                    <i class="fa-solid fa-xmark"></i>
                  </li>`;
        }
      })
      .join("");
    const totalresultspublished = data.subjects.filter(
      (subject) => subject.published
    ).length;
    const totalresults = data.subjects.length;
    Publishedcounter.innerHTML =
      totalresultspublished === totalresults
        ? `<span class="text-success fw-bold ">Completed</span>`
        : `
      <span class="fw-bold text-success ">${totalresultspublished}</span> out of <span class="fw-bold text-success">${totalresults}</span> Subject Teachers have Published
        `;
  } else {
    subjectpublished.innerHTML = `<li class="list-group-item d-flex justify-content-between align-items-center fw-bold text-danger">
                    <span>
                        <i class="fa-solid fa-xmark me-2"></i>
                        No Result Published Yet for ${resultcredentials.classname} in ${resultcredentials.term} ${resultcredentials.session}
                    </span>
                  </li>`;
    Publishedcounter.innerHTML = "";
  }
}
