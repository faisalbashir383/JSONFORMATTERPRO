/**
 * JSON Tree Viewer
 * Interactive tree visualization for JSON data
 */

document.addEventListener('DOMContentLoaded', function () {
    const jsonInput = document.getElementById('jsonInput');
    const treeView = document.getElementById('treeView');
    const visualizeBtn = document.getElementById('visualizeBtn');
    const expandAllBtn = document.getElementById('expandAllBtn');
    const collapseAllBtn = document.getElementById('collapseAllBtn');
    const expandBtn = document.getElementById('expandBtn');
    const collapseBtn = document.getElementById('collapseBtn');
    const clearBtn = document.getElementById('clearBtn');
    const sampleBtn = document.getElementById('sampleBtn');

    // Create tree HTML from JSON
    function createTreeNode(key, value, isLast = true) {
        const type = getType(value);
        let html = '';

        if (type === 'object' || type === 'array') {
            const isEmpty = type === 'object' ? Object.keys(value).length === 0 : value.length === 0;
            const bracket = type === 'object' ? ['{', '}'] : ['[', ']'];
            const count = type === 'object' ? Object.keys(value).length : value.length;

            if (isEmpty) {
                html = `
                    <div class="tree-item">
                        <span class="tree-toggle"></span>
                        ${key !== null ? `<span class="tree-key">"${escapeHtml(key)}"</span>: ` : ''}
                        <span class="tree-type">${bracket[0]}${bracket[1]}</span>
                    </div>
                `;
            } else {
                html = `
                    <div class="tree-item tree-expandable">
                        <span class="tree-toggle" onclick="toggleNode(this)">▼</span>
                        ${key !== null ? `<span class="tree-key">"${escapeHtml(key)}"</span>: ` : ''}
                        <span class="tree-type">${bracket[0]} ${count} ${type === 'object' ? 'properties' : 'items'} ${bracket[1]}</span>
                    </div>
                    <div class="tree-node">
                `;

                if (type === 'object') {
                    const keys = Object.keys(value);
                    keys.forEach((k, i) => {
                        html += createTreeNode(k, value[k], i === keys.length - 1);
                    });
                } else {
                    value.forEach((item, i) => {
                        html += createTreeNode(i, item, i === value.length - 1);
                    });
                }

                html += '</div>';
            }
        } else {
            // Primitive value
            let valueClass = 'tree-value-' + type;
            let displayValue = formatValue(value, type);

            html = `
                <div class="tree-item">
                    <span class="tree-toggle"></span>
                    ${key !== null ? `<span class="tree-key">"${escapeHtml(String(key))}"</span>: ` : ''}
                    <span class="${valueClass}">${displayValue}</span>
                </div>
            `;
        }

        return html;
    }

    // Get type of value
    function getType(value) {
        if (value === null) return 'null';
        if (Array.isArray(value)) return 'array';
        return typeof value;
    }

    // Format value for display
    function formatValue(value, type) {
        if (type === 'string') return `"${escapeHtml(value)}"`;
        if (type === 'null') return 'null';
        if (type === 'boolean') return value ? 'true' : 'false';
        return escapeHtml(String(value));
    }

    // Escape HTML
    function escapeHtml(input) {
        const str = String(input);
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    // Toggle node expand/collapse
    window.toggleNode = function (element) {
        const parent = element.closest('.tree-item');
        const sibling = parent.nextElementSibling;

        if (sibling && sibling.classList.contains('tree-node')) {
            if (sibling.style.display === 'none') {
                sibling.style.display = '';
                element.textContent = '▼';
            } else {
                sibling.style.display = 'none';
                element.textContent = '▶';
            }
        }
    };

    // Expand all nodes
    function expandAll() {
        const toggles = treeView.querySelectorAll('.tree-toggle');
        toggles.forEach(toggle => {
            const parent = toggle.closest('.tree-item');
            const sibling = parent?.nextElementSibling;
            if (sibling && sibling.classList.contains('tree-node')) {
                sibling.style.display = '';
                toggle.textContent = '▼';
            }
        });
    }

    // Collapse all nodes
    function collapseAll() {
        const toggles = treeView.querySelectorAll('.tree-toggle');
        toggles.forEach(toggle => {
            const parent = toggle.closest('.tree-item');
            const sibling = parent?.nextElementSibling;
            if (sibling && sibling.classList.contains('tree-node')) {
                sibling.style.display = 'none';
                toggle.textContent = '▶';
            }
        });
    }

    // Visualize button handler
    visualizeBtn.addEventListener('click', function () {
        const input = jsonInput.value.trim();

        if (!input) {
            treeView.innerHTML = '<div style="color: var(--color-error); padding: 1rem;">Please enter JSON to visualize</div>';
            return;
        }

        try {
            const parsed = JSON.parse(input);
            const treeHtml = createTreeNode(null, parsed);
            treeView.innerHTML = `<div class="tree-root">${treeHtml}</div>`;
        } catch (e) {
            treeView.innerHTML = `<div style="color: var(--color-error); padding: 1rem;">Error: Invalid JSON<br><br>${escapeHtml(e.message)}</div>`;
        }
    });

    // Expand/Collapse buttons
    expandAllBtn.addEventListener('click', expandAll);
    collapseAllBtn.addEventListener('click', collapseAll);
    expandBtn.addEventListener('click', expandAll);
    collapseBtn.addEventListener('click', collapseAll);

    // Clear button handler
    clearBtn.addEventListener('click', function () {
        jsonInput.value = '';
        treeView.innerHTML = '<div style="color: var(--color-text-secondary); text-align: center; padding: 2rem;">Paste JSON and click "Visualize Tree" to see the structure</div>';
    });

    // Sample button handler
    sampleBtn.addEventListener('click', function () {
        const sample = {
            "company": "Tech Corp",
            "founded": 2020,
            "active": true,
            "headquarters": {
                "city": "San Francisco",
                "country": "USA",
                "coordinates": {
                    "lat": 37.7749,
                    "lng": -122.4194
                }
            },
            "employees": [
                {
                    "name": "Alice Johnson",
                    "role": "CEO",
                    "skills": ["Leadership", "Strategy"]
                },
                {
                    "name": "Bob Smith",
                    "role": "CTO",
                    "skills": ["JavaScript", "Python", "Go"]
                },
                {
                    "name": "Carol Williams",
                    "role": "Designer",
                    "skills": ["UI/UX", "Figma"]
                }
            ],
            "products": ["App", "API", "Dashboard"],
            "metadata": null
        };
        jsonInput.value = JSON.stringify(sample, null, 2);
    });
});
