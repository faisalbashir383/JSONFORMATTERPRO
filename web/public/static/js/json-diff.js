/**
 * JSON Diff Tool
 * Client-side JSON comparison with inline visual highlighting
 */

document.addEventListener('DOMContentLoaded', function () {
    const jsonLeft = document.getElementById('jsonLeft');
    const jsonRight = document.getElementById('jsonRight');
    const highlightLeft = document.getElementById('highlightLeft');
    const highlightRight = document.getElementById('highlightRight');
    const compareBtn = document.getElementById('compareBtn');
    const swapBtn = document.getElementById('swapBtn');
    const clearBtn = document.getElementById('clearBtn');
    const sampleBtn = document.getElementById('sampleBtn');
    const editLeftBtn = document.getElementById('editLeftBtn');
    const editRightBtn = document.getElementById('editRightBtn');
    const diffSummary = document.getElementById('diffSummary');
    const statAdded = document.getElementById('statAdded');
    const statRemoved = document.getElementById('statRemoved');
    const statChanged = document.getElementById('statChanged');

    // Deep compare two values
    function deepEqual(a, b) {
        if (a === b) return true;
        if (typeof a !== typeof b) return false;
        if (a === null || b === null) return a === b;
        if (typeof a !== 'object') return a === b;

        if (Array.isArray(a) !== Array.isArray(b)) return false;

        const keysA = Object.keys(a);
        const keysB = Object.keys(b);

        if (keysA.length !== keysB.length) return false;

        for (const key of keysA) {
            if (!keysB.includes(key)) return false;
            if (!deepEqual(a[key], b[key])) return false;
        }

        return true;
    }

    // Find differences between two objects
    function findDiff(left, right, path = '') {
        const diffs = {
            added: [],
            removed: [],
            changed: []
        };

        // Handle null/undefined
        if (left === null || left === undefined) {
            if (right !== null && right !== undefined) {
                diffs.added.push({ path: path || 'root', value: right });
            }
            return diffs;
        }

        if (right === null || right === undefined) {
            diffs.removed.push({ path: path || 'root', value: left });
            return diffs;
        }

        // Different types
        if (typeof left !== typeof right) {
            diffs.changed.push({ path: path || 'root', oldValue: left, newValue: right });
            return diffs;
        }

        // Primitives
        if (typeof left !== 'object') {
            if (left !== right) {
                diffs.changed.push({ path: path || 'root', oldValue: left, newValue: right });
            }
            return diffs;
        }

        // Arrays
        if (Array.isArray(left) && Array.isArray(right)) {
            const maxLen = Math.max(left.length, right.length);
            for (let i = 0; i < maxLen; i++) {
                const itemPath = path ? `${path}[${i}]` : `[${i}]`;
                if (i >= left.length) {
                    diffs.added.push({ path: itemPath, value: right[i] });
                } else if (i >= right.length) {
                    diffs.removed.push({ path: itemPath, value: left[i] });
                } else {
                    const itemDiffs = findDiff(left[i], right[i], itemPath);
                    diffs.added.push(...itemDiffs.added);
                    diffs.removed.push(...itemDiffs.removed);
                    diffs.changed.push(...itemDiffs.changed);
                }
            }
            return diffs;
        }

        // Objects
        const allKeys = new Set([...Object.keys(left), ...Object.keys(right)]);
        for (const key of allKeys) {
            const keyPath = path ? `${path}.${key}` : key;
            if (!(key in left)) {
                diffs.added.push({ path: keyPath, value: right[key] });
            } else if (!(key in right)) {
                diffs.removed.push({ path: keyPath, value: left[key] });
            } else {
                const keyDiffs = findDiff(left[key], right[key], keyPath);
                diffs.added.push(...keyDiffs.added);
                diffs.removed.push(...keyDiffs.removed);
                diffs.changed.push(...keyDiffs.changed);
            }
        }

        return diffs;
    }

    // Escape HTML
    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Format value for display
    function formatValue(value) {
        if (typeof value === 'string') return `"${value}"`;
        if (typeof value === 'object') return JSON.stringify(value);
        return String(value);
    }

    // Create highlighted JSON with inline markers
    function createHighlightedJson(json, diffs, side) {
        // Get paths that apply to this side
        const pathsToHighlight = new Map();

        if (side === 'left') {
            // Removed items (in left, not in right)
            diffs.removed.forEach(d => {
                pathsToHighlight.set(d.path, { type: 'removed', tooltip: `Removed: ${formatValue(d.value)}` });
            });
            // Changed items - show old value
            diffs.changed.forEach(d => {
                pathsToHighlight.set(d.path, { type: 'changed', tooltip: `Changed from ${formatValue(d.oldValue)} to ${formatValue(d.newValue)}` });
            });
        } else {
            // Added items (in right, not in left)
            diffs.added.forEach(d => {
                pathsToHighlight.set(d.path, { type: 'added', tooltip: `Added: ${formatValue(d.value)}` });
            });
            // Changed items - show new value
            diffs.changed.forEach(d => {
                pathsToHighlight.set(d.path, { type: 'changed', tooltip: `Changed from ${formatValue(d.oldValue)} to ${formatValue(d.newValue)}` });
            });
        }

        // Recursively build highlighted JSON
        function highlightObject(obj, currentPath = '') {
            if (obj === null) return '<span class="json-null">null</span>';
            if (typeof obj === 'boolean') return `<span class="json-bool">${obj}</span>`;
            if (typeof obj === 'number') return `<span class="json-number">${obj}</span>`;
            if (typeof obj === 'string') return `<span class="json-string">"${escapeHtml(obj)}"</span>`;

            if (Array.isArray(obj)) {
                if (obj.length === 0) return '[]';
                let html = '[\n';
                obj.forEach((item, i) => {
                    const itemPath = currentPath ? `${currentPath}[${i}]` : `[${i}]`;
                    const highlight = pathsToHighlight.get(itemPath);
                    let itemHtml = highlightObject(item, itemPath);

                    if (highlight) {
                        itemHtml = `<span class="diff-${highlight.type}" data-tooltip="${escapeHtml(highlight.tooltip)}">${itemHtml}</span>`;
                    }

                    html += '  ' + itemHtml + (i < obj.length - 1 ? ',' : '') + '\n';
                });
                html += ']';
                return html;
            }

            if (typeof obj === 'object') {
                const keys = Object.keys(obj);
                if (keys.length === 0) return '{}';
                let html = '{\n';
                keys.forEach((key, i) => {
                    const keyPath = currentPath ? `${currentPath}.${key}` : key;
                    const highlight = pathsToHighlight.get(keyPath);
                    let valueHtml = highlightObject(obj[key], keyPath);
                    let lineHtml = `  <span class="json-key">"${escapeHtml(key)}"</span>: ${valueHtml}`;

                    if (highlight) {
                        lineHtml = `<span class="diff-${highlight.type}" data-tooltip="${escapeHtml(highlight.tooltip)}">${lineHtml}</span>`;
                    }

                    html += lineHtml + (i < keys.length - 1 ? ',' : '') + '\n';
                });
                html += '}';
                return html;
            }

            return escapeHtml(String(obj));
        }

        return highlightObject(json);
    }

    // Show edit mode
    function showEditMode() {
        jsonLeft.style.display = 'block';
        jsonRight.style.display = 'block';
        highlightLeft.classList.remove('active');
        highlightRight.classList.remove('active');
        editLeftBtn.style.display = 'none';
        editRightBtn.style.display = 'none';
        diffSummary.classList.remove('active');
    }

    // Compare button handler
    compareBtn.addEventListener('click', function () {
        const leftInput = jsonLeft.value.trim();
        const rightInput = jsonRight.value.trim();

        if (!leftInput || !rightInput) {
            alert('Please provide JSON in both panels');
            return;
        }

        try {
            const leftJson = JSON.parse(leftInput);
            const rightJson = JSON.parse(rightInput);

            // Find differences
            const diffs = findDiff(leftJson, rightJson);

            // Update stats
            statAdded.textContent = `+ ${diffs.added.length} Added`;
            statRemoved.textContent = `− ${diffs.removed.length} Removed`;
            statChanged.textContent = `~ ${diffs.changed.length} Changed`;

            // Check if identical
            if (diffs.added.length === 0 && diffs.removed.length === 0 && diffs.changed.length === 0) {
                alert('✓ JSON objects are identical!');
                return;
            }

            // Create highlighted views
            highlightLeft.innerHTML = createHighlightedJson(leftJson, diffs, 'left');
            highlightRight.innerHTML = createHighlightedJson(rightJson, diffs, 'right');

            // Switch to highlight mode
            jsonLeft.style.display = 'none';
            jsonRight.style.display = 'none';
            highlightLeft.classList.add('active');
            highlightRight.classList.add('active');
            editLeftBtn.style.display = 'block';
            editRightBtn.style.display = 'block';
            diffSummary.classList.add('active');

        } catch (e) {
            alert('Error: Invalid JSON\n' + e.message);
        }
    });

    // Edit buttons
    editLeftBtn.addEventListener('click', showEditMode);
    editRightBtn.addEventListener('click', showEditMode);

    // Swap button handler
    swapBtn.addEventListener('click', function () {
        const temp = jsonLeft.value;
        jsonLeft.value = jsonRight.value;
        jsonRight.value = temp;
        showEditMode();
    });

    // Clear button handler
    clearBtn.addEventListener('click', function () {
        jsonLeft.value = '';
        jsonRight.value = '';
        showEditMode();
    });

    // Sample button handler
    sampleBtn.addEventListener('click', function () {
        jsonLeft.value = JSON.stringify({
            "name": "John",
            "age": 30,
            "city": "New York",
            "skills": ["JavaScript", "Python"]
        }, null, 2);

        jsonRight.value = JSON.stringify({
            "name": "John Doe",
            "age": 31,
            "country": "USA",
            "skills": ["JavaScript", "Python", "Go"]
        }, null, 2);

        showEditMode();
    });
});
