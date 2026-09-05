let board = Array.from({length: 75}, (_, i) => i + 1).sort(() => Math.random() - .5).slice(0, 25);
board[12] = "FREE";
let called = new Set(["FREE"]);

let grid = document.getElementById("board");
board.forEach(v => grid.innerHTML += <div class="cell ${v === "FREE" ? "called" : ""}" id="c-${v}">${v}</div>);

