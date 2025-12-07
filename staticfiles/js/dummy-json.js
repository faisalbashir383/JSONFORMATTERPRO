/**
 * Dummy JSON Generator
 * Generate random fake JSON data with customizable fields
 */

document.addEventListener('DOMContentLoaded', function () {
    const recordCount = document.getElementById('recordCount');
    const outputFormat = document.getElementById('outputFormat');
    const indentSize = document.getElementById('indentSize');
    const fieldOptions = document.getElementById('fieldOptions');
    const generateBtn = document.getElementById('generateBtn');
    const copyBtn = document.getElementById('copyBtn');
    const downloadBtn = document.getElementById('downloadBtn');
    const jsonOutput = document.getElementById('jsonOutput');

    // Sample data pools
    const firstNames = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Harper', 'Evelyn'];
    const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson'];
    const domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'company.com', 'email.com', 'mail.com', 'proton.me'];
    const streets = ['Main St', 'Oak Ave', 'Maple Dr', 'Cedar Ln', 'Pine Rd', 'Elm St', 'Washington Blvd', 'Park Ave', 'Lake Dr', 'Hill Rd', 'River Rd', 'Forest Ave', 'Sunset Blvd', 'Ocean Dr', 'Mountain View'];
    const cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte', 'Seattle', 'Denver', 'Boston', 'Portland', 'Miami'];
    const states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI', 'NJ', 'VA', 'WA', 'AZ', 'MA', 'CO', 'TN', 'IN', 'MD', 'MN'];
    const companies = ['Tech Solutions', 'Global Systems', 'Digital Dynamics', 'Cloud Innovations', 'Data Experts', 'Cyber Networks', 'Smart Technologies', 'Future Labs', 'Alpha Corp', 'Beta Industries', 'Gamma Tech', 'Delta Systems', 'Omega Solutions', 'Prime Consulting', 'Elite Software'];
    const bios = [
        'Passionate developer with expertise in modern web technologies.',
        'Creative problem solver who loves building innovative solutions.',
        'Full-stack engineer with a focus on scalable architecture.',
        'Tech enthusiast always exploring new frameworks and tools.',
        'Software craftsman dedicated to clean code and best practices.',
        'Results-driven professional with strong analytical skills.',
        'Experienced leader with a track record of successful projects.',
        'Detail-oriented specialist in user experience design.',
        'Strategic thinker with expertise in digital transformation.',
        'Collaborative team player passionate about agile methodologies.'
    ];

    // Utility functions
    function random(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    }

    function randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function randomDate() {
        const start = new Date(2020, 0, 1);
        const end = new Date();
        const date = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
        return date.toISOString().split('T')[0];
    }

    function randomPhone() {
        return `+1 (${randomInt(200, 999)}) ${randomInt(100, 999)}-${randomInt(1000, 9999)}`;
    }

    function randomEmail(firstName, lastName) {
        const separators = ['.', '_', ''];
        const sep = random(separators);
        const num = Math.random() > 0.5 ? randomInt(1, 99) : '';
        return `${firstName.toLowerCase()}${sep}${lastName.toLowerCase()}${num}@${random(domains)}`;
    }

    function randomAddress() {
        return {
            street: `${randomInt(100, 9999)} ${random(streets)}`,
            city: random(cities),
            state: random(states),
            zipCode: String(randomInt(10000, 99999)),
            country: 'USA'
        };
    }

    function randomAvatar(id) {
        const styles = ['avataaars', 'bottts', 'pixel-art', 'identicon', 'initials'];
        return `https://api.dicebear.com/7.x/${random(styles)}/svg?seed=${id}`;
    }

    // Generate a single record
    function generateRecord(id, fields) {
        const firstName = random(firstNames);
        const lastName = random(lastNames);
        const record = {};

        fields.forEach(field => {
            switch (field) {
                case 'id':
                    record.id = id;
                    break;
                case 'name':
                    record.name = `${firstName} ${lastName}`;
                    break;
                case 'email':
                    record.email = randomEmail(firstName, lastName);
                    break;
                case 'phone':
                    record.phone = randomPhone();
                    break;
                case 'address':
                    record.address = randomAddress();
                    break;
                case 'company':
                    record.company = random(companies);
                    break;
                case 'date':
                    record.createdAt = randomDate();
                    break;
                case 'avatar':
                    record.avatar = randomAvatar(id);
                    break;
                case 'bio':
                    record.bio = random(bios);
                    break;
                case 'age':
                    record.age = randomInt(18, 65);
                    break;
                case 'isActive':
                    record.isActive = Math.random() > 0.3;
                    break;
                case 'salary':
                    record.salary = randomInt(30000, 150000);
                    break;
            }
        });

        return record;
    }

    // Get selected fields
    function getSelectedFields() {
        const checkboxes = fieldOptions.querySelectorAll('input[type="checkbox"]:checked');
        return Array.from(checkboxes).map(cb => cb.value);
    }

    // Generate JSON
    function generateJSON() {
        const count = parseInt(recordCount.value) || 5;
        const format = outputFormat.value;
        const fields = getSelectedFields();

        if (fields.length === 0) {
            jsonOutput.value = 'Error: Please select at least one field';
            return;
        }

        let data;

        switch (format) {
            case 'array':
                data = [];
                for (let i = 1; i <= count; i++) {
                    data.push(generateRecord(i, fields));
                }
                break;
            case 'object':
                data = generateRecord(1, fields);
                break;
            case 'nested':
                data = {
                    status: 'success',
                    count: count,
                    timestamp: new Date().toISOString(),
                    data: []
                };
                for (let i = 1; i <= count; i++) {
                    data.data.push(generateRecord(i, fields));
                }
                break;
        }

        // Format output
        let indent;
        switch (indentSize.value) {
            case '2':
                indent = 2;
                break;
            case '4':
                indent = 4;
                break;
            case 'tab':
                indent = '\t';
                break;
            case '0':
                indent = 0;
                break;
            default:
                indent = 2;
        }

        jsonOutput.value = indent === 0
            ? JSON.stringify(data)
            : JSON.stringify(data, null, indent);
    }

    // Toggle checkbox item styling
    fieldOptions.addEventListener('change', function (e) {
        if (e.target.type === 'checkbox') {
            const item = e.target.closest('.checkbox-item');
            if (e.target.checked) {
                item.classList.add('checked');
            } else {
                item.classList.remove('checked');
            }
        }
    });

    // Generate button handler
    generateBtn.addEventListener('click', generateJSON);

    // Copy button handler
    copyBtn.addEventListener('click', function () {
        const text = jsonOutput.value;
        if (!text || text.startsWith('Error')) return;

        navigator.clipboard.writeText(text).then(() => {
            const originalText = copyBtn.textContent;
            copyBtn.textContent = '✓ Copied!';
            setTimeout(() => {
                copyBtn.textContent = originalText;
            }, 2000);
        });
    });

    // Download button handler
    downloadBtn.addEventListener('click', function () {
        const text = jsonOutput.value;
        if (!text || text.startsWith('Error')) return;

        const blob = new Blob([text], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'dummy-data.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    // Generate initial data
    generateJSON();
});
