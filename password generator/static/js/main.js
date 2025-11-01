// ================= Password Generator =================
async function generatePassword() {
  const length = document.getElementById("length").value;
  const uppercase = document.getElementById("uppercase").checked;
  const lowercase = document.getElementById("lowercase").checked;
  const numbers = document.getElementById("numbers").checked;
  const symbols = document.getElementById("symbols").checked;

  const response = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ length, uppercase, lowercase, numbers, symbols }),
  });
  const data = await response.json();
  document.getElementById("passwordOutput").value = data.password || "Error";
}

// ================= Hash Password =================
async function hashPassword() {
  const password = document.getElementById("hashInput").value.trim();
  if (!password) return;

  const algorithm = document.getElementById("algorithm").value;
  const response = await fetch("/hash", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password, algorithm }),
  });
  const data = await response.json();
  document.getElementById("hashOutput").value = data.hash || "Error";
}

// ================= Copy Functions =================
async function copyToClipboard(id) {
  const el = document.getElementById(id);
  if (el.value.trim() === "") return;
  await navigator.clipboard.writeText(el.value);
  showNotification("Copied!");
}

// ================= Notification =================
function showNotification(msg) {
  const note = document.querySelector(".notification");
  note.textContent = msg;
  note.classList.add("show");
  setTimeout(() => note.classList.remove("show"), 1500);
}
