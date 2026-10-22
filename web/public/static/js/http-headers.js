/**
 * HTTP Headers Parser - Client-side JavaScript
 * Parses and analyzes HTTP response headers
 */

document.addEventListener('DOMContentLoaded', function () {
    const headerInput = document.getElementById('headerInput');
    const parsedOutput = document.getElementById('parsedOutput');
    const parseBtn = document.getElementById('parseBtn');
    const sampleBtn = document.getElementById('sampleBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const statsBar = document.getElementById('statsBar');

    // Header descriptions and categories
    const headerInfo = {
        // Security Headers
        'content-security-policy': { category: 'security', desc: 'Prevents XSS attacks by specifying allowed content sources' },
        'x-frame-options': { category: 'security', desc: 'Prevents clickjacking by controlling iframe embedding' },
        'x-content-type-options': { category: 'security', desc: 'Prevents MIME type sniffing' },
        'x-xss-protection': { category: 'security', desc: 'Legacy XSS filter (deprecated in modern browsers)' },
        'strict-transport-security': { category: 'security', desc: 'Forces HTTPS connections' },
        'referrer-policy': { category: 'security', desc: 'Controls referrer information sent with requests' },
        'permissions-policy': { category: 'security', desc: 'Controls browser feature permissions' },
        'x-permitted-cross-domain-policies': { category: 'security', desc: 'Controls Adobe Flash/PDF cross-domain requests' },

        // Cache Headers
        'cache-control': { category: 'cache', desc: 'Directives for caching mechanisms' },
        'expires': { category: 'cache', desc: 'Date/time after which response is stale' },
        'etag': { category: 'cache', desc: 'Unique identifier for resource version' },
        'last-modified': { category: 'cache', desc: 'Date of last resource modification' },
        'age': { category: 'cache', desc: 'Time in seconds since response was generated' },
        'vary': { category: 'cache', desc: 'Headers that affect cache validity' },
        'pragma': { category: 'cache', desc: 'Legacy HTTP/1.0 cache control' },

        // CORS Headers
        'access-control-allow-origin': { category: 'cors', desc: 'Specifies allowed origins for cross-origin requests' },
        'access-control-allow-methods': { category: 'cors', desc: 'Allowed HTTP methods for CORS' },
        'access-control-allow-headers': { category: 'cors', desc: 'Allowed request headers for CORS' },
        'access-control-allow-credentials': { category: 'cors', desc: 'Whether credentials are allowed' },
        'access-control-expose-headers': { category: 'cors', desc: 'Headers exposed to frontend JavaScript' },
        'access-control-max-age': { category: 'cors', desc: 'Preflight request cache duration' },

        // Content Headers
        'content-type': { category: 'content', desc: 'Media type of the response body' },
        'content-length': { category: 'content', desc: 'Size of the response body in bytes' },
        'content-encoding': { category: 'content', desc: 'Compression algorithm used' },
        'content-language': { category: 'content', desc: 'Language of the content' },
        'content-disposition': { category: 'content', desc: 'How content should be displayed/downloaded' },
        'transfer-encoding': { category: 'content', desc: 'Encoding used for transfer' },

        // Server Headers
        'server': { category: 'server', desc: 'Server software information' },
        'x-powered-by': { category: 'server', desc: 'Backend technology (consider hiding)' },
        'date': { category: 'server', desc: 'Date and time of response' },
        'connection': { category: 'server', desc: 'Connection handling options' },

        // Cookie Headers
        'set-cookie': { category: 'cookie', desc: 'Sets HTTP cookies' },
        'cookie': { category: 'cookie', desc: 'Cookies sent to server' }
    };

    // Sample headers
    const sampleHeaders = `HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 1234
Cache-Control: public, max-age=3600
ETag: "abc123"
Last-Modified: Sat, 07 Dec 2024 10:00:00 GMT
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Server: nginx/1.24.0
Date: Sat, 07 Dec 2024 12:00:00 GMT
Vary: Accept-Encoding
Connection: keep-alive`;

    let parsedHeaders = [];

    // Parse headers
    parseBtn.addEventListener('click', function () {
        const input = headerInput.value.trim();
        if (!input) {
            showError('Please paste some HTTP headers to parse');
            return;
        }

        parseHeaders(input);
    });

    // Sample button
    sampleBtn.addEventListener('click', function () {
        headerInput.value = sampleHeaders;
    });

    // Clear button
    clearBtn.addEventListener('click', function () {
        headerInput.value = '';
        parsedOutput.innerHTML = `
            <div class="empty-state">
                <div class="icon">📋</div>
                <p>Paste headers on the left and click "Parse Headers"</p>
            </div>
        `;
        statsBar.style.display = 'none';
        parsedHeaders = [];
    });

    // Copy button
    copyBtn.addEventListener('click', function () {
        if (parsedHeaders.length === 0) {
            showError('No headers to copy');
            return;
        }

        const jsonOutput = {};
        parsedHeaders.forEach(h => {
            jsonOutput[h.name] = h.value;
        });

        navigator.clipboard.writeText(JSON.stringify(jsonOutput, null, 2))
            .then(() => {
                copyBtn.textContent = '✅ Copied!';
                setTimeout(() => {
                    copyBtn.textContent = '📋 Copy JSON';
                }, 2000);
            });
    });

    function parseHeaders(input) {
        const lines = input.split('\n');
        parsedHeaders = [];

        let stats = { total: 0, security: 0, cache: 0, cors: 0 };

        lines.forEach(line => {
            line = line.trim();
            if (!line) return;

            // Skip HTTP status line
            if (line.match(/^HTTP\/[\d.]+\s+\d+/)) return;

            // Parse header: value
            const colonIndex = line.indexOf(':');
            if (colonIndex === -1) return;

            const name = line.substring(0, colonIndex).trim();
            const value = line.substring(colonIndex + 1).trim();

            if (name && value) {
                const lowerName = name.toLowerCase();
                const info = headerInfo[lowerName] || { category: 'other', desc: '' };

                parsedHeaders.push({
                    name: name,
                    value: value,
                    category: info.category,
                    description: info.desc
                });

                stats.total++;
                if (info.category === 'security') stats.security++;
                if (info.category === 'cache') stats.cache++;
                if (info.category === 'cors') stats.cors++;
            }
        });

        if (parsedHeaders.length === 0) {
            showError('No valid headers found. Make sure format is "Header-Name: value"');
            return;
        }

        // Update stats
        document.getElementById('totalHeaders').textContent = stats.total;
        document.getElementById('securityHeaders').textContent = stats.security;
        document.getElementById('cacheHeaders').textContent = stats.cache;
        document.getElementById('corsHeaders').textContent = stats.cors;
        statsBar.style.display = 'flex';

        // Render parsed headers
        renderHeaders();
    }

    function renderHeaders() {
        let html = '';

        parsedHeaders.forEach(header => {
            const badgeClass = getBadgeClass(header.category);
            const badgeText = header.category.toUpperCase();

            html += `
                <div class="header-item">
                    <div class="header-name">
                        ${escapeHtml(header.name)}
                        ${header.category !== 'other' ? `<span class="header-badge ${badgeClass}">${badgeText}</span>` : ''}
                    </div>
                    <div class="header-value">${escapeHtml(header.value)}</div>
                    ${header.description ? `<div class="header-desc">${header.description}</div>` : ''}
                </div>
            `;
        });

        parsedOutput.innerHTML = html;
    }

    function getBadgeClass(category) {
        switch (category) {
            case 'security': return 'badge-security';
            case 'cache': return 'badge-cache';
            case 'cors': return 'badge-cors';
            case 'content': return 'badge-content';
            default: return '';
        }
    }

    function showError(message) {
        parsedOutput.innerHTML = `
            <div class="empty-state">
                <div class="icon">⚠️</div>
                <p>${message}</p>
            </div>
        `;
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
});
