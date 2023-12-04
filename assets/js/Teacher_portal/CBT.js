// The Question Class
class Question {
    constructor(questionText, questionMark, required, questionid) {
        this.id = questionid || Math.random().toString(16).slice(2);
        this.questionText = questionText || "None";
        this.questionMark = questionMark || 0;
        this.questionrequired = required;
        this.answers = [];
    }

    updateQuestionText(newText) {
        this.questionText = newText;
    }

    // CRUD for Answers
    addAnswer(answer) {
        this.answers.push(answer);
    }

    deleteAnswer(answer) {
        const index = this.answers.indexOf(answer);
        if (index !== -1) {
            this.answers.splice(index, 1);
        }
    }

}

// The Answer Class
class Answer {
    constructor(answerText, isCorrect, answerid) {
        this.id = answerid || Math.random().toString(16).slice(2);
        this.answerText = answerText || "None";
        this.isCorrect = isCorrect;
    }

    updateAnswerText(newText) {
        this.answerText = newText;
    }

}



// The Question Subject Class
class QuestionSet {
    constructor() {
        this.questions = this.loadQuestions();
    }



    // CREATE ( POST to the database) and (display to the UI)
    addQuestion(question) {
        storage.saveQuestions(question)
        this.__displayQuestions(question)
    }

    updateQuestion(question) {
        storage.updatequestion(question)
        this.__displayQuestions(question)
    }



    // DELETE ( Delete to the database) and (remove from the UI)
    removequestion(questionid) {
        storage.removeQuestion(questionid)
    }

    removeallquestions() {
        this.__removeQuestions();
        storage.clearAllQuestions()
    }



    async loadQuestions() {
        try {
            const questions = await storage.getQuestions();
            questions.forEach((question) => this.__displayQuestions(question))
        } catch (error) {
            console.error('Error occurred:', error);
            throw error;
        }
    }



    // Private methods
    __displayQuestions(question) {
        const MainDiv = document.querySelector('#QuestionContainer')
        const QuestionCard = document.createElement('div');
        QuestionCard.classList.add('QuestionCard', 'mb-3');
        QuestionCard.setAttribute('data-question', `${question.id}`)
        QuestionCard.innerHTML = `
                            <div class="d-flex justify-content-between mb-2">
                                <div class='question-text'> ${question.questionText}</div>
                            <div>
                                <div class='question-mark ms-4 fs-6'> ${question.questionMark == 1 ? question.questionMark + 'Mk' : question.questionMark + 'Mks'}</div>
                                </div>
                            </div>
                            <div class='question-answers'>
                                ${question.answers.map((answer, index) => {
                                    const isLastAnswer = index === question.answers.length - 1;
                                    const requiredAttribute = isLastAnswer ? 'required' : '';
                                    const invalidFeedback = isLastAnswer
                                            ? `<div class="invalid-feedback">You must select one of the options</div>`
                                            : '';

                                        return `<div class="form-check">
                                                <input class="form-check-input" type="radio" name="flexRadioDefault${question.id}" id="flexRadioDefault${answer.id}" ${requiredAttribute}>
                                                <label class="form-check-label answerlabel" data-answer="${answer.id}" for="flexRadioDefault${answer.id}">
                                                    ${answer.answerText}
                                                </label>
                                                ${invalidFeedback}
                                            </div>`;
                                }).join('')}
                            </div>

                            <div class="QuestionCardutilities d-flex justify-content-between align-items-center mt-3">
                                <div class="form-check form-switch me-3">
                                    <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" ${question.questionrequired ? 'checked' : ''}>
                                    <label class="form-check-label" for="flexSwitchCheckDefault">Required</label>
                                </div>
                                <div>
                                    <i class=" fa-solid fa-pen-to-square mx-2 h5 text-success editQuestionCard" style="cursor:pointer"></i>
                                    <i class="fa-solid fa-trash text-danger h5 deleteQuestionCard" style="cursor:pointer"></i>
                                </div>
                            </div>

                        `
        MainDiv.appendChild(QuestionCard)
        checkUi();

    }

    __removeQuestions() {
        const MainDiv = document.querySelector('#QuestionContainer')
        MainDiv.innerHTML = '';
    }
}

class MainQuestions {
    constructor(option) {
        this.questionsetid = option.questionsetid;
        this.subject = option.subject || '';
        this.questions = [];
        this.teacher = option.teacher || '';
        this.examTime = option.examTime || 40;
        this.Class = option.Class || [];
    }

