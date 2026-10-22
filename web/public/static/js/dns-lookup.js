/**
 * DNS Lookup Tool - Client-side JavaScript
 * Calls backend API for DNS queries with IP geolocation
 */

document.addEventListener('DOMContentLoaded', function () {
    const domainInput = document.getElementById('domainInput');
    const lookupBtn = document.getElementById('lookupBtn');
    const resultCard = document.getElementById('resultCard');
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');
    const displayDomain = document.getElementById('displayDomain');
    const recordsContainer = document.getElementById('recordsContainer');

    // Country code to flag emoji
    function countryCodeToFlag(countryCode) {
        if (!countryCode) return '🌍';
        const codePoints = countryCode
            .toUpperCase()
            .split('')
            .map(char => 127397 + char.charCodeAt());
        return String.fromCodePoint(...codePoints);
    }

    // Lookup button click
    lookupBtn.addEventListener('click', function () {
        const domain = domainInput.value.trim();
        if (!domain) {
            showError('Please enter a domain name');
            return;
        }

        lookupDNS(domain);
    });

    // Enter key
    domainInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            lookupBtn.click();
        }
    });

    function lookupDNS(domain) {
        showLoading();

        // Get CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
            getCookie('csrftoken');

        fetch('/api/dns-lookup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ domain: domain })
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
                console.error('DNS lookup error:', error);
                showError('Failed to perform DNS lookup. Please try again.');
            });
    }

    function displayResult(data) {
        hideLoading();
        errorState.style.display = 'none';
        resultCard.style.display = 'block';

        displayDomain.textContent = data.domain;

        let html = '';

        // A Records
        if (data.records.A && data.records.A.length > 0) {
            html += createRecordSection('A', 'IPv4 Addresses', data.records.A);
        }

        // AAAA Records
        if (data.records.AAAA && data.records.AAAA.length > 0) {
            html += createRecordSection('AAAA', 'IPv6 Addresses', data.records.AAAA);
        }

        // Hostname
        if (data.hostname) {
            html += createRecordSection('PTR', 'Reverse Hostname', [data.hostname]);
        }

        // Aliases
        if (data.aliases && data.aliases.length > 0) {
            html += createRecordSection('CNAME', 'Aliases', data.aliases);
        }

        if (html === '' && (!data.ipDetails || data.ipDetails.length === 0)) {
            html = `
                <div class="record-section">
                    <p class="no-records">No DNS records found for this domain.</p>
                </div>
            `;
        }

        // IP Details section
        if (data.ipDetails && data.ipDetails.length > 0) {
            html += createIpDetailsSection(data.ipDetails);
        }

        recordsContainer.innerHTML = html;
    }

    function createRecordSection(type, label, values) {
        return `
            <div class="record-section">
                <div class="record-type">${type} <span style="font-weight: 400; opacity: 0.8;">- ${label}</span></div>
                <div class="record-values">
                    ${values.map(v => `<div class="record-value">${escapeHtml(v)}</div>`).join('')}
                </div>
            </div>
        `;
    }

    function createIpDetailsSection(ipDetails) {
        let html = `
            <div class="ip-details-section">
                <div class="ip-details-title">📍 IP Geolocation Details</div>
                <div class="ip-detail-grid">
        `;

        ipDetails.forEach(ip => {
            if (ip.error) {
                html += `
                    <div class="ip-card">
                        <div class="ip-card-header">
                            <div class="ip-flag">🌍</div>
                            <div>
                                <div class="ip-address">${escapeHtml(ip.ip)}</div>
                                <div class="ip-location">Location unavailable</div>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                const flag = countryCodeToFlag(ip.countryCode);
                html += `
                    <div class="ip-card">
                        <div class="ip-card-header">
                            <div class="ip-flag">${flag}</div>
                            <div>
                                <div class="ip-address">${escapeHtml(ip.ip)}</div>
                                <div class="ip-location">${escapeHtml(ip.city || '')}, ${escapeHtml(ip.country || '')}</div>
                            </div>
                        </div>
                        <div class="ip-info-grid">
                            <div class="ip-info-item">
                                <span class="ip-info-label">Country</span>
                                <span class="ip-info-value">${escapeHtml(ip.country || '-')}</span>
                            </div>
                            <div class="ip-info-item">
                                <span class="ip-info-label">Region</span>
                                <span class="ip-info-value">${escapeHtml(ip.region || '-')}</span>
                            </div>
                            <div class="ip-info-item">
                                <span class="ip-info-label">City</span>
                                <span class="ip-info-value">${escapeHtml(ip.city || '-')}</span>
                            </div>
                            <div class="ip-info-item">
                                <span class="ip-info-label">ZIP</span>
                                <span class="ip-info-value">${escapeHtml(ip.zip || '-')}</span>
                            </div>
                            <div class="ip-info-item">
                                <span class="ip-info-label">Timezone</span>
                                <span class="ip-info-value">${escapeHtml(ip.timezone || '-')}</span>
                            </div>
                            <div class="ip-info-item">
                                <span class="ip-info-label">Coordinates</span>
                                <span class="ip-info-value">${ip.lat ? ip.lat.toFixed(4) : '-'}, ${ip.lon ? ip.lon.toFixed(4) : '-'}</span>
                            </div>
                            <div class="ip-info-item full-width">
                                <span class="ip-info-label">ISP</span>
                                <span class="ip-info-value">${escapeHtml(ip.isp || '-')}</span>
                            </div>
                            <div class="ip-info-item full-width">
                                <span class="ip-info-label">Organization</span>
                                <span class="ip-info-value">${escapeHtml(ip.org || '-')}</span>
                            </div>
                            <div class="ip-info-item full-width">
                                <span class="ip-info-label">AS Number</span>
                                <span class="ip-info-value">${escapeHtml(ip.as || '-')}</span>
                            </div>
                        </div>
                    </div>
                `;
            }
        });

        html += '</div></div>';
        return html;
    }

    function showLoading() {
        resultCard.style.display = 'none';
        errorState.style.display = 'none';
        loadingState.style.display = 'block';
        lookupBtn.disabled = true;
    }

    function hideLoading() {
        loadingState.style.display = 'none';
        lookupBtn.disabled = false;
    }

    function showError(message) {
        hideLoading();
        resultCard.style.display = 'none';
        errorState.style.display = 'block';
        errorState.textContent = '⚠️ ' + message;
    }

    function escapeHtml(str) {
        if (str === null || str === undefined) return '';
        const div = document.createElement('div');
        div.textContent = String(str);
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
