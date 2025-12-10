/**
 * JSON Formatter Pro - Enhanced Application JavaScript
 * Handles all frontend functionality and API integration
 */

// DOM Elements
const elements = {
    inputJson: document.getElementById('inputJson'),
    outputJson: document.getElementById('outputJson'),
    formatBtn: document.getElementById('formatBtn'),
    minifyBtn: document.getElementById('minifyBtn'),
    validateBtn: document.getElementById('validateBtn'),
    toXmlBtn: document.getElementById('toXmlBtn'),
    toCsvBtn: document.getElementById('toCsvBtn'),
    clearBtn: document.getElementById('clearBtn'),
    downloadBtn: document.getElementById('downloadBtn'),
    themeToggle: document.getElementById('themeToggle'),
    uploadZone: document.getElementById('uploadZone'),
    fileInput: document.getElementById('fileInput'),
    messageContainer: document.getElementById('messageContainer'),
    inputCount: document.getElementById('inputCount'),
    outputCount: document.getElementById('outputCount'),
    fullscreenBtn: document.getElementById('fullscreenBtn'),
    fullscreenModal: document.getElementById('fullscreenModal'),
    closeFullscreen: document.getElementById('closeFullscreen'),
    fullscreenOutput: document.getElementById('fullscreenOutput'),
    errorIndicator: document.getElementById('errorIndicator'),
    errorDetails: document.getElementById('errorDetails'),
    currentYear: document.getElementById('currentYear'),
    hamburgerBtn: document.getElementById('hamburgerBtn'),
    navMenu: document.getElementById('navMenu')
};

// API Base URL
const API_BASE = window.location.origin;

// Current output type (for download functionality with proper filenames)
let currentOutputType = 'json';
let currentOperation = 'formatted'; // formatted, minified, validated, converted

// ====================
// Dynamic Footer Year
// ====================

function setCurrentYear() {
    if (elements.currentYear) {
        elements.currentYear.textContent = new Date().getFullYear();
    }
}

// ====================
// Theme Toggle - Handled in base.html
// ====================
// Theme toggle is handled in base.html inline script
// Removed duplicate code to prevent conflicts

// Apply saved theme on page load (kept for compatibility)
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// ====================
// Fullscreen Modal
// ====================

function openFullscreen() {
    const output = elements.outputJson.value.trim();

    if (!output) {
        showMessage('error', 'No Output', 'There is no output to display in fullscreen.');
        return;
    }

    elements.fullscreenOutput.textContent = output;
    elements.fullscreenModal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeFullscreenModal() {
    elements.fullscreenModal.classList.remove('active');
    document.body.style.overflow = '';
}

function copyFullscreenContent() {
    const output = elements.fullscreenOutput.textContent;

    if (!output) {
        showMessage('error', 'No Content', 'There is no content to copy.');
        return;
    }

    navigator.clipboard.writeText(output).then(() => {
        showMessage('success', 'Copied!', 'Content copied to clipboard.');
    }).catch(() => {
        showMessage('error', 'Copy Failed', 'Failed to copy to clipboard.');
    });
}

// Close on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && elements.fullscreenModal.classList.contains('active')) {
        closeFullscreenModal();
    }
});

// Close on backdrop click
elements.fullscreenModal?.addEventListener('click', (e) => {
    if (e.target === elements.fullscreenModal) {
        closeFullscreenModal();
    }
});

// ====================
// Error Highlighting
// ====================

