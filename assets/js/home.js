
 mapboxgl.accessToken = 'pk.eyJ1Ijoib2tmcyIsImEiOiJjbDFodTNjMG8wNnh6M2tycHN0ZDhzamYzIn0.H1VgtMiBAjkMEe7GXREzvA';
 var map = new mapboxgl.Map({
   container: 'map',
   style: 'mapbox://styles/mapbox/streets-v11',
   center: [6.800465, 6.124938],
   zoom: 12,
 });



const contactForm = document.querySelector('#contact-form');
const btn = contactForm.querySelector('button');
contactForm .addEventListener('submit', submitcontactformdata)

// Submit Form Data
async function submitcontactformdata(e) {
  e.preventDefault();
  const formData = new FormData(contactForm);
  const userformdata = {
    'name': formData.get('name'),
    'email': formData.get('email'),
    'message': formData.get('message'),
  }
  try {
    const url = '/submit_contact_form/'
    const data = await postData(userformdata,url);
    btn.innerHTML = 'Send Message';
    const successAlert = document.querySelector('.alert-success');
    successAlert.style.display = 'flex';
    successAlert.innerHTML=`<div>
                            ${data}
                        </div>`
    setTimeout(function() {
      successAlert.style.display = 'none';
    }, 3000);
    contactForm.reset();

  } catch (error) {
    btn.innerHTML = 'Send Message';
    console.log(error);
    const errorAlert = document.querySelector('.alert-danger');
    errorAlert.style.display = 'flex';
    errorAlert.innerHTML=`<div>
                            ${error}
                        </div>`
    setTimeout(function() {
      errorAlert.style.display = 'none';
    }, 3000);
    contactForm.reset();
  }
  

}

// Post the Data to backend
async function postData(userformdata,url) {
  btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> submitting...';
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({ 'userformdata': userformdata })
  })
  if (res.status !== 200) {
    throw new Error('Oops Something went wrong');
  }
  const data = await res.json();
  return data;
        
}
  

  

// const notice = document.querySelector('.notice');
// const closeBtn = notice.querySelector('.close-btn');

// closeBtn.addEventListener('click', () => {
//   notice.style.display = 'none';
// });