    addQuestion(question) {
        this.questions.push(question);
    }
}

const questionsetid = document.getElementById('questionsetid').value
const subject = document.getElementById('subject').value
const teacher = document.getElementById('teacher').value
const examTime = document.getElementById('time').value
const selectElement = document.getElementById('test_classes');
const Class = [...selectElement.selectedOptions].map(option => option.value);
let isEditMode = false;

const option = {
    questionsetid: +questionsetid,
    subject,
    teacher,
    Class,
    examTime: +examTime
}


const questionsform = document.querySelector('#questionSubmitform')
const submitquestionbtn = document.querySelector('#mainsubmitQuestionbtn')
const deleteQuestionbtnModal = document.querySelector("#deleteQuestionbtnModal")
const filtercontainer = document.querySelector('.filter')
const submitQuestionModalbtn = document.querySelector('#submitQuestionbtn')
const addquestionform = document.querySelector('#addtestquestionform')
const addquestionModal = document.querySelector('#addquestionmodal')
const deletequestionModal = document.querySelector('#deletequestionModal')
const alertcontainer = document.querySelector('.alertcontainer')
const submitalertcontainer = document.querySelector('.submitalertcontainer')
const noquestion = document.querySelector('.noquestion')

function displayalert(type, message) {
    const alertdiv = document.createElement('div');
    alertdiv.classList.add('alert', `${type}`, 'd-flex', 'align-items-center', 'mt-3');
    alertdiv.setAttribute('role', 'alert');
    alertdiv.innerHTML = `
                        <i class="fa-solid fa-circle-check h6 me-2"></i>
                        <div>
                           ${message}
                        </div>
                        `
    alertcontainer.appendChild(alertdiv)

    setTimeout(() => {
        alertdiv.remove();
    }, 3000);

}

function displaysubmitalert(type, message) {
    const alertdiv = document.createElement('div');
    alertdiv.classList.add('alert', `${type}`, 'd-flex', 'align-items-center', 'mt-3');
    alertdiv.setAttribute('role', 'alert');
    alertdiv.innerHTML = `
                        <i class="fa-solid fa-circle-check h6 me-2"></i>
                        <div>
                           ${message}
                        </div>
                        `
    submitalertcontainer.appendChild(alertdiv)

    setTimeout(() => {
        alertdiv.remove();
    }, 3000);

}

addquestionModal.addEventListener('hidden.bs.modal', function () {
    window.ckeditorEditor.setData('');
    const questionanswers = addquestionform.querySelectorAll('#questionanswer')
    questionanswers.forEach((answer) => {
        answer.value = '';
    })
});

// Check the State of the UI and perform an Action 
function checkUi() {
    const questioncards = document.querySelectorAll('.QuestionCard');
    const editQuestionCardBtns = document.querySelectorAll('.editQuestionCard');
    const deleteQuestionCardBtns = document.querySelectorAll('.deleteQuestionCard');
    editQuestionCardBtns.forEach((editQuestionCardbtn) => editQuestionCardbtn.addEventListener('click', setupeditform))
    addquestionform.classList.remove('was-validated');
    deleteQuestionCardBtns.forEach((deleteQuestionCardBtn) => deleteQuestionCardBtn.addEventListener('click', setupdeleteModal))

    if (!isEditMode) {
        questioncards.forEach((questioncard) => {
            questioncard.classList.remove('is-edit');
        });
        const formbtn = addquestionform.querySelector('#addtestquestionsbtn');
        formbtn.classList.add('addquestionstate')
        formbtn.classList.remove('btnineditstate')

    }

    if (questioncards.length === 0) {
        deleteQuestionbtnModal.style.display = 'none';
        filtercontainer.style.display = 'none';
        submitQuestionModalbtn.style.display = 'none';
        noquestion.style.display = 'block';
    } else {
        noquestion.style.display = 'none';
        deleteQuestionbtnModal.style.display = 'block';
        filtercontainer.style.display = 'block';
        submitQuestionModalbtn.style.display = 'block';
        
    }
}

function setupdeleteModal(e) {
    isEditMode = true
    document.querySelectorAll('.QuestionCard').forEach((card) => {
        card.classList.remove('is-edit')
    })
    const questionCard = e.target.closest('.QuestionCard')
    questionCard.classList.add('is-edit')
    $(deletequestionModal).modal('show');
}