function highlightError(errorMessage) {
    // Parse error message to extract line and column
    // Common format: "Expecting property name enclosed in double quotes: line 3 column 5 (char 42)"
    const lineMatch = errorMessage.match(/line (\d+)/i);
    const columnMatch = errorMessage.match(/column (\d+)/i);

    if (lineMatch || columnMatch) {
        const line = lineMatch ? parseInt(lineMatch[1]) : null;
        const column = columnMatch ? parseInt(columnMatch[1]) : null;

        // Display error details
        if (elements.errorDetails) {
            const locationText = line && column
                ? `Line ${line}, Column ${column}`
                : line
                    ? `Line ${line}`
                    : column
                        ? `Column ${column}`
                        : 'Unknown location';

            elements.errorDetails.querySelector('.error-location').textContent = locationText;
            elements.errorDetails.querySelector('.error-message').textContent = errorMessage;
            elements.errorDetails.style.display = 'flex';

            // Highlight the line in the textarea
            if (line && elements.errorIndicator) {
                const textarea = elements.inputJson;
                const lines = textarea.value.split('\n');

                // Calculate the position of the error line
                const lineHeight = parseFloat(getComputedStyle(textarea).lineHeight) || 20;
                const topPosition = (line - 1) * lineHeight;

                // Position the error indicator
                elements.errorIndicator.style.top = `${topPosition}px`;
                elements.errorIndicator.style.height = `${lineHeight}px`;
                elements.errorIndicator.style.display = 'block';

                // Scroll to error position
                const scrollPosition = Math.max(0, topPosition - (textarea.offsetHeight / 2));
                textarea.scrollTop = scrollPosition;
            }
        }
    } else {
        // Show generic error without highlighting
        if (elements.errorDetails) {
            elements.errorDetails.querySelector('.error-location').textContent = 'JSON Error';
            elements.errorDetails.querySelector('.error-message').textContent = errorMessage;
            elements.errorDetails.style.display = 'flex';
        }
    }
}

function clearErrorHighlight() {
    if (elements.errorIndicator) {
        elements.errorIndicator.style.display = 'none';
    }
    if (elements.errorDetails) {
        elements.errorDetails.style.display = 'none';
    }
}

// ====================
// Message Display
// ====================

function showMessage(type, title, text) {
    const message = document.createElement('div');
    message.className = `message ${type}`;

    const icon = type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ';

    message.innerHTML = `
    <div class="message-icon">${icon}</div>
    <div class="message-content">
      <div class="message-title">${title}</div>
      <div class="message-text">${text}</div>
    </div>
    <button class="message-close" onclick="this.parentElement.remove()" aria-label="Close">&times;</button>
  `;

    elements.messageContainer.appendChild(message);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (message.parentElement) {
            message.style.animation = 'slideOut 0.3s ease-in-out';
            setTimeout(() => message.remove(), 300);
        }
    }, 5000);
}

// ====================
// Character Counter
// ====================

function updateCharCount() {
    const inputLength = elements.inputJson.value.length;
    const outputLength = elements.outputJson.value.length;

    // Only update if elements exist (homepage has charCount, not inputCount/outputCount)
    if (elements.inputCount) {
        elements.inputCount.textContent = `${inputLength.toLocaleString()} characters`;
    }
    if (elements.outputCount) {
        elements.outputCount.textContent = `${outputLength.toLocaleString()} characters`;
    }
    // For homepage with single charCount element
    const charCount = document.getElementById('charCount');
    if (charCount) {
        charCount.textContent = `${inputLength.toLocaleString()} characters`;
    }
}

// ====================
// API Calls
// ====================

