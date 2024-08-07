// studentApi.js
async function addStudent(studentdata) {
    const response = await fetch(`/Teachers_Portal/newStudent/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(studentdata)
    });
    return await response.json();
}

async function updateStudent(updatestudentdata) {
    const response = await fetch(`/Teachers_Portal/updateStudent/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(updatestudentdata)
    });
    return await response.json();
}

async function deleteStudents(studentidtoremove) {
    const response = await fetch(`/Teachers_Portal/DeleteStudents/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(studentidtoremove)
    });
    return await response.json();
}

export { addStudent, updateStudent, deleteStudents };
