// scripts.js

// Function to validate the student form before submission
function validateStudentForm() {
    const firstName = document.getElementById('first_name').value.trim();
    const middleName = document.getElementById('middle_names').value.trim(); // Optional
    const lastName = document.getElementById('last_name').value.trim();
    const creativityLevel = document.getElementById('creativity_level').value;
    const criticalThinkingSkill = document.getElementById('critical_thinking_skill').value;

    // Validation for first name and last name (both required)
    if (firstName === "") {
        alert("First name is required.");
        return false;
    }
    if (lastName === "") {
        alert("Last name is required.");
        return false;
    }

    // Validation for creativity level (must be between 0 and 10)
    if (creativityLevel === "" || creativityLevel < 0 || creativityLevel > 10) {
        alert("Creativity level must be between 0 and 10.");
        return false;
    }

    // Validation for critical thinking skill (must be between 0 and 10)
    if (criticalThinkingSkill === "" || criticalThinkingSkill < 0 || criticalThinkingSkill > 10) {
        alert("Critical thinking skill must be between 0 and 10.");
        return false;
    }

    // If all validations pass
    return true;
}

// Function to add a new subject input field dynamically
function addSubjectField() {
    const subjectsDiv = document.getElementById('subjects');

    // Create a new div for the new subject
    const newSubjectDiv = document.createElement('div');
    newSubjectDiv.classList.add('subject-input'); // Optional: Add a class for consistent styling
    
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

    // Optional: Add a remove button for the subject field
    const removeButton = document.createElement('button');
    removeButton.type = "button";
    removeButton.textContent = "Remove Subject";
    removeButton.classList.add('remove-subject-btn');
    removeButton.onclick = function () {
        subjectsDiv.removeChild(newSubjectDiv);
    };

    // Append elements to the new div
    newSubjectDiv.appendChild(subjectLabel);
    newSubjectDiv.appendChild(subjectInputName);
    newSubjectDiv.appendChild(scoreLabel);
    newSubjectDiv.appendChild(scoreInput);
    newSubjectDiv.appendChild(removeButton); // Optional: Append remove button

    // Append the new div to the subjects section
    subjectsDiv.appendChild(newSubjectDiv);
}