// set up form for editing
function setupeditform(e) {
    const editor = window.ckeditorEditor;
    

    // Set the content of the CKEditor instance
    isEditMode = true
    document.querySelectorAll('.editQuestionCard').forEach((card) => {
        card.classList.remove('is-edit')
    })
    const questionCard = e.target.closest('.QuestionCard')
    questionCard.classList.add('is-edit')

    const questiontextinput = addquestionform.querySelector('#questiontextinput');
    questiontextinput.value =''
    const newContent = questionCard.querySelector('.question-text').innerHTML;
    editor.setData(newContent);
    const questionmark = addquestionform.querySelector('#questionmark');
    questionmark.value = questionCard.querySelector('.question-mark').innerText[0];

    const formanswercontainer = addquestionform.querySelector('.answersinput');
    formanswercontainer.innerHTML = ''
    const answers = questionCard.querySelectorAll('.answerlabel')
    answers.forEach((answer) => {
        const answergroupdiv = document.createElement('div');
        answergroupdiv.classList.add('answergroup', 'd-flex', 'align-items-center', 'mb-3', 'pe-3')
        answergroupdiv.innerHTML = `
                        <input type="text" class="form-control" id="questionanswer" placeholder="add your answer text" value="${answer.innerText}" required>
                        <i class="fa-solid fa-xmark pt-2 h4 ms-3 text-danger"></i>`
        formanswercontainer.appendChild(answergroupdiv)
    })
    if (isEditMode) {
        const formbtn = addquestionform.querySelector('#addtestquestionsbtn');
        formbtn.classList.remove('addquestionstate')
        formbtn.classList.add('btnineditstate')
    }
    $(addquestionModal).modal('show');

}



class App {
    constructor() {
        this.questionCard = new QuestionSet({});
        this.questionCard.questions;
        document.querySelector("#filter").addEventListener('input', this.filterItems.bind(this));
        document.querySelector('#deleteallquestionbtn').addEventListener('click', this.deleteallquestions.bind(this))
        questionsform.addEventListener('submit', this.preventsubmit.bind(this))
        submitquestionbtn.addEventListener('click', this.submittestquestions.bind(this))
        addquestionModal.addEventListener('click', this.processmodal.bind(this))
        deletequestionModal.addEventListener('click', this.processdeletemodal.bind(this))
        // document.querySelector('#updatetestquestionform').addEventListener('submit', this.updatequestion(e))
        checkUi();
    }
    processmodal(e) {
        if (e.target.classList.contains('addanswersinput')) {
            e.preventDefault()
            const answercontainer = e.target.parentElement.previousElementSibling
            const answerDiv = document.createElement('div')
            answerDiv.classList.add('answergroup', 'd-flex', 'align-items-center', 'mb-3', 'pe-3')
            answerDiv.innerHTML = `
                            <div>
                                <input type="text" class="form-control" id="questionanswer" placeholder="add your answer text" required>
                                <div class="invalid-feedback">
                                    Please input an answer
                                </div>
                            </div>
                            <i class="fa-solid fa-xmark pt-2 h4 ms-3 text-danger"></i>`
            answercontainer.appendChild(answerDiv)
        }

        if (e.target.classList.contains('addquestionstate')) {
            e.preventDefault()
            const form = e.target.closest('#addtestquestionform')
            const ckEditoraddTextarea = form.querySelector('#questiontextinput');
            
            if (form.checkValidity() === false) {
                // If the form is not valid, show Bootstrap's custom validation styles
                form.classList.add('was-validated');
            } else {
                form.classList.remove('was-validated');
                ckEditoraddTextarea.setAttribute('data-validation', 'false');
                this.addquestions(form)

                setTimeout(() => {
                    ckEditoraddTextarea.removeAttribute('data-validation');
                }, 1000);
            }
        }

        if (e.target.classList.contains('btnineditstate')) {
            e.preventDefault();
            const updateform = e.target.closest('#addtestquestionform');
            const ckEditorTextarea = updateform.querySelector('#questiontextinput'); // Replace with your CKEditor textarea class or ID

            if (updateform.checkValidity() === false) {
                updateform.classList.add('was-validated');
            } else {
                // Temporarily disable validation on CKEditor textarea
                updateform.classList.remove('was-validated');
                ckEditorTextarea.setAttribute('data-validation', 'false');
                const questionCard = document.querySelector('.QuestionCard.is-edit');
                const questionid = questionCard.getAttribute('data-question');
                this.updatequestion(updateform, questionCard, questionid);

                // Re-enable the validation after submission
                setTimeout(() => {
                    ckEditorTextarea.removeAttribute('data-validation');
                }, 1000); // Change this delay as needed to accommodate the form submission time
            }
        }

        if (e.target.classList.contains('fa-xmark')) {
            e.target.parentElement.remove();
        }

    }
    processdeletemodal(e) {
        if (e.target.id == 'deletequestionbtn') {
            this.removeQuestion(e)
        }
    }
    // process Submitting for the Questions
    preventsubmit(e) {
        e.preventDefault();

        if (questionsform.checkValidity() === false) {
            // If the form is not valid, show Bootstrap's custom validation styles
            questionsform.classList.add('was-validated');
        } else {
            questionsform.classList.remove('was-validated');
            const modal = document.querySelector('#submitquestionsmodal')
            $(modal).modal('show');
        }

    }

