const form = document.getElementById("setup-form");
const input = document.getElementById("board-input");
const callButton = document.getElementById("call-button");
const grid = document.getElementById("board");
const message = document.getElementById("message");
const latest = document.getElementById("latest");

function render(state) {
    grid.innerHTML = state.board.map(number => {
        const called = state.called.includes(number);
        return `<div class="cell ${called ? "called" : ""}">${called ? "--" : number}</div>`;
    }).join("");
    latest.textContent = state.latest ? `Called: ${state.latest}` : "Called: None";
    callButton.disabled = state.bingo || state.finished;
    if (state.bingo) message.textContent = "BINGO!";
}

async function send(path, body = {}) {
    const response = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);
    return data;
}

form.addEventListener("submit", async event => {
    event.preventDefault();
    try {
        const board = input.value.trim().split(/\s+/).map(Number);
        const state = await send("/api/start", { board });
        message.textContent = "Game started. Call numbers when ready.";
        render(state);
        callButton.disabled = false;
    } catch (error) {
        message.textContent = error.message;
    }
});

callButton.addEventListener("click", async () => {
    try {
        render(await send("/api/call"));
    } catch (error) {
        message.textContent = error.message;
    }
});
