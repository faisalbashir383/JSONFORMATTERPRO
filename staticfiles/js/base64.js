/**
 * Base64 Encoder/Decoder - JavaScript
 */

// DOM Elements
const elements = {
    inputText: document.getElementById('inputText'),
    outputText: document.getElementById('outputText'),
    encodeBtn: document.getElementById('encodeBtn'),
    decodeBtn: document.getElementById('decodeBtn'),
    clearBtn: document.getElementById('clearBtn'),
    downloadBtn: document.getElementById('downloadBtn'),
    themeToggle: document.getElementById('themeToggle'),
    messageContainer: document.getElementById('messageContainer'),
    inputCount: document.getElementById('inputCount'),
    outputCount: document.getElementById('outputCount'),
    currentYear: document.getElementById('currentYear')
};

// Current operation type
let currentOperation = 'encoded';  // 'encoded' or 'decoded'

// Set current year
function setCurrentYear() {
    if (elements.currentYear) {
        elements.currentYear.textContent = new Date().getFullYear();
    }
}

// Show message
function showMessage(type, title, message) {
    const messageEl = document.createElement('div');
    messageEl.className = `message message-${type}`;
    messageEl.innerHTML = `
        <div class="message-header">
            <strong>${title}</strong>
            <button class="message-close" onclick="this.parentElement.parentElement.remove()">✕</button>
        </div>
        <div class="message-body">${message}</div>
    `;

    elements.messageContainer.appendChild(messageEl);

    setTimeout(() => {
        messageEl.classList.add('show');
    }, 10);

    setTimeout(() => {
        messageEl.classList.remove('show');
        setTimeout(() => messageEl.remove(), 300);
    }, 5000);
}

// Update character counts
function updateCharCount() {
    const inputLength = elements.inputText.value.length;
    const outputLength = elements.outputText.value.length;

    elements.inputCount.textContent = `${inputLength} character${inputLength !== 1 ? 's' : ''}`;
    elements.outputCount.textContent = `${outputLength} character${outputLength !== 1 ? 's' : ''}`;
}

// Encode to Base64
function encodeToBase64() {
    const input = elements.inputText.value;

    if (!input) {
        showMessage('error', 'No Input', 'Please enter text to encode.');
        return;
    }

    try {
        const encoded = btoa(unescape(encodeURIComponent(input)));
        elements.outputText.value = encoded;
        currentOperation = 'encoded';
        updateCharCount();
        showMessage('success', 'Encoded Successfully', 'Your text has been encoded to Base64.');
    } catch (error) {
        showMessage('error', 'Encoding Failed', error.message);
    }
}

// Decode from Base64
function decodeFromBase64() {
    const input = elements.inputText.value;

    if (!input) {
        showMessage('error', 'No Input', 'Please enter Base64 to decode.');
        return;
    }

    try {
        const decoded = decodeURIComponent(escape(atob(input.trim())));
        elements.outputText.value = decoded;
        currentOperation = 'decoded';
        updateCharCount();
        showMessage('success', 'Decoded Successfully', 'Your Base64 has been decoded to text.');
    } catch (error) {
        showMessage('error', 'Decoding Failed', 'Invalid Base64 string. Please check your input.');
    }
}

// Clear all
function clearAll() {
    elements.inputText.value = '';
    elements.outputText.value = '';
    currentOperation = 'encoded';
    updateCharCount();
    showMessage('info', 'Cleared', 'All inputs and outputs have been cleared.');
}

// Download output
function downloadOutput() {
    const output = elements.outputText.value.trim();

    if (!output) {
        showMessage('error', 'No Output', 'Nothing to download. Please encode or decode some text first.');
        return;
    }

    const filename = currentOperation === 'encoded' ? 'encoded.txt' : 'decoded.txt';
    const blob = new Blob([output], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showMessage('success', 'Downloaded', `File saved as ${filename}`);
}

// Theme Management
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// Event Listeners
elements.encodeBtn.addEventListener('click', encodeToBase64);
elements.decodeBtn.addEventListener('click', decodeFromBase64);
elements.clearBtn.addEventListener('click', clearAll);
elements.downloadBtn.addEventListener('click', downloadOutput);
elements.themeToggle.addEventListener('click', toggleTheme);
elements.inputText.addEventListener('input', updateCharCount);

// Initialize
loadTheme();
setCurrentYear();
updateCharCount();
