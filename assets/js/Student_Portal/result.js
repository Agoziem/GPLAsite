const result_btn = document.getElementById('result_btn');
const spinner = result_btn.querySelector('.spinner-border');
const labels = document.querySelector('#labels')
const data = document.querySelector('#data')
const modifiedlabelsList = labels.value.replace(/'/g, '"');
const modifieddataList = data.value.replace(/'/g, '"');
const Jsonlabellist = `${modifiedlabelsList}`
const Jsondatalist = `${modifieddataList}`


result_btn.addEventListener('click', () => {
    // Show spinner
    spinner.classList.remove('d-none');
    result_btn.disabled = true;
  
    // Call the function that generates the PDF
    myFunction()
      .then(() => {
        // PDF generation is finished, stop spinner
        spinner.classList.add('d-none');
        result_btn.disabled = false;
        // Add your code to start downloading the PDF here
      })
      .catch((error) => {
        // PDF generation encountered an error, display error message
        spinner.classList.add('d-none');
        result_btn.disabled = false;
        result_btn.innerHTML = 'Error: ' + error.message;
      });
  });

  function myFunction(e){
    var element = document.getElementById('container_result');
    var opt =
    {
        margin: 0,
        filename: 'GPLA Result' + '.pdf',
        image: { type: 'jpeg', quality: 1 },
        html2canvas: {
          scale: 5,
          useCORS: true,
          imageTimeout:0,
          allowTaint:false
        },
        jsPDF: { unit: 'px', format: 'a4', orientation: 'portrait' }
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


    const ctx = document.getElementById('mybarChart');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: JSON.parse(Jsonlabellist),
        datasets: [{
          label: 'Total Scores',
          data: JSON.parse(Jsondatalist),
          backgroundColor: ['#9c0101', 'black', '#d2cfcf'],
          borderWidth: 1
          }]
        },
      options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
      });

