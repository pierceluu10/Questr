document.addEventListener('DOMContentLoaded', function() {
    const displayUserXp = document.getElementById('display-user-xp');
    const hungerAvailableEl = document.getElementById('hunger-available');
    const hungerPointsInput = document.getElementById('hunger-points');
    const addPointsBtn = document.getElementById('add-points-btn');
    const confirmBtn = document.getElementById('confirm-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const allocateMsg = document.getElementById('allocate-msg');
    const progressBar = document.querySelector('.progress-bar');
    const petXpSpan = document.querySelector('.pet-xp');

    function updateUI(data) {
        if (displayUserXp) displayUserXp.textContent = data.user_xp;
        if (document.querySelector('.pet-points')) {
            document.querySelector('.pet-points').textContent = data.hunger_points;
        }
        if (progressBar) {
            progressBar.style.width = data.progress + '%';
            progressBar.textContent = (data.total_points % 3) + '/3';
        }
        if (hungerAvailableEl) hungerAvailableEl.textContent = data.user_xp;
        
        // Update pending points if any
        const pendingEl = document.querySelector('.text-muted');
        if (pendingEl && data.temp_points > 0) {
            pendingEl.textContent = `pending ${data.temp_points}`;
            pendingEl.style.display = 'inline';
        } else if (pendingEl) {
            pendingEl.style.display = 'none';
        }
    }

    // Add points handler
    if (addPointsBtn) {
        addPointsBtn.addEventListener('click', () => {
            const points = parseInt(hungerPointsInput.value, 10);
            if (points > 0) {
                fetch('/myQuestr/allocate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ points: points })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        updateUI(data);
                        allocateMsg.textContent = `Added ${points} points. Click Confirm to save or Cancel to refund.`;
                        allocateMsg.className = 'text-success small';
                    } else {
                        allocateMsg.textContent = data.error;
                        allocateMsg.className = 'text-danger small';
                    }
                })
                .catch(error => {
                    allocateMsg.textContent = 'Error occurred while feeding. Please try again.';
                    allocateMsg.className = 'text-danger small';
                });
            }
        });
    }

    // Confirm button handler
    if (confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            fetch('/myQuestr/confirm', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload(); // Refresh to show new stage if applicable
                    } else {
                        allocateMsg.textContent = data.error;
                        allocateMsg.className = 'text-danger small';
                    }
                });
        });
    }

    // Cancel button handler
    if (cancelBtn) {
        cancelBtn.addEventListener('click', () => {
            fetch('/myQuestr/cancel', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.reload();
                    } else {
                        allocateMsg.textContent = data.error;
                        allocateMsg.className = 'text-danger small';
                    }
                });
        });
    }
});
        fetch('/myQuestr/select', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({pet: pet}),
            credentials: 'same-origin'
        }).then(r => r.json()).then(data => {
            if (data.success) {
                // request fresh page data
                fetch('/myQuestr').then(r => r.text()).then(html => {
                    // simple approach: reload page fragment by reload
                    window.location.reload();
                });
            } else {
                alert(data.error || 'Error selecting pet');
            }
        }).catch(err => {
            console.error(err);
            alert('Error selecting pet');
        });
    });

    // Add points
    if (addBtn) addBtn.addEventListener('click', function() {
        const pts = parseInt(pointsInput.value || '0', 10);
        if (!pts || pts <= 0) return alert('Enter valid hunger points');
        fetch('/myQuestr/allocate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({points: pts}),
            credentials: 'same-origin'
        }).then(r => r.json()).then(data => {
            if (data.success) {
                allocateMsg.textContent = `Allocated ${pts} hunger points (pending).`;
                // refresh UI values
                fetch('/myQuestr').then(r => r.text()).then(() => window.location.reload());
            } else {
                alert(data.error || 'Allocation failed');
            }
        }).catch(err => {
            console.error(err);
            alert('Allocation failed');
        });
    });

    if (confirmBtn) confirmBtn.addEventListener('click', function() {
        fetch('/myQuestr/confirm', {method: 'POST', credentials: 'same-origin'}).then(r => r.json()).then(data => {
            if (data.success) {
                allocateMsg.textContent = 'Feed confirmed.';
                window.location.reload();
            } else {
                alert(data.error || 'Confirm failed');
            }
        }).catch(err => {
            console.error(err);
            alert('Confirm failed');
        });
    });

    if (cancelBtn) cancelBtn.addEventListener('click', function() {
        fetch('/myQuestr/cancel', {method: 'POST', credentials: 'same-origin'}).then(r => r.json()).then(data => {
            if (data.success) {
                allocateMsg.textContent = 'Allocation refunded.';
                window.location.reload();
            } else {
                alert(data.error || 'Cancel failed');
            }
        }).catch(err => {
            console.error(err);
            alert('Cancel failed');
        });
    });

});