    submittestquestions(e) {
        const modal = e.target.closest('.modal')
        $(modal).modal('hide');
        this.submitTestGroup();
    }

    submitTestGroup() {
        const questionset = new MainQuestions(option);

        // get the questions and append to the questionsets
        const questioncards = document.querySelectorAll('.QuestionCard');
        questioncards.forEach((question) => {
            const questionMark = question.querySelector('.question-mark').innerText[0];
            const questionText = question.querySelector('.question-text').innerText;
            const questionid = question.getAttribute('data-question')
            const switchElement = question.querySelector('.form-check-input[role="switch"]');
            const required = switchElement.checked;
            const requiredBoolean = required ? true : false;
            const testquestion = new Question(questionText, +questionMark, requiredBoolean, questionid)
            questionset.addQuestion(testquestion)

            // get the Answers and append to the questions
            const checkedRadioButtons = question.querySelectorAll('input[type="radio"]');
            checkedRadioButtons.forEach((radio) => {
                const answertext = radio.nextElementSibling.innerText;
                const answerid = radio.nextElementSibling.getAttribute('data-answer');
                const isRadioChecked = radio.checked;
                const answervalueBoolean = isRadioChecked ? true : false;
                const testanswer = new Answer(answertext, answervalueBoolean, answerid);
                testquestion.addAnswer(testanswer);
            });

        })

        storage.submitQuestionstoServer(questionset);
    }



    addquestions(form) {
        const addquestionform = form
        const editorContent = window.ckeditorEditor.getData();
        const questioninput = addquestionform.querySelector('#questiontextinput');
        questioninput.value = editorContent
        let questioninputtext = questioninput.value
        const questionmkinput = addquestionform.querySelector('#questionmark');
        const questionmk = questionmkinput.value
        const question = new Question(questioninputtext, questionmk,true);
        questionmkinput.value = '2';
        const questionanswers = addquestionform.querySelectorAll('#questionanswer')
        questionanswers.forEach((answer) => {
            let answerText = answer.value;
            const answerobject = new Answer(answerText, false)
            answer.value = '';
            question.addAnswer(answerobject)
        })
        this.questionCard.addQuestion(question)
        const modal = addquestionform.closest('.modal')
        $(modal).modal('hide');
    }

    updatequestion(form, questioncard, questionid) {
        // remove it from the DOM and Storage
        questioncard.remove()

        // add it back to the DOM and Storage
        const updatetestquestionform = form
        const editorContent = window.ckeditorEditor.getData();
        const questioninput = updatetestquestionform.querySelector('#questiontextinput');
        questioninput.value = editorContent
        let questioninputtext = questioninput.value
        const questionmkinput = updatetestquestionform.querySelector('#questionmark');
        const questionmk = questionmkinput.value
        const question = new Question(questioninputtext, questionmk, true, questionid);
        questioninput.value = '';
        questionmkinput.value = '2';
        const questionanswers = updatetestquestionform.querySelectorAll('#questionanswer')
        questionanswers.forEach((answer) => {
            let answerText = answer.value;
            const answerobject = new Answer(answerText, false)
            answer.value = '';
            question.addAnswer(answerobject)
        })
        this.questionCard.updateQuestion(question)
        const modal = updatetestquestionform.closest('.modal')
        $(modal).modal('hide');
        isEditMode = false;
        checkUi();
    }

   

