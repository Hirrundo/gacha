function openExchange() {
    document
        .getElementById('exchange-modal')
        .classList.add('active');
}

function closeExchange() {
    document
        .getElementById('exchange-modal')
        .classList.remove('active');
}

async function exchangeHearts(amount) {
    const formData = new FormData();
    formData.append('amount', amount);

   const csrfToken = document.querySelector(
    '[name=csrfmiddlewaretoken]'
).value;

const response = await fetch('/game/exchange/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrfToken,
    },
    body: formData,
});
    const data = await response.json();

    if (data.error) {
        document.getElementById('exchange-error').textContent =
            data.error;

        return;
    }

    document.getElementById('exchange-hearts').textContent =
        data.hearts;

    document.getElementById('exchange-spins').textContent =
        data.spins;

    document.getElementById('exchange-error').textContent = '';

    document.querySelectorAll('.balance').forEach((balance) => {
        balance.innerHTML =
            `❤️ ${data.hearts} 🎟️ ${data.spins}`;
    });
}
function closeWelcomeBonus() {
    const modal = document.getElementById('welcome-bonus-modal');

    if (modal) {
        modal.classList.remove('active');
    }
}