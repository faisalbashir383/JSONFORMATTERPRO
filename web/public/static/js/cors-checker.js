/**
 * CORS Checker - Client-side JavaScript
 * Calls backend API to test CORS configuration
 */

document.addEventListener('DOMContentLoaded', function () {
    const urlInput = document.getElementById('urlInput');
    const originInput = document.getElementById('originInput');
    const checkBtn = document.getElementById('checkBtn');
    const resultCard = document.getElementById('resultCard');
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');

    // Check button click
    checkBtn.addEventListener('click', function () {
        const url = urlInput.value.trim();
        if (!url) {
            showError('Please enter a URL to test');
            return;
        }

        const origin = originInput.value.trim() || 'https://example.com';
        checkCORS(url, origin);
    });

    // Enter key
    urlInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            checkBtn.click();
        }
    });

    function checkCORS(url, origin) {
        showLoading();

        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
            getCookie('csrftoken');

        fetch('/api/cors-checker/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ url: url, origin: origin })
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    showError(data.error);
                    return;
                }

                displayResult(data);
            })
            .catch(error => {
                console.error('CORS check error:', error);
                showError('Failed to check CORS configuration. Please try again.');
            });
    }

    function displayResult(data) {
        hideLoading();
        errorState.style.display = 'none';
        resultCard.style.display = 'block';

        const statusHeader = document.getElementById('statusHeader');
        const statusIcon = document.getElementById('statusIcon');
        const statusText = document.getElementById('statusText');
        const statusDesc = document.getElementById('statusDesc');

        if (data.corsEnabled) {
            statusHeader.className = 'status-header enabled';
            statusIcon.textContent = '✅';
            statusText.textContent = 'CORS Enabled';

            if (data.allowsAnyOrigin) {
                statusDesc.textContent = 'Allows requests from any origin (*)';
            } else if (data.allowsTestOrigin) {
                statusDesc.textContent = `Allows requests from ${data.testOrigin}`;
            } else {
                statusDesc.textContent = `Origin allowed: ${data.headers['Access-Control-Allow-Origin']}`;
            }
        } else {
            statusHeader.className = 'status-header disabled';
            statusIcon.textContent = '❌';
            statusText.textContent = 'CORS Not Enabled';
            statusDesc.textContent = 'No Access-Control-Allow-Origin header found';
        }

        // Display headers
        const headersContainer = document.getElementById('headersContainer');
        const corsHeaders = [
            { key: 'Access-Control-Allow-Origin', label: 'Allow-Origin' },
            { key: 'Access-Control-Allow-Methods', label: 'Allow-Methods' },
            { key: 'Access-Control-Allow-Headers', label: 'Allow-Headers' },
            { key: 'Access-Control-Allow-Credentials', label: 'Allow-Credentials' },
            { key: 'Access-Control-Expose-Headers', label: 'Expose-Headers' },
            { key: 'Access-Control-Max-Age', label: 'Max-Age' }
        ];

        let html = '';
        corsHeaders.forEach(header => {
            const value = data.headers[header.key];
            html += `
                <div class="header-row">
                    <div class="header-name">${header.key}</div>
                    <div class="header-value ${!value ? 'empty' : ''}">${value || '(not set)'}</div>
                </div>
            `;
        });

        // Add status code
        html += `
            <div class="header-row">
                <div class="header-name">HTTP Status Code</div>
                <div class="header-value">${data.statusCode}</div>
            </div>
        `;

        headersContainer.innerHTML = html;
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