async function makeApiCall(endpoint, data, loadingBtn) {
    try {
        // Clear any previous errors
        clearErrorHighlight();

        // Add loading state
        loadingBtn.classList.add('loading');

        const response = await fetch(`${API_BASE}/api/${endpoint}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data })
        });

        const result = await response.json();

        // Remove loading state
        loadingBtn.classList.remove('loading');

        return result;
    } catch (error) {
        loadingBtn.classList.remove('loading');
        throw error;
    }
}

// ====================
// Format JSON
// ====================

async function formatJson() {
    const input = elements.inputJson.value.trim();

    if (!input) {
        showMessage('error', 'No Input', 'Please enter JSON data to format.');
        return;
    }

    try {
        const result = await makeApiCall('format', input, elements.formatBtn);

        if (result.success) {
            elements.outputJson.value = result.formatted;
            currentOutputType = 'json';
            currentOperation = 'formatted';
            updateCharCount();
            showMessage('success', 'Formatted Successfully', 'Your JSON has been formatted with proper indentation.');
        } else {
            highlightError(result.error);
            showMessage('error', 'Format Failed', result.error);
        }
    } catch (error) {
        showMessage('error', 'Error', `Failed to format JSON: ${error.message}`);
    }
}

// ====================
// Minify JSON
// ====================

async function minifyJson() {
    const input = elements.inputJson.value.trim();

    if (!input) {
        showMessage('error', 'No Input', 'Please enter JSON data to minify.');
        return;
    }

    try {
        const result = await makeApiCall('minify', input, elements.minifyBtn);

        if (result.success) {
            elements.outputJson.value = result.minified;
            currentOutputType = 'json';
            currentOperation = 'minified';
            updateCharCount();
            showMessage('success', 'Minified Successfully', 'Your JSON has been compressed by removing whitespace.');
        } else {
            highlightError(result.error);
            showMessage('error', 'Minify Failed', result.error);
        }
    } catch (error) {
        showMessage('error', 'Error', `Failed to minify JSON: ${error.message}`);
    }
}

// ====================
// Validate JSON
// ====================

async function validateJson() {
    const input = elements.inputJson.value.trim();

    if (!input) {
        showMessage('error', 'No Input', 'Please enter JSON data to validate.');
        return;
    }

    try {
        const result = await makeApiCall('validate', input, elements.validateBtn);

        if (result.valid) {
            elements.outputJson.value = JSON.stringify(result.data, null, 2);
            currentOutputType = 'json';
            currentOperation = 'validated';
            updateCharCount();
            clearErrorHighlight();
            showMessage('success', 'Valid JSON', result.message);
        } else {
            highlightError(result.message);
            showMessage('error', 'Invalid JSON', result.message);
        }
    } catch (error) {
        showMessage('error', 'Validation Error', `Failed to validate JSON: ${error.message}`);
    }
}

// ====================
// Convert to XML
// ====================

async function convertToXml() {
    const input = elements.inputJson.value.trim();

    if (!input) {
        showMessage('error', 'No Input', 'Please enter JSON data to convert to XML.');
        return;
    }

    try {
        const result = await makeApiCall('convert/xml', input, elements.toXmlBtn);

        if (result.success) {
            elements.outputJson.value = result.xml;
            currentOutputType = 'xml';
            currentOperation = 'converted';
            updateCharCount();
            showMessage('success', 'Converted to XML', 'Your JSON has been successfully converted to XML format.');
        } else {
            highlightError(result.error);
            showMessage('error', 'Conversion Failed', result.error);
        }
    } catch (error) {
        showMessage('error', 'Error', `Failed to convert to XML: ${error.message}`);
    }
}

// ====================
// Convert to CSV
// ====================

async function convertToCsv() {
    const input = elements.inputJson.value.trim();

    if (!input) {
        showMessage('error', 'No Input', 'Please enter JSON data to convert to CSV.');
        return;
    }

    try {
        const result = await makeApiCall('convert/csv', input, elements.toCsvBtn);

        if (result.success) {
            elements.outputJson.value = result.csv;
            currentOutputType = 'csv';
            currentOperation = 'converted';
            updateCharCount();
            showMessage('success', 'Converted to CSV', 'Your JSON has been successfully converted to CSV format.');
        } else {
            highlightError(result.error);
            showMessage('error', 'Conversion Failed', result.error);
        }
    } catch (error) {
        showMessage('error', 'Error', `Failed to convert to CSV: ${error.message}`);
    }
}

// ====================
// Base64 Encode
// ====================

async function base64Encode() {
    const input = elements.inputJson.value.trim();

    if (!input) {
        showMessage('error', 'No Input', 'Please enter text data to encode.');
        return;
    }

    try {
        // Use a temporary button for loading state (format button)
        const tempBtn = elements.formatBtn;
        tempBtn.classList.add('loading');

        const response = await fetch(`${API_BASE}/api/base64/encode/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: input })
        });

        const result = await response.json();
        tempBtn.classList.remove('loading');

        if (result.success) {
            elements.outputJson.value = result.encoded;
            currentOutputType = 'txt';
            currentOperation = 'encoded';
            updateCharCount();
            showMessage('success', 'Encoded Successfully', 'Your text has been encoded to Base64.');
        } else {
            showMessage('error', 'Encoding Failed', result.error);
        }
    } catch (error) {
        elements.formatBtn.classList.remove('loading');
        showMessage('error', 'Error', `Failed to encode: ${error.message}`);
    }
}

