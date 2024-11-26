document.addEventListener('DOMContentLoaded', function () {
    // Elements
    const uploadForm = document.getElementById('uploadForm');
    const deleteForm = document.getElementById('deleteForm');
    const updateForm = document.getElementById('updateForm');
    const pdfFileInput = document.getElementById('pdfFile');
    const pdfUpdateFileInput = document.getElementById('pdfUpdateFile');
    const fileToDeleteInput = document.getElementById('fileToDelete');
    const messageDiv = document.getElementById('message');
    const askButton = document.getElementById('askButton');
    const userPromptInput = document.getElementById('userPrompt');
    const responseArea = document.getElementById('responseArea');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // Utility function: Toggle Spinner visibility
    function toggleSpinner(show) {
        loadingSpinner.style.display = show ? 'block' : 'none';
    }

    // Utility function: Show messages
    function showMessage(message, type = 'info') {
        messageDiv.textContent = message;
        messageDiv.style.color = type === 'error' ? 'red' : 'green';
        setTimeout(() => {
            messageDiv.textContent = '';
        }, 3000);
    }

    // Add Document
    if (uploadForm) {
        uploadForm.addEventListener('submit', function (event) {
            event.preventDefault();

            if (!pdfFileInput.files.length) {
                showMessage('Please select a file to upload.', 'error');
                return;
            }

            const formData = new FormData();
            formData.append('pdf', pdfFileInput.files[0]);

            toggleSpinner(true);
            fetch('/add-doc', {
                method: 'POST',
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    showMessage(data.message);
                    toggleSpinner(false);
                })
                .catch((error) => {
                    console.error('Error adding document:', error);
                    showMessage('An error occurred while adding the document.', 'error');
                    toggleSpinner(false);
                });
        });
    }

    // Delete Document
    if (deleteForm) {
        deleteForm.addEventListener('submit', function (event) {
            event.preventDefault();

            if (!fileToDeleteInput.value.trim()) {
                showMessage('Please enter the file name to delete.', 'error');
                return;
            }

            const formData = new URLSearchParams();
            formData.append('file_name', fileToDeleteInput.value);

            toggleSpinner(true);
            fetch('/delete-doc', {
                method: 'POST',
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    showMessage(data.message);
                    toggleSpinner(false);
                })
                .catch((error) => {
                    console.error('Error deleting document:', error);
                    showMessage('An error occurred while deleting the document.', 'error');
                    toggleSpinner(false);
                });
        });
    }

    // Update Document
    if (updateForm) {
        updateForm.addEventListener('submit', function (event) {
            event.preventDefault();

            if (!pdfUpdateFileInput.files.length) {
                showMessage('Please select a file to update.', 'error');
                return;
            }

            const formData = new FormData();
            formData.append('pdf', pdfUpdateFileInput.files[0]);

            toggleSpinner(true);
            fetch('/update-doc', {
                method: 'POST',
                body: formData,
            })
                .then((response) => response.json())
                .then((data) => {
                    showMessage(data.message);
                    toggleSpinner(false);
                })
                .catch((error) => {
                    console.error('Error updating document:', error);
                    showMessage('An error occurred while updating the document.', 'error');
                    toggleSpinner(false);
                });
        });
    }

    // Handle User Questions
    if (askButton && userPromptInput && responseArea) {
        askButton.addEventListener('click', function () {
            const prompt = userPromptInput.value.trim();

            if (!prompt) {
                showMessage('Please enter a question.', 'error');
                return;
            }

            toggleSpinner(true);

            fetch('/process-prompt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            })
                .then((response) => response.json())
                .then((data) => {
                    const responseText = data.response || 'No response available.';
                    const sourceDocs = data.source_doc || [];

                    // Display the response
                    responseArea.innerHTML = `
                        <p><strong>Response:</strong> ${responseText}</p>
                    `;

                    // Display source documents if available
                    if (sourceDocs.length > 0) {
                        const sourceList = document.createElement('ul');
                        sourceList.innerHTML = '<strong>Source Documents:</strong>';
                        sourceDocs.forEach((source) => {
                            const listItem = document.createElement('li');
                            listItem.textContent = source;
                            sourceList.appendChild(listItem);
                        });
                        responseArea.appendChild(sourceList);
                    } else {
                        responseArea.innerHTML += `
                            <p><em>No source documents found.</em></p>
                        `;
                    }

                    toggleSpinner(false);
                })
                .catch((error) => {
                    console.error('Error processing prompt:', error);
                    responseArea.textContent = 'An error occurred while processing your question.';
                    toggleSpinner(false);
                });
        });
    }
});
