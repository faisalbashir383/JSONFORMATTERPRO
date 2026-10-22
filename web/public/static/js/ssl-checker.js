/**
 * SSL Certificate Checker - Client-side JavaScript
 * Calls backend API for SSL certificate info
 */

document.addEventListener('DOMContentLoaded', function () {
    const domainInput = document.getElementById('domainInput');
    const checkBtn = document.getElementById('checkBtn');
    const resultCard = document.getElementById('resultCard');
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');

    // Check button click
    checkBtn.addEventListener('click', function () {
        const domain = domainInput.value.trim();
        if (!domain) {
            showError('Please enter a domain name');
            return;
        }

        checkSSL(domain);
    });

    // Enter key
    domainInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            checkBtn.click();
        }
    });

    function checkSSL(domain) {
        showLoading();

        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
            getCookie('csrftoken');

        fetch('/api/ssl-checker/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ domain: domain })
        })
            .then(response => response.json())
            .then(data => {
                if (data.error && !data.domain) {
                    showError(data.error);
                    return;
                }

                displayResult(data);
            })
            .catch(error => {
                console.error('SSL check error:', error);
                showError('Failed to check SSL certificate. Please try again.');
            });
    }

    function displayResult(data) {
        hideLoading();
        errorState.style.display = 'none';
        resultCard.style.display = 'block';

        const statusHeader = document.getElementById('statusHeader');
        const statusIcon = document.getElementById('statusIcon');
        const statusText = document.getElementById('statusText');
        const daysRemaining = document.getElementById('daysRemaining');

        // Determine status
        if (!data.valid) {
            statusHeader.className = 'status-header invalid';
            statusIcon.textContent = '❌';
            statusText.textContent = 'Invalid Certificate';
            daysRemaining.textContent = data.error || 'Certificate validation failed';
        } else if (data.expired) {
            statusHeader.className = 'status-header invalid';
            statusIcon.textContent = '⚠️';
            statusText.textContent = 'Certificate Expired';
            daysRemaining.textContent = `Expired ${Math.abs(data.daysRemaining)} day(s) ago`;
        } else if (data.daysRemaining <= 30) {
            statusHeader.className = 'status-header warning';
            statusIcon.textContent = '⚠️';
            statusText.textContent = 'Certificate Expiring Soon';
            daysRemaining.textContent = `Expires in <strong>${data.daysRemaining}</strong> day(s)`;
        } else {
            statusHeader.className = 'status-header valid';
            statusIcon.textContent = '🔒';
            statusText.textContent = 'Valid Certificate';
            daysRemaining.textContent = `Expires in <strong>${data.daysRemaining}</strong> day(s)`;
        }

        // Update details
        if (data.subject) {
            document.getElementById('commonName').textContent = data.subject.commonName || '-';
            document.getElementById('organization').textContent = data.subject.organization || '-';
        }

        if (data.issuer) {
            const issuerText = data.issuer.organization
                ? `${data.issuer.commonName} (${data.issuer.organization})`
                : data.issuer.commonName || '-';
            document.getElementById('issuer').textContent = issuerText;
        }

        // Format dates
        if (data.validFrom) {
            const from = new Date(data.validFrom);
            document.getElementById('validFrom').textContent = from.toLocaleDateString('en-US', {
                year: 'numeric', month: 'long', day: 'numeric'
            });
        }

        if (data.validTo) {
            const to = new Date(data.validTo);
            document.getElementById('validTo').textContent = to.toLocaleDateString('en-US', {
                year: 'numeric', month: 'long', day: 'numeric'
            });
        }

        document.getElementById('serialNumber').textContent = data.serialNumber || '-';

        // Subject Alternative Names
        const sanList = document.getElementById('sanList');
        const sanTags = document.getElementById('sanTags');

        if (data.subjectAltNames && data.subjectAltNames.length > 0) {
            sanList.style.display = 'block';
            sanTags.innerHTML = data.subjectAltNames
                .slice(0, 10)  // Limit to 10
                .map(san => `<span class="san-tag">${escapeHtml(san)}</span>`)
                .join('');

            if (data.subjectAltNames.length > 10) {
                sanTags.innerHTML += `<span class="san-tag">+${data.subjectAltNames.length - 10} more</span>`;
            }
        } else {
            sanList.style.display = 'none';
        }
    }

    function showLoading() {
        resultCard.style.display = 'none';
        errorState.style.display = 'none';
        loadingState.style.display = 'block';
        checkBtn.disabled = true;
    }

    function hideLoading() {
        loadingState.style.display = 'none';
        checkBtn.disabled = false;
    }

    function showError(message) {
        hideLoading();
        resultCard.style.display = 'none';
        errorState.style.display = 'block';
        errorState.textContent = '⚠️ ' + message;
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
