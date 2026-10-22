/**
 * JSON to YAML Converter
 * Client-side JSON to YAML conversion
 */

document.addEventListener('DOMContentLoaded', function () {
    const jsonInput = document.getElementById('jsonInput');
    const yamlOutput = document.getElementById('yamlOutput');
    const convertBtn = document.getElementById('convertBtn');
    const clearBtn = document.getElementById('clearBtn');
    const sampleBtn = document.getElementById('sampleBtn');
    const copyBtn = document.getElementById('copyBtn');
    const inputCount = document.getElementById('inputCount');

    // Update character count
    function updateCount() {
        const count = jsonInput.value.length;
        inputCount.textContent = count.toLocaleString() + ' chars';
    }

    jsonInput.addEventListener('input', updateCount);

    // Convert JSON to YAML
    function jsonToYaml(obj, indent = 0) {
        const spaces = '  '.repeat(indent);
        let yaml = '';

        if (obj === null) {
            return 'null';
        }

        if (typeof obj === 'undefined') {
            return 'null';
        }

        if (typeof obj === 'string') {
            // Check if string needs quoting
            if (obj.includes('\n') || obj.includes(':') || obj.includes('#') ||
                obj.startsWith(' ') || obj.endsWith(' ') ||
                /^[0-9]/.test(obj) || obj === '' ||
                ['true', 'false', 'null', 'yes', 'no'].includes(obj.toLowerCase())) {
                return JSON.stringify(obj);
            }
            return obj;
        }

        if (typeof obj === 'number' || typeof obj === 'boolean') {
            return String(obj);
        }

        if (Array.isArray(obj)) {
            if (obj.length === 0) {
                return '[]';
            }
            yaml = '\n';
            obj.forEach(item => {
                const itemYaml = jsonToYaml(item, indent + 1);
                if (typeof item === 'object' && item !== null && !Array.isArray(item)) {
                    yaml += spaces + '- ' + itemYaml.trim().replace(/^\n/, '').replace(/^  /, '') + '\n';
                } else {
                    yaml += spaces + '- ' + itemYaml + '\n';
                }
            });
            return yaml.slice(0, -1); // Remove trailing newline
        }

        if (typeof obj === 'object') {
            const keys = Object.keys(obj);
            if (keys.length === 0) {
                return '{}';
            }
            yaml = indent > 0 ? '\n' : '';
            keys.forEach(key => {
                const value = obj[key];
                const valueYaml = jsonToYaml(value, indent + 1);

                // Handle simple values on same line
                if (typeof value !== 'object' || value === null) {
                    yaml += spaces + key + ': ' + valueYaml + '\n';
                } else {
                    yaml += spaces + key + ':' + valueYaml + '\n';
                }
            });
            return yaml.slice(0, -1); // Remove trailing newline
        }

        return String(obj);
    }

    // Convert button handler
    convertBtn.addEventListener('click', function () {
        const input = jsonInput.value.trim();

        if (!input) {
            yamlOutput.value = 'Error: Please enter JSON to convert';
            return;
        }

        try {
            const parsed = JSON.parse(input);
            const yaml = jsonToYaml(parsed);
            yamlOutput.value = yaml;
        } catch (e) {
            yamlOutput.value = 'Error: Invalid JSON\n\n' + e.message;
        }
    });

    // Clear button handler
    clearBtn.addEventListener('click', function () {
        jsonInput.value = '';
        yamlOutput.value = '';
        updateCount();
    });

    // Sample button handler
    sampleBtn.addEventListener('click', function () {
        const sample = {
            "name": "JSON Formatters Pro",
            "version": "2.0",
            "description": "Professional JSON tools",
            "features": [
                "JSON Formatting",
                "JSON Validation",
                "JSON to YAML",
                "JSON Diff"
            ],
            "settings": {
                "theme": "dark",
                "autoSave": true,
                "indentSize": 2
            },
            "active": true
        };
        jsonInput.value = JSON.stringify(sample, null, 2);
        updateCount();
    });

    // Copy button handler
    copyBtn.addEventListener('click', function () {
        const text = yamlOutput.value;
        if (!text) return;

        navigator.clipboard.writeText(text).then(() => {
            const originalText = copyBtn.textContent;
            copyBtn.textContent = '✓ Copied!';
            setTimeout(() => {
                copyBtn.textContent = originalText;
            }, 2000);
        });
    });

    // Initial count
    updateCount();
});
