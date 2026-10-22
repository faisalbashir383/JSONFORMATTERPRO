/**
 * QR Code Generator - Client-side JavaScript
 * Uses qrcode.js library from CDN
 */

document.addEventListener('DOMContentLoaded', function () {
    const qrContent = document.getElementById('qrContent');
    const qrSize = document.getElementById('qrSize');
    const fgColor = document.getElementById('fgColor');
    const fgColorText = document.getElementById('fgColorText');
    const generateBtn = document.getElementById('generateBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const qrDisplay = document.getElementById('qrDisplay');
    const inputLabel = document.getElementById('inputLabel');

    let currentType = 'text';
    let currentCanvas = null;

    console.log('QR Generator initialized');
    console.log('QRCode library available:', typeof QRCode !== 'undefined');

    // Preset buttons
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentType = this.dataset.type;
            updatePlaceholder();
        });
    });

    // Color picker
    fgColor.addEventListener('input', function () {
        fgColorText.textContent = this.value.toUpperCase();
    });

    // Generate button
    generateBtn.addEventListener('click', generateQR);

    // Download button
    downloadBtn.addEventListener('click', function () {
        if (currentCanvas) {
            const link = document.createElement('a');
            link.download = 'qrcode.png';
            link.href = currentCanvas.toDataURL('image/png');
            link.click();
        }
    });

    // Enter key
    qrContent.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            generateQR();
        }
    });

    function updatePlaceholder() {
        const placeholders = {
            'text': 'Enter any text to encode...',
            'url': 'https://example.com',
            'email': 'email@example.com',
            'phone': '+1234567890',
            'wifi': 'Network Name'
        };

        const labels = {
            'text': 'Enter Text',
            'url': 'Enter URL',
            'email': 'Enter Email Address',
            'phone': 'Enter Phone Number',
            'wifi': 'Enter WiFi Network Name'
        };

        qrContent.placeholder = placeholders[currentType] || placeholders.text;
        inputLabel.textContent = labels[currentType] || labels.text;
        qrContent.value = '';
    }

    function generateQR() {
        let content = qrContent.value.trim();
        console.log('Generate QR called with content:', content);

        if (!content) {
            alert('Please enter content to generate QR code');
            return;
        }

        // Format content based on type
        switch (currentType) {
            case 'url':
                if (!content.startsWith('http://') && !content.startsWith('https://')) {
                    content = 'https://' + content;
                }
                break;
            case 'email':
                if (!content.startsWith('mailto:')) {
                    content = 'mailto:' + content;
                }
                break;
            case 'phone':
                if (!content.startsWith('tel:')) {
                    content = 'tel:' + content.replace(/[^0-9+]/g, '');
                }
                break;
            case 'wifi':
                content = 'WIFI:T:nopass;S:' + content + ';;';
                break;
        }

        const size = parseInt(qrSize.value);
        const color = fgColor.value;

        console.log('Generating QR with:', { content, size, color });
        console.log('QRCode type:', typeof QRCode);

        // Clear previous QR
        qrDisplay.innerHTML = '';

        // Check if QRCode library is loaded
        if (typeof QRCode === 'undefined') {
            console.error('QRCode library not loaded!');
            qrDisplay.innerHTML = '<div class="qr-placeholder" style="color: red;">QR library failed to load. Please refresh the page.</div>';
            return;
        }

        // Create canvas
        const canvas = document.createElement('canvas');
        qrDisplay.appendChild(canvas);

        // Generate QR code using qrcode library
        try {
            QRCode.toCanvas(canvas, content, {
                width: size,
                margin: 2,
                color: {
                    dark: color,
                    light: '#FFFFFF'
                }
            }, function (error) {
                if (error) {
                    console.error('QR generation error:', error);
                    qrDisplay.innerHTML = '<div class="qr-placeholder" style="color: red;">Error: ' + error.message + '</div>';
                    downloadBtn.disabled = true;
                } else {
                    console.log('QR code generated successfully');
                    currentCanvas = canvas;
                    downloadBtn.disabled = false;
                }
            });
        } catch (e) {
            console.error('QR generation exception:', e);
            qrDisplay.innerHTML = '<div class="qr-placeholder" style="color: red;">Error: ' + e.message + '</div>';
        }
    }
});