// ====================
// Base64 Decode
// ====================

async function base64Decode() {
    const input = elements.inputJson.value.trim();

    if (!input) {
        showMessage('error', 'No Input', 'Please enter Base64 data to decode.');
        return;
    }

    try {
        // Use a temporary button for loading state (minify button)
        const tempBtn = elements.minifyBtn;
        tempBtn.classList.add('loading');

        const response = await fetch(`${API_BASE}/api/base64/decode/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ data: input })
        });

        const result = await response.json();
        tempBtn.classList.remove('loading');

        if (result.success) {
            elements.outputJson.value = result.decoded;
            currentOutputType = 'txt';
            currentOperation = 'decoded';
            updateCharCount();
            showMessage('success', 'Decoded Successfully', 'Your Base64 data has been decoded to text.');
        } else {
            showMessage('error', 'Decoding Failed', result.error);
        }
    } catch (error) {
        elements.minifyBtn.classList.remove('loading');
        showMessage('error', 'Error', `Failed to decode: ${error.message}`);
    }
}

// ====================
// Clear Inputs
// ====================

function clearInputs() {
    elements.inputJson.value = '';
    elements.outputJson.value = '';
    currentOutputType = 'json';
    currentOperation = 'formatted';
    clearErrorHighlight();
    updateCharCount();
    showMessage('info', 'Cleared', 'All inputs and outputs have been cleared.');
}

// ====================
// Enhanced Download with Proper Filenames
// ====================

function downloadOutput() {
    const output = elements.outputJson.value.trim();

    if (!output) {
        showMessage('error', 'No Output', 'There is no output to download.');
        return;
    }

    // Define file extensions
    const extensions = {
        json: 'json',
        xml: 'xml',
        csv: 'csv',
        txt: 'txt' // Added for Base64
    };

    // Define MIME types for proper encoding
    const mimeTypes = {
        json: 'application/json;charset=utf-8',
        xml: 'application/xml;charset=utf-8',
        csv: 'text/csv;charset=utf-8',
        txt: 'text/plain;charset=utf-8' // Added for Base64
    };

    // Define filenames based on operation
    const filenames = {
        formatted: `formatted.${extensions[currentOutputType]}`,
        minified: `minified.${extensions[currentOutputType]}`,
        validated: `validated.${extensions[currentOutputType]}`,
        converted: `converted.${extensions[currentOutputType]}`,
        encoded: `encoded.${extensions[currentOutputType]}`, // Added for Base64
        decoded: `decoded.${extensions[currentOutputType]}`  // Added for Base64
    };

    const extension = extensions[currentOutputType] || 'txt';
    const mimeType = mimeTypes[currentOutputType] || 'text/plain;charset=utf-8';
    const filename = filenames[currentOperation] || `output.${extension}`;

    // Create blob with UTF-8 encoding
    const blob = new Blob([output], { type: mimeType });
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

// ====================
// File Upload
// ====================

function handleFileUpload(file) {
    if (!file) return;

    if (!file.name.endsWith('.json')) {
        showMessage('error', 'Invalid File', 'Please upload a JSON file.');
        return;
    }

    const reader = new FileReader();

    reader.onload = (e) => {
        elements.inputJson.value = e.target.result;
        clearErrorHighlight();
        updateCharCount();
        showMessage('success', 'File Loaded', `${file.name} has been loaded successfully.`);
    };

    reader.onerror = () => {
        showMessage('error', 'Read Error', 'Failed to read the file.');
    };

    reader.readAsText(file, 'UTF-8');
}

// ====================
// Hamburger Menu Toggle
// ====================

function toggleMobileMenu() {
    if (elements.hamburgerBtn && elements.navMenu) {
        elements.hamburgerBtn.classList.toggle('active');
        elements.navMenu.classList.toggle('active');
    }
}

function closeMobileMenu() {
    if (elements.hamburgerBtn && elements.navMenu) {
        elements.hamburgerBtn.classList.remove('active');
        elements.navMenu.classList.remove('active');
    }
}

// ====================
// Navigation Menu Actions
// ====================

function setupNavMenuActions() {
    const navItems = document.querySelectorAll('.dropdown-item[data-action]');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const action = e.currentTarget.dataset.action;

            // Close mobile menu when clicking an item
            closeMobileMenu();

            switch (action) {
                case 'format':
                    formatJson();
                    break;
                case 'minify':
                    minifyJson();
                    break;
                case 'validate':
                    validateJson();
                    break;
                case 'toXml':
                    convertToXml();
                    break;
                case 'toCsv':
                    convertToCsv();
                    break;
                case 'base64Encode':
                    base64Encode();
                    break;
                case 'base64Decode':
                    base64Decode();
                    break;
            }
        });
    });

    // Handle coming soon items
    const comingSoonItems = document.querySelectorAll('.dropdown-item.coming-soon');
    comingSoonItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            closeMobileMenu();
            showMessage('info', 'Coming Soon', 'This feature will be available in a future update.');
        });
    });

    // Mobile dropdown toggle
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            if (window.innerWidth <= 1024) {
                e.preventDefault();
                const parent = this.parentElement;
                parent.classList.toggle('open');
            }
        });
    });
}

// ====================
// Event Listeners
// ====================

// Button clicks - using optional chaining for null safety
elements.formatBtn?.addEventListener('click', formatJson);
elements.minifyBtn?.addEventListener('click', minifyJson);
elements.validateBtn?.addEventListener('click', validateJson);
elements.toXmlBtn?.addEventListener('click', convertToXml);
elements.toCsvBtn?.addEventListener('click', convertToCsv);
elements.clearBtn?.addEventListener('click', clearInputs);
elements.downloadBtn?.addEventListener('click', downloadOutput);
// Theme toggle handled in base.html - removed duplicate listener

// Hamburger menu - Handled in base.html inline script
// Removed duplicate event listener to prevent conflicts

// Fullscreen
elements.fullscreenBtn?.addEventListener('click', openFullscreen);
elements.closeFullscreen?.addEventListener('click', closeFullscreenModal);

// Copy fullscreen content
const copyFullscreenBtn = document.getElementById('copyFullscreen');
if (copyFullscreenBtn) {
    copyFullscreenBtn.addEventListener('click', copyFullscreenContent);
}

// Character counting
elements.inputJson?.addEventListener('input', () => {
    updateCharCount();
    clearErrorHighlight(); // Clear errors when user starts typing
});

// File upload
elements.uploadZone?.addEventListener('click', () => elements.fileInput?.click());
elements.fileInput?.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
    }
});

// Drag and drop
elements.uploadZone?.addEventListener('dragover', (e) => {
    e.preventDefault();
    elements.uploadZone.classList.add('dragover');
});

elements.uploadZone?.addEventListener('dragleave', () => {
    elements.uploadZone.classList.remove('dragover');
});

elements.uploadZone?.addEventListener('drop', (e) => {
    e.preventDefault();
    elements.uploadZone.classList.remove('dragover');

    if (e.dataTransfer.files.length > 0) {
        handleFileUpload(e.dataTransfer.files[0]);
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to format
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        formatJson();
    }

    // Ctrl/Cmd + K to clear
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        clearInputs();
    }

    // F11 to toggle fullscreen (if output exists)
    if (e.key === 'F11') {
        e.preventDefault();
        if (elements.outputJson.value.trim()) {
            openFullscreen();
        }
    }
});

// ====================
// Initialize
// ====================

function init() {
    initTheme();
    updateCharCount();
    setCurrentYear();
    setupNavMenuActions();
}

// Run initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