    removeQuestion(e) {
        const questioncard = document.querySelector('.QuestionCard.is-edit')
        const questionid = questioncard.getAttribute('data-question');
        questioncard.remove()
        this.questionCard.removequestion(questionid)
        $(deletequestionModal).modal('hide');
        isEditMode = false
        checkUi();
    }

    deleteallquestions(e) {
        this.questionCard.removeallquestions()
        const modal = e.target.closest('.modal')
        $(modal).modal('hide');
        checkUi();
    }


    filterItems(e) {
        const items = document.querySelectorAll('.QuestionCard');
        const text = e.target.value.toLowerCase();
        items.forEach((item) => {
            const itemName = item.firstElementChild.firstElementChild.textContent.toLowerCase();
            if (itemName.indexOf(text) != -1) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    }


}

class storage {
    static async getQuestions() {
        try {
            let questions = await storage.getQuestionsAndAnswers(+questionsetid);
            return questions;
        } catch (error) {
            console.error('Error:', error);
        }
    }

    static saveQuestions(question) {
        storage.saveQuestionToQuestionSet(+questionsetid, question);
    }

    static removeQuestion(id) {
        storage.removeQuestionFromQuestionSet(+questionsetid, id)
    }

    static updatequestion(question) {
        storage.updateQuestioninQuestionSet(+questionsetid, question)
    }

    static clearAllQuestions() {
        storage.removeAllQuestionsFromQuestionSet(+questionsetid)
    }



    // Function to get questions and respective answers related to the TestQuestionSet
    static async getQuestionsAndAnswers(questionSetId) {
        const response = await fetch(`/CBT/get-questions-answers/${questionSetId}/`)
        if (response.status !== 200) {
            throw new Error('Oops Something went wrong');
        }
        const data = await response.json()
        return data;
    }

    // Function to save a particular question to the TestQuestionSet
    static saveQuestionToQuestionSet(questionSetId, question) {
        const questiondata = {
            question_id: question.id,
            question_text: question.questionText,
            question_mark: question.questionMark,
            question_required: question.questionrequired,
            question_answers: question.answers
        };
        fetch(`/CBT/save-question/${questionSetId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(questiondata)
        })
            .then(response => response.json())
            .then(
                data => {
                    const type = 'alert-success'
                    const message = data['message']
                    displayalert(type, message)
                })
            .catch(error => console.error('Error:', error));
    }

    // Function to remove a particular question from the TestQuestionSet
    static removeQuestionFromQuestionSet(questionSetId, questionid) {
        const maindata = { question_id: questionid };
        fetch(`/CBT/remove-question/${questionSetId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(maindata)
        })
            .then(response => response.json())
            .then(data => {
                const type = 'alert-success'
                const message = data['message']
                displayalert(type, message)
            })
            .catch(error => console.error('Error:', error));
    }

    static updateQuestioninQuestionSet(questionSetId, question) {
        const updatequestiondata = {
            question_id: question.id,
            question_text: question.questionText,
            question_mark: question.questionMark,
            question_required: question.questionrequired,
            question_answers: question.answers
        };
        fetch(`/CBT/update-question/${questionSetId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(updatequestiondata)
        })
            .then(response => response.json())
            .then(
                data => {
                    // Handle response message or do additional operations
                    const type = 'alert-success'
                    const message = data['message']
                    displayalert(type, message)
                })
            .catch(error => console.error('Error:', error));
    }

    // Function to remove all questions from the TestQuestionSet
    static removeAllQuestionsFromQuestionSet(questionSetId) {
        fetch(`/CBT/remove-all-questions/${questionSetId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        })
            .then(response => response.json())
            .then(data => {
                // Handle response message or do additional operations
                const type = 'alert-success'
                const message = data['message']
                displayalert(type, message)
            })
            .catch(error => console.error('Error:', error));
    }

    // Function to Submit Questions
    static submitQuestionstoServer(formattedSet) {
        fetch('/Teachers_Portal/submit_questions/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(formattedSet)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }
                return response.json();
            })
            .then(data => {
                const type = 'alert-success'
                const message = data['message']
                displaysubmitalert(type, message)
            })
            .catch(error => console.error('Error:', error));
    }

}




const app = new App();





