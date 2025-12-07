/**
 * JSON Diff Tool
 * Client-side JSON comparison with visual diff
 */

document.addEventListener('DOMContentLoaded', function () {
    const jsonLeft = document.getElementById('jsonLeft');
    const jsonRight = document.getElementById('jsonRight');
    const compareBtn = document.getElementById('compareBtn');
    const swapBtn = document.getElementById('swapBtn');
    const clearBtn = document.getElementById('clearBtn');
    const sampleBtn = document.getElementById('sampleBtn');
    const diffResults = document.getElementById('diffResults');
    const diffStats = document.getElementById('diffStats');
    const diffOutput = document.getElementById('diffOutput');

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

    // Format value for display
    function formatValue(value) {
        if (typeof value === 'string') return `"${value}"`;
        if (typeof value === 'object') return JSON.stringify(value);
        return String(value);
    }

    // Compare button handler
    compareBtn.addEventListener('click', function () {
        const leftInput = jsonLeft.value.trim();
        const rightInput = jsonRight.value.trim();

        if (!leftInput || !rightInput) {
            diffResults.classList.add('active');
            diffStats.innerHTML = '';
            diffOutput.innerHTML = '<span style="color: var(--color-error);">Please provide JSON in both panels</span>';
            return;
        }

        try {
            const leftJson = JSON.parse(leftInput);
            const rightJson = JSON.parse(rightInput);

            // Check if identical
            if (deepEqual(leftJson, rightJson)) {
                diffResults.classList.add('active');
                diffStats.innerHTML = '<span class="stat-badge stat-same">✓ JSON objects are identical</span>';
                diffOutput.innerHTML = '';
                return;
            }

            // Find differences
            const diffs = findDiff(leftJson, rightJson);

            // Display stats
            diffStats.innerHTML = `
                <span class="stat-badge stat-added">+ ${diffs.added.length} Added</span>
                <span class="stat-badge stat-removed">− ${diffs.removed.length} Removed</span>
                <span class="stat-badge stat-changed">~ ${diffs.changed.length} Changed</span>
            `;

            // Display differences
            let output = '';

            diffs.removed.forEach(d => {
                output += `<span class="diff-line-removed">− ${d.path}: ${formatValue(d.value)}</span>`;
            });

            diffs.added.forEach(d => {
                output += `<span class="diff-line-added">+ ${d.path}: ${formatValue(d.value)}</span>`;
            });

            diffs.changed.forEach(d => {
                output += `<span class="diff-line-changed">~ ${d.path}: ${formatValue(d.oldValue)} → ${formatValue(d.newValue)}</span>`;
            });

            diffOutput.innerHTML = output || '<span style="color: var(--color-text-secondary);">No differences found</span>';
            diffResults.classList.add('active');

        } catch (e) {
            diffResults.classList.add('active');
            diffStats.innerHTML = '';
            diffOutput.innerHTML = `<span style="color: var(--color-error);">Error: Invalid JSON\n${e.message}</span>`;
        }
    });

    // Swap button handler
    swapBtn.addEventListener('click', function () {
        const temp = jsonLeft.value;
        jsonLeft.value = jsonRight.value;
        jsonRight.value = temp;
    });

    // Clear button handler
    clearBtn.addEventListener('click', function () {
        jsonLeft.value = '';
        jsonRight.value = '';
        diffResults.classList.remove('active');
        diffStats.innerHTML = '';
        diffOutput.innerHTML = '';
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
    });
});
