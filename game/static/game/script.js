const cooldowns = {
    1: 2 * 60,
    2: 5 * 60,
    3: 7 * 60,
    4: 15 * 60,
    5: 30 * 60,
};

const interactionTimers = {};

const characterData = document.getElementById('character-data');
const characterId = characterData.dataset.characterId;
function showError(message) {
    const modal = document.getElementById('error-modal');
    const messageElement = document.getElementById('error-message');

    messageElement.textContent = message;
    modal.classList.add('active');

    setTimeout(() => {
        modal.classList.remove('active');
    }, 2500);
}
async function useInteraction(action) {
    const response = await fetch(
        `/game/character/${characterId}/interaction/${action}/`
    );

    const data = await response.json();
   if (data.error) {
    if (data.remaining) {
        startInteractionTimer(action, data.remaining);
    } else {
        showError(data.error);
    }

    return;
}
    
    document.getElementById('interaction-image').src = data.image;
    document.getElementById('interaction-title').textContent = data.title;
    document.getElementById('interaction-text').textContent = data.text;
    document.getElementById('interaction-reward').textContent =
        `+${data.reward} ❤️`;

    document
        .getElementById('interaction-modal')
        .classList.add('active');
    startInteractionTimer(action, cooldowns[action]);
}

function closeInteraction() {
    document
        .getElementById('interaction-modal')
        .classList.remove('active');
}
function startInteractionTimer(action, seconds) {
    const button = document.getElementById(
        `interaction-button-${action}`
    );

    if (!button) {
        return;
    }

    clearInterval(interactionTimers[action]);

    button.disabled = true;

    let remaining = seconds;

    function updateButton() {
        const minutes = Math.floor(remaining / 60);
        const secondsLeft = remaining % 60;

        button.textContent =
            `Доступно через ${minutes}:${String(secondsLeft).padStart(2, '0')}`;

        if (remaining <= 0) {
            clearInterval(interactionTimers[action]);

            button.disabled = false;
            button.textContent = action;

            return;
        }

        remaining--;
    }

    updateButton();

    interactionTimers[action] = setInterval(updateButton, 1000);
}
async function loadInteractionTimers() {
    const response = await fetch(
        `/game/character/${characterId}/interaction-status/`
    );

    const data = await response.json();

    if (!data.cooldowns) {
        return;
    }

    for (const action in data.cooldowns) {
        const remaining = data.cooldowns[action];

        if (remaining > 0) {
            startInteractionTimer(
                Number(action),
                remaining
            );
        }
    }
}

loadInteractionTimers();