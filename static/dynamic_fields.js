document.addEventListener('DOMContentLoaded', function () {
    let fieldCount = 0;

    document.getElementById('add-field-button').addEventListener('click', function () {
        fieldCount++;
        
        // Prompt for field name
        const fieldName = prompt('Enter the field name:');
        if (!fieldName) return;  // Exit if no name is provided
        
        // Create a new field container
        const fieldContainer = document.createElement('div');
        fieldContainer.className = 'form-group';
        
        // Use escape function to avoid HTML injection
        const escapedFieldName = fieldName.replace(/</g, '&lt;').replace(/>/g, '&gt;');
        
        fieldContainer.innerHTML = `
            <label for="dynamic-field-${fieldCount}">${escapedFieldName}:</label>
            <input type="text" class="form-control" id="dynamic-field-${fieldCount}" name="dynamic_field_value_${fieldCount}">
            <input type="hidden" name="dynamic_field_name_${fieldCount}" value="${escapedFieldName}">
        `;
        
        // Append to the container
        document.getElementById('additional-fields-container').appendChild(fieldContainer);
    });

    // Add form validation for dynamic fields
    document.querySelector('form').addEventListener('submit', function(event) {
        let valid = true;
        const dynamicFields = document.querySelectorAll('input[name^="dynamic_field_value_"]');
        dynamicFields.forEach(field => {
            if (field.value.trim() === '') {
                valid = false;
                field.classList.add('is-invalid');
            } else {
                field.classList.remove('is-invalid');
            }
        });
        if (!valid) {
            event.preventDefault();
            alert('Please fill out all dynamic fields.');
        }
    });
});
