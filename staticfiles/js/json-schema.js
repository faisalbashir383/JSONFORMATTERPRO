/**
 * JSON Schema Validator
 * Client-side JSON Schema validation
 */

document.addEventListener('DOMContentLoaded', function () {
    const jsonData = document.getElementById('jsonData');
    const jsonSchema = document.getElementById('jsonSchema');
    const validateBtn = document.getElementById('validateBtn');
    const clearBtn = document.getElementById('clearBtn');
    const sampleBtn = document.getElementById('sampleBtn');
    const validationResults = document.getElementById('validationResults');
    const resultContent = document.getElementById('resultContent');

    // Simple JSON Schema validator
    function validateSchema(data, schema, path = '') {
        const errors = [];

        // Check type
        if (schema.type) {
            const actualType = getType(data);
            const expectedTypes = Array.isArray(schema.type) ? schema.type : [schema.type];

            if (!expectedTypes.includes(actualType)) {
                errors.push({
                    path: path || 'root',
                    message: `Expected type "${expectedTypes.join(' or ')}" but got "${actualType}"`
                });
                return errors; // Stop further validation for this path
            }
        }

        // Check required properties
        if (schema.required && Array.isArray(schema.required) && typeof data === 'object' && data !== null) {
            for (const prop of schema.required) {
                if (!(prop in data)) {
                    errors.push({
                        path: path ? `${path}.${prop}` : prop,
                        message: `Required property "${prop}" is missing`
                    });
                }
            }
        }

        // Check properties
        if (schema.properties && typeof data === 'object' && data !== null) {
            for (const [key, propSchema] of Object.entries(schema.properties)) {
                if (key in data) {
                    const propPath = path ? `${path}.${key}` : key;
                    const propErrors = validateSchema(data[key], propSchema, propPath);
                    errors.push(...propErrors);
                }
            }
        }

        // Check array items
        if (schema.items && Array.isArray(data)) {
            data.forEach((item, index) => {
                const itemPath = path ? `${path}[${index}]` : `[${index}]`;
                const itemErrors = validateSchema(item, schema.items, itemPath);
                errors.push(...itemErrors);
            });
        }

        // Check minimum
        if (schema.minimum !== undefined && typeof data === 'number') {
            if (data < schema.minimum) {
                errors.push({
                    path: path || 'root',
                    message: `Value ${data} is less than minimum ${schema.minimum}`
                });
            }
        }

        // Check maximum
        if (schema.maximum !== undefined && typeof data === 'number') {
            if (data > schema.maximum) {
                errors.push({
                    path: path || 'root',
                    message: `Value ${data} is greater than maximum ${schema.maximum}`
                });
            }
        }

        // Check minLength
        if (schema.minLength !== undefined && typeof data === 'string') {
            if (data.length < schema.minLength) {
                errors.push({
                    path: path || 'root',
                    message: `String length ${data.length} is less than minLength ${schema.minLength}`
                });
            }
        }

        // Check maxLength
        if (schema.maxLength !== undefined && typeof data === 'string') {
            if (data.length > schema.maxLength) {
                errors.push({
                    path: path || 'root',
                    message: `String length ${data.length} is greater than maxLength ${schema.maxLength}`
                });
            }
        }

        // Check pattern
        if (schema.pattern && typeof data === 'string') {
            const regex = new RegExp(schema.pattern);
            if (!regex.test(data)) {
                errors.push({
                    path: path || 'root',
                    message: `String does not match pattern "${schema.pattern}"`
                });
            }
        }

        // Check enum
        if (schema.enum && Array.isArray(schema.enum)) {
            if (!schema.enum.includes(data)) {
                errors.push({
                    path: path || 'root',
                    message: `Value must be one of: ${schema.enum.map(v => JSON.stringify(v)).join(', ')}`
                });
            }
        }

        // Check format (basic support)
        if (schema.format && typeof data === 'string') {
            if (schema.format === 'email') {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(data)) {
                    errors.push({
                        path: path || 'root',
                        message: `Invalid email format`
                    });
                }
            } else if (schema.format === 'uri' || schema.format === 'url') {
                try {
                    new URL(data);
                } catch {
                    errors.push({
                        path: path || 'root',
                        message: `Invalid URL format`
                    });
                }
            }
        }

        return errors;
    }

    // Get JSON type
    function getType(value) {
        if (value === null) return 'null';
        if (Array.isArray(value)) return 'array';
        if (typeof value === 'number' && Number.isInteger(value)) return 'integer';
        return typeof value;
    }

    // Validate button handler
    validateBtn.addEventListener('click', function () {
        const dataInput = jsonData.value.trim();
        const schemaInput = jsonSchema.value.trim();

        if (!dataInput || !schemaInput) {
            validationResults.classList.add('active');
            resultContent.innerHTML = '<div class="result-error"><div class="error-header">⚠️ Error</div><p>Please provide both JSON data and JSON Schema</p></div>';
            return;
        }

        try {
            const data = JSON.parse(dataInput);
            const schema = JSON.parse(schemaInput);

            const errors = validateSchema(data, schema);

            validationResults.classList.add('active');

            if (errors.length === 0) {
                resultContent.innerHTML = `
                    <div class="result-success">
                        <span class="icon">✓</span>
                        <div>
                            <strong>Valid!</strong>
                            <p style="margin: 0.5rem 0 0; opacity: 0.9;">JSON data conforms to the schema</p>
                        </div>
                    </div>
                `;
            } else {
                let errorHtml = `
                    <div class="result-error">
                        <div class="error-header">✗ Validation Failed (${errors.length} error${errors.length > 1 ? 's' : ''})</div>
                        <ul class="error-list">
                `;

                errors.forEach(error => {
                    errorHtml += `<li class="error-item"><span class="error-path">${error.path}:</span> ${error.message}</li>`;
                });

                errorHtml += '</ul></div>';
                resultContent.innerHTML = errorHtml;
            }

        } catch (e) {
            validationResults.classList.add('active');
            resultContent.innerHTML = `<div class="result-error"><div class="error-header">⚠️ Parse Error</div><p>${e.message}</p></div>`;
        }
    });

    // Clear button handler
    clearBtn.addEventListener('click', function () {
        jsonData.value = '';
        jsonSchema.value = '';
        validationResults.classList.remove('active');
        resultContent.innerHTML = '';
    });

    // Sample button handler
    sampleBtn.addEventListener('click', function () {
        jsonData.value = JSON.stringify({
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com",
            "role": "developer"
        }, null, 2);

        jsonSchema.value = JSON.stringify({
            "type": "object",
            "required": ["name", "email"],
            "properties": {
                "name": {
                    "type": "string",
                    "minLength": 1
                },
                "age": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 150
                },
                "email": {
                    "type": "string",
                    "format": "email"
                },
                "role": {
                    "type": "string",
                    "enum": ["admin", "developer", "designer", "manager"]
                }
            }
        }, null, 2);
    });
});
