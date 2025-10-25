document.addEventListener('DOMContentLoaded', function() {
    const petsRow = document.getElementById('pets-row');
    const activeNameEl = document.getElementById('active-pet-name');
    const hungerAvailableEl = document.getElementById('hunger-available');
    const userXpEl = document.getElementById('display-user-xp');
    const pointsInput = document.getElementById('hunger-points');
    const addBtn = document.getElementById('add-points-btn');
    const confirmBtn = document.getElementById('confirm-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const allocateMsg = document.getElementById('allocate-msg');

    function refreshPetCards(data) {
        // update user xp and hunger available
        if (data.user_xp !== undefined) userXpEl.textContent = data.user_xp;
        if (data.hunger_available !== undefined) hungerAvailableEl.textContent = data.hunger_available;
        if (data.active_pet !== undefined) activeNameEl.textContent = data.active_pet || 'None';
        // update cards if pet_data provided
        if (data.pets) {
            data.pets.forEach(p => {
                const card = document.querySelector(`.pet-card[data-pet="${p.name}"]`);
                if (card) {
                    card.querySelector('.pet-xp').textContent = p.xp;
                    // update image
                    const img = card.querySelector('img.pet-img');
                    if (img) img.src = `/static/images/pets/${p.name}_stage${p.stage}.png`;
                    // toggle selected
                    if (data.active_pet === p.name) {
                        card.classList.add('pet-selected');
                    } else {
                        card.classList.remove('pet-selected');
                    }
                }
            });
        }
    }

    // Select pet handler
    petsRow.addEventListener('click', function(e) {
        const btn = e.target.closest('.select-pet-btn');
        if (!btn) return;
        const card = btn.closest('.pet-card');
        const pet = card.dataset.pet;
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
