// Submits <form data-ajax-form data-message="#elementId"> to its action as JSON and shows the
// result in the message element, instead of a full page reload. Used by the contact form and
// job applications, which post to the Pages Functions in functions/api/.
(function () {
    const STYLES = {
        success: { background: '#d1fae5', color: '#065f46', border: '1px solid #6ee7b7' },
        error: { background: '#fee2e2', color: '#991b1b', border: '1px solid #fca5a5' },
    };

    function show(box, type, lines) {
        Object.assign(box.style, STYLES[type], { display: 'block' });
        box.innerHTML = '';
        lines.forEach(function (line) {
            const p = document.createElement('p');
            p.style.margin = '0.25rem 0';
            p.textContent = (type === 'success' ? '✓ ' : '✕ ') + line;
            box.appendChild(p);
        });
        box.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    document.querySelectorAll('form[data-ajax-form]').forEach(function (form) {
        const box = document.querySelector(form.dataset.message);
        const button = form.querySelector('[type="submit"]');

        form.addEventListener('submit', async function (event) {
            event.preventDefault();
            const label = button.innerHTML;
            button.disabled = true;
            button.textContent = 'Sending...';
            try {
                const res = await fetch(form.action, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(Object.fromEntries(new FormData(form))),
                });
                const data = await res.json();
                if (data.success) {
                    show(box, 'success', [data.message]);
                    form.reset();
                } else {
                    show(box, 'error', data.errors || [data.error || 'Something went wrong. Please try again.']);
                }
            } catch (e) {
                show(box, 'error', ['Could not send. Please check your connection and try again.']);
            } finally {
                button.disabled = false;
                button.innerHTML = label;
            }
        });
    });
})();
