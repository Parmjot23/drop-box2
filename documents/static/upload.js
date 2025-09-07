function uploadFiles(form, fileInput) {
    const files = fileInput.files;
    const progressContainer = document.getElementById('progress-container');
    const csrfToken = form.querySelector('input[name=csrfmiddlewaretoken]').value;
    const uploadButton = form.querySelector('button[type="submit"]');
    const folderSelect = form.querySelector('#id_folder');
    if (uploadButton) uploadButton.disabled = true;
    Array.from(files).forEach(file => {
        const wrapper = document.createElement('div');
        wrapper.className = 'upload-progress';
        const label = document.createElement('span');
        label.textContent = file.name + ': ';
        const progress = document.createElement('progress');
        progress.max = 100;
        progress.value = 0;
        wrapper.appendChild(label);
        wrapper.appendChild(progress);
        progressContainer.appendChild(wrapper);

        const formData = new FormData();
        formData.append('file', file);
        if (folderSelect && folderSelect.value) {
            formData.append('folder', folderSelect.value);
        }
        const xhr = new XMLHttpRequest();
        xhr.open('POST', form.action);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.responseType = 'json';
        xhr.upload.addEventListener('progress', e => {
            if (e.lengthComputable) {
                progress.value = (e.loaded / e.total) * 100;
            }
        });
        xhr.addEventListener('load', () => {
            progress.value = 100;
            label.textContent = file.name + ': Uploaded ✓';
        });
        xhr.addEventListener('error', () => {
            label.textContent = file.name + ': Failed ✗';
        });
        xhr.addEventListener('loadend', () => {
            if (uploadButton) uploadButton.disabled = false;
        });
        xhr.send(formData);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    if (form) {
        const fileInput = form.querySelector('input[type="file"]');
        form.addEventListener('submit', e => {
            e.preventDefault();
            uploadFiles(form, fileInput);
        });
    }
});
