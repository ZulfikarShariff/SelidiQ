// scripts.js

// Function to validate the student form before submission
function validateStudentForm() {
    const name = document.getElementById('name').value;
    const creativityLevel = document.getElementById('creativity_level').value;
    const criticalThinkingSkill = document.getElementById('critical_thinking_skill').value;

    if (name === "") {
        alert("Name is required.");
        return false;
    }
    if (creativityLevel < 0 || creativityLevel > 10) {
        alert("Creativity level must be between 0 and 10.");
        return false;
    }
    if (criticalThinkingSkill < 0 || criticalThinkingSkill > 10) {
        alert("Critical thinking skill must be between 0 and 10.");
        return false;
    }
    return true;
}

// Function to add a new subject input field dynamically
function addSubjectField() {
    const subjectsDiv = document.getElementById('subjects');

    // Create a new div for the new subject
    const newSubjectDiv = document.createElement('div');
    
    // Create a label and input for the new subject
    const subjectLabel = document.createElement('label');
    subjectLabel.textContent = "Subject Name:";
    
    const subjectInputName = document.createElement('input');
    subjectInputName.type = "text";
    subjectInputName.name = "subject_name[]"; // Use array notation for multiple subjects

    const scoreLabel = document.createElement('label');
    scoreLabel.textContent = "Score:";

    const scoreInput = document.createElement('input');
    scoreInput.type = "number";
    scoreInput.name = "subject_score[]";
    scoreInput.step = "1"; // Step set to increment by 1

    // Append elements to the new div
    newSubjectDiv.appendChild(subjectLabel);
    newSubjectDiv.appendChild(subjectInputName);
    newSubjectDiv.appendChild(scoreLabel);
    newSubjectDiv.appendChild(scoreInput);

    // Append the new div to the subjects section
    subjectsDiv.appendChild(newSubjectDiv);
}

}

