
const groupName = document.getElementById('groupname').value;
const grouptestname = document.getElementById('grouptestname').value;
const studentname = document.getElementById('studentname').value;
const studentclass = document.getElementById('studentclass').value;
const testduration = document.getElementById('testduration').value;
const testsubmitbtn = document.getElementById('testsubmit')
const testform = document.getElementById('testform')
const options = {
    groupName,
    grouptestname,
    studentname,
    studentclass
};

class TestQuestionSetGroup {
    constructor(options) {
        this.groupName = groupName || '';
        this.grouptestname = grouptestname || '';
        this.studentname = studentname || '';
        this.studentclass = studentclass || '';
        this.questionSets = [];
    }

    addQuestionSet(questionSet) {
        this.questionSets.push(questionSet);
    }

}

class TestQuestionSet {
    constructor(testSubject) {
        this.testSubject = testSubject;
        this.testQuestions = [];
        this.testTotalScore = 0;
    }

    addQuestion(question) {
        this.testQuestions.push(question);
    }

    calculateTotalScore() {
        this.testQuestions.forEach(question => {
            let questionScore = 0;
            question.testAnswers.forEach(answer => {
                if (answer.isCorrect) {
                    questionScore += question.testScore; // Increase by the question's score if the answer is correct
                }
            });
            this.testTotalScore += questionScore;
        });
    }
}

class TestQuestions {
    constructor(testquestiontext, testScore) {
        this.testquestiontext = testquestiontext;
        this.testScore = testScore;
        this.testAnswers = []
    }

    addAnswer(answer) {
        this.testAnswers.push(answer);
    }
}

class TestAnswer {
    constructor(answertext, isCorrect) {
        this.answertext = answertext;
        this.isCorrect = isCorrect;
    }
}


class App {
    constructor() {
        testform.addEventListener('submit', this.preventsubmit.bind(this))
        testsubmitbtn.addEventListener('click', this.submittestquestions.bind(this))
        window.addEventListener('DOMContentLoaded', this.startTimer.bind(this, +testduration ))
    }

    preventsubmit(e) {
        e.preventDefault();
       
        if (testform.checkValidity() === false) {
            // If the form is not valid, show Bootstrap's custom validation styles
            testform.classList.add('was-validated');
        } else {

            testform.classList.remove('was-validated');
            const modal = e.target.querySelector('.modal')
            $(modal).modal('show');

        }
        
    }

    
    submittestquestions(e) {
        const modal = e.target.closest('.modal')
        $(modal).modal('hide');
        this.submitTestGroup();
    }

    startTimer(duration) {
    let timer = duration * 60;
    const timerDisplay = document.getElementById('timer');

    let interval = setInterval(() => {
        const minutes = parseInt(timer / 60, 10);
        const seconds = parseInt(timer % 60, 10);

        timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

        if (--timer < 0) {
            clearInterval(interval);
            this.submitTestGroup();
        }
    }, 1000);
}


    submitTestGroup(){
        const formattedSet = new TestQuestionSetGroup(options);
        // get the question sets and append to the questionsetGroup
        const questionsets = document.querySelectorAll('.question_set');
        questionsets.forEach((questionset) => {
            const questionsetname = questionset.querySelector('.question_set_name').innerText;
            const testQuestionSet = new TestQuestionSet(questionsetname)
            formattedSet.addQuestionSet(testQuestionSet)

            // get the questions and append to the questionsets
            const questioncards = questionset.querySelectorAll('.test_card');
            questioncards.forEach((question) => {
                const questionmark = question.querySelector('.test_mark').innerText[0];
                const questiontext = question.querySelector('.test_question').innerText;
                const testquestion = new TestQuestions(questiontext, +questionmark)
                testQuestionSet.addQuestion(testquestion)

                // get the Answers and append to the questions
                const checkedRadioButtons = question.querySelectorAll('input[type="radio"]:checked');
                checkedRadioButtons.forEach((radio) => {
                    const answertext = radio.nextElementSibling.innerText
                    const answervalue = radio.nextElementSibling.dataset.iscorrect
                    const answermainvalue = answervalue == 'True' ? 'True' : '';
                    const answervalueBoolean = Boolean(answermainvalue)
                    const testanswer = new TestAnswer(answertext, answervalueBoolean)
                    testquestion.addAnswer(testanswer)
                });
            })
            testQuestionSet.calculateTotalScore();
        })
        this.submitDatatoServer(formattedSet);
    }

    submitDatatoServer(formattedSet) {
        fetch('/CBT/submit_test/', {
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
                if (data['submitted'] === 'false') {
                    window.location.href = `/CBT/${data['studentobject']}/${data['test_set_group']}/success/`;

                } else {
                    const alert = document.querySelector('.alert-danger')
                    alert.querySelector('.alert-text').innerHTML = `${data['message']}`
                    alert.classList.remove('d-none');
                    setTimeout(() => {
                        alert.classList.add('d-none');
                    }, 4000);
                }
            })
            .catch(error => console.error('Error:', error));
    }

}

const app = new App()








