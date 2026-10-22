/**
 * IP Address Info - Client-side JavaScript
 * Uses ip-api.com free API for geolocation
 */

document.addEventListener('DOMContentLoaded', function () {
    const ipInput = document.getElementById('ipInput');
    const lookupBtn = document.getElementById('lookupBtn');
    const myIpBtn = document.getElementById('myIpBtn');
    const resultCard = document.getElementById('resultCard');
    const loadingState = document.getElementById('loadingState');
    const errorState = document.getElementById('errorState');

    // Country code to flag emoji mapping
    function countryCodeToFlag(countryCode) {
        if (!countryCode) return '🌍';
        const codePoints = countryCode
            .toUpperCase()
            .split('')
            .map(char => 127397 + char.charCodeAt());
        return String.fromCodePoint(...codePoints);
    }

    // Lookup button
    lookupBtn.addEventListener('click', function () {
        const ip = ipInput.value.trim();
        if (!ip) {
            showError('Please enter an IP address');
            return;
        }

        // Basic IP validation
        const ipv4Regex = /^(\d{1,3}\.){3}\d{1,3}$/;
        const ipv6Regex = /^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/;

        if (!ipv4Regex.test(ip) && !ipv6Regex.test(ip)) {
            showError('Please enter a valid IPv4 or IPv6 address');
            return;
        }

        lookupIP(ip);
    });

    // My IP button
    myIpBtn.addEventListener('click', function () {
        lookupIP(''); // Empty string gets user's own IP
    });

    // Enter key
    ipInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            lookupBtn.click();
        }
    });

    function lookupIP(ip) {
        showLoading();

        // Use ip-api.com free API (no key needed)
        // Note: HTTP only for free tier, HTTPS requires pro
        const url = ip
            ? `http://ip-api.com/json/${ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query`
            : `http://ip-api.com/json/?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query`;

        // Use CORS proxy if on HTTPS
        const finalUrl = window.location.protocol === 'https:'
            ? `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`
            : url;

        fetch(finalUrl)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'fail') {
                    showError(data.message || 'Failed to lookup IP address');
                    return;
                }

                displayResult(data);
            })
            .catch(error => {
                console.error('Lookup error:', error);
                showError('Failed to lookup IP address. Please try again.');
            });
    }

    function displayResult(data) {
        hideLoading();
        errorState.style.display = 'none';
        resultCard.style.display = 'block';

        // Update display
        document.getElementById('displayIp').textContent = data.query || '-';
        document.getElementById('flagEmoji').textContent = countryCodeToFlag(data.countryCode);
        document.getElementById('locationText').textContent = `${data.city || '-'}, ${data.country || '-'}`;

        // Update grid items
        document.getElementById('country').textContent = data.country || '-';
        document.getElementById('region').textContent = data.regionName || data.region || '-';
        document.getElementById('city').textContent = data.city || '-';
        document.getElementById('zip').textContent = data.zip || '-';
        document.getElementById('timezone').textContent = data.timezone || '-';
        document.getElementById('isp').textContent = data.isp || '-';
        document.getElementById('org').textContent = data.org || '-';
        document.getElementById('asn').textContent = data.as || '-';

        // Update map coordinates
        if (data.lat && data.lon) {
            document.getElementById('lat').textContent = data.lat.toFixed(4);
            document.getElementById('lon').textContent = data.lon.toFixed(4);
            document.getElementById('mapCoords').style.display = 'block';
            document.getElementById('mapPlaceholder').innerHTML = `
                <a href="https://www.openstreetmap.org/?mlat=${data.lat}&mlon=${data.lon}&zoom=10" 
                   target="_blank" 
                   style="color: var(--color-primary); text-decoration: none;">
                    📍 View on OpenStreetMap →
                </a>
            `;
        }

        // Update input with the IP
        ipInput.value = data.query || '';
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
});
