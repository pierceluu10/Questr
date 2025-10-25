document.addEventListener('DOMContentLoaded', function() {
    const photoForm = document.getElementById('photo-form');
    const photoInput = document.getElementById('photo-input');
    const uploadBtn = document.getElementById('photo-upload-btn');
    const resetBtn = document.getElementById('photo-reset-btn');
    const topAvatar = document.getElementById('profile-avatar');
    const previewLarge = document.getElementById('profile-photo-preview');
    const previewSmall = document.getElementById('profile-photo-preview-small');

    function setAvatars(url) {
        if (topAvatar) topAvatar.src = url;
        if (previewLarge) previewLarge.src = url;
        if (previewSmall) previewSmall.src = url;
    }

    function showLoading(state) {
        if (uploadBtn) {
            if (state) {
                uploadBtn.dataset.orig = uploadBtn.innerHTML;
                uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
                uploadBtn.disabled = true;
            } else {
                if (uploadBtn.dataset.orig) uploadBtn.innerHTML = uploadBtn.dataset.orig;
                uploadBtn.disabled = false;
            }
        }
    }

    if (photoForm) {
        photoForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const file = photoInput.files[0];
            if (!file) return alert('Please choose a file to upload.');

            // Basic client-side validation
            const maxSize = 5 * 1024 * 1024; // 5MB
            if (file.size > maxSize) return alert('File too large. Max 5MB.');

            const allowed = ['image/png','image/jpeg','image/jpg','image/gif'];
            if (!allowed.includes(file.type)) return alert('Invalid file type.');

            const formData = new FormData();
            formData.append('photo', file);

            showLoading(true);

            fetch('/profile/photo/upload', {
                method: 'POST',
                body: formData,
                credentials: 'same-origin'
            })
            .then(resp => resp.json())
            .then(data => {
                showLoading(false);
                if (data && data.success) {
                    setAvatars(data.url);
                } else {
                    alert(data.error || 'Upload failed');
                }
            })
            .catch(err => {
                showLoading(false);
                console.error(err);
                alert('An error occurred while uploading.');
            });
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            if (!confirm('Reset your profile photo to the default?')) return;
            resetBtn.disabled = true;
            fetch('/profile/photo/reset', {method: 'POST', credentials: 'same-origin'})
                .then(r => r.json())
                .then(data => {
                    resetBtn.disabled = false;
                    if (data && data.success) {
                        setAvatars(data.url);
                    } else {
                        alert(data.error || 'Reset failed');
                    }
                })
                .catch(err => {
                    resetBtn.disabled = false;
                    console.error(err);
                    alert('An error occurred while resetting.');
                });
        });
    }

});
