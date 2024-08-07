import { showSpinner, hideSpinner } from "../utils/displayspinner.js";

// --------------------------------------------
// function for admin get Class Published Results
// --------------------------------------------
const getClassPublishedResults = async (
  url,
  resultcredentials,
  displayResultPublishedbadge,
  displaypublishedResult
) => {
  showSpinner("verifyspinner", "verifyspinnerbtnmessage", "Verifying...");
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(resultcredentials),
    });
    const data = await response.json();
    if (response.ok) {
      displayResultPublishedbadge(data);
      displaypublishedResult(data);
    } else {
      throw new Error(data.error);
    }
  } catch (error) {
    console.log(error);
  }
  hideSpinner("verifyspinner", "verifyspinnerbtnmessage", "Verify Submissions");
};

// ---------------------------------------------------------------------------------------------
//  function for admin get Class Annual Published Results
// ---------------------------------------------------------------------------------------------
const getClassannualPublishedResults = async (
  resultcredentials,
  displayResultPublishedbadge,
  displaypublishedResult
) => {
  // showSpinner("verifyannualspinner", "verifyannualspinnerbtnmessage", "Verifying...");
  try {
    const response = await fetch("/Teachers_Portal/getclassannualpublishedResults/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify(resultcredentials),
    });
    const data = await response.json();
    if (response.ok) {
      displayResultPublishedbadge(data);
      displaypublishedResult(data);
    } else {
      throw new Error(data.error);
    }
  } catch (error) {
    console.log(error);
  }
  // hideSpinner("verifyannualspinner", "verifyannualspinnerbtnmessage", "Verify Submissions");
};

export { getClassPublishedResults, getClassannualPublishedResults };
