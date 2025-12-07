/**
 * Markdown Preview - Client-side JavaScript
 * Uses marked.js for parsing
 */

document.addEventListener('DOMContentLoaded', function () {
    const markdownInput = document.getElementById('markdownInput');
    const preview = document.getElementById('preview');
    const sampleBtn = document.getElementById('sampleBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyHtmlBtn = document.getElementById('copyHtmlBtn');

    const sampleMarkdown = `# Welcome to Markdown Preview

This is a **live preview** of your markdown content.

## Features

- **Bold text** and *italic text*
- \`inline code\` and code blocks
- [Links](https://example.com)
- Lists and blockquotes

### Code Block

\`\`\`javascript
function hello() {
    console.log("Hello, World!");
}
\`\`\`

### Blockquote

> This is a blockquote.
> It can span multiple lines.

### Table

| Name | Age | City |
|------|-----|------|
| John | 25  | NYC  |
| Jane | 30  | LA   |

---

*Start editing to see your markdown rendered!*`;

    // Configure marked
    if (typeof marked !== 'undefined') {
        marked.setOptions({
            breaks: true,
            gfm: true
        });
    }

    // Live preview
    markdownInput.addEventListener('input', updatePreview);

    // Sample button
    sampleBtn.addEventListener('click', function () {
        markdownInput.value = sampleMarkdown;
        updatePreview();
    });

    // Clear button
    clearBtn.addEventListener('click', function () {
        markdownInput.value = '';
        preview.innerHTML = '<p style="color: var(--color-text-secondary); font-style: italic;">Start typing to see preview...</p>';
    });

    // Copy HTML button
    copyHtmlBtn.addEventListener('click', function () {
        const html = preview.innerHTML;
        navigator.clipboard.writeText(html).then(() => {
            copyHtmlBtn.textContent = '✅ Copied!';
            setTimeout(() => {
                copyHtmlBtn.textContent = '📋 Copy HTML';
            }, 2000);
        });
    });

    function updatePreview() {
        const markdown = markdownInput.value;

        if (!markdown.trim()) {
            preview.innerHTML = '<p style="color: var(--color-text-secondary); font-style: italic;">Start typing to see preview...</p>';
            return;
        }

        if (typeof marked !== 'undefined') {
            preview.innerHTML = marked.parse(markdown);
        } else {
            // Fallback simple markdown parsing
            preview.innerHTML = simpleMarkdown(markdown);
        }
    }

    // Simple fallback parser
    function simpleMarkdown(text) {
        return text
            .replace(/^### (.+)$/gm, '<h3>$1</h3>')
            .replace(/^## (.+)$/gm, '<h2>$1</h2>')
            .replace(/^# (.+)$/gm, '<h1>$1</h1>')
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/`(.+?)`/g, '<code>$1</code>')
            .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>')
            .replace(/^- (.+)$/gm, '<li>$1</li>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/^/g, '<p>')
            .replace(/$/g, '</p>');
    }
});
