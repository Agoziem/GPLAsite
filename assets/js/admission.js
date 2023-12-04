// const form = document.querySelector("form"),
//         nextBtn = form.querySelector(".nextBtn"),
//         backBtn = form.querySelector(".backBtn"),
//         allInput = form.querySelectorAll(".first input");


// nextBtn.addEventListener("click", ()=> {
//     allInput.forEach(input => {
//         if(input.value != ""){
//             form.classList.add('secActive');
//         }else{
//             form.classList.remove('secActive');
//         }
//     })
// })

// backBtn.addEventListener("click", () => form.classList.remove('secActive'));

const details_btn = document.getElementById('details_btn');
const spinner = details_btn.querySelector('.spinner-border');

details_btn.addEventListener('click', () => {
    // Show spinner
    spinner.classList.remove('d-none');
    details_btn.disabled = true;
  
    // Call the function that generates the PDF
    myFunction()
      .then(() => {
        // PDF generation is finished, stop spinner
        spinner.classList.add('d-none');
        details_btn.disabled = false;
        // Add your code to start downloading the PDF here
      })
      .catch((error) => {
        // PDF generation encountered an error, display error message
        spinner.classList.add('d-none');
        details_btn.disabled = false;
        details_btn.innerHTML = 'Error: ' + error.message;
      });
  });

  function myFunction(e){
    var element = document.getElementById('container_details');
    var opt =
    {
        margin: 0.5,
        filename: 'Entrance Exam' + '.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 4 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'Portrait' }
    };
    // New Promise-based usage:
    return new Promise((resolve, reject) => {
        html2pdf().set(opt).from(element).save()
        .then(() => {
            // PDF generation is complete, resolve the promise
            resolve();
          })
          .catch((error) => {
            // PDF generation encountered an error, reject the promise with the error
            reject(error);
          });
      });
}