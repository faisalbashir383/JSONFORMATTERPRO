// CSV to JSON Web Worker
// Runs entirely in background thread to prevent UI freeze

self.onmessage = function (e) {
    const { csv, options } = e.data;
    const { useHeaders, trimWhitespace, parseNumbers } = options;

    try {
        // Split into lines
        const lines = csv.split(/\r?\n/).filter(line => line.trim());

        if (lines.length === 0) {
            self.postMessage({ error: 'No data found in CSV' });
            return;
        }

        const totalLines = lines.length;

        // Parse CSV line handling quoted fields
        function parseLine(line) {
            const result = [];
            let current = '';
            let inQuotes = false;

            for (let i = 0; i < line.length; i++) {
                const char = line[i];

                if (char === '"') {
                    if (inQuotes && line[i + 1] === '"') {
                        current += '"';
                        i++;
                    } else {
                        inQuotes = !inQuotes;
                    }
                } else if (char === ',' && !inQuotes) {
                    result.push(trimWhitespace ? current.trim() : current);
                    current = '';
                } else {
                    current += char;
                }
            }
            result.push(trimWhitespace ? current.trim() : current);

            return result;
        }

        function parseValue(value) {
            if (!parseNumbers) return value;

            const lowerVal = value.toLowerCase();
            if (lowerVal === 'true') return true;
            if (lowerVal === 'false') return false;
            if (value === '' || lowerVal === 'null') return null;

            if (!isNaN(value) && value !== '') {
                const num = Number(value);
                if (!isNaN(num)) return num;
            }

            return value;
        }

        const data = [];
        const PROGRESS_INTERVAL = 500; // Report progress every 500 rows

        if (useHeaders) {
            const headers = parseLine(lines[0]);

            for (let i = 1; i < lines.length; i++) {
                const values = parseLine(lines[i]);
                const obj = {};

                for (let j = 0; j < headers.length; j++) {
                    obj[headers[j]] = parseValue(values[j] || '');
                }

                data.push(obj);

                // Report progress
                if (i % PROGRESS_INTERVAL === 0) {
                    self.postMessage({
                        progress: Math.round((i / totalLines) * 100),
                        status: `Parsing row ${i} of ${totalLines}...`
                    });
                }
            }
        } else {
            for (let i = 0; i < lines.length; i++) {
                data.push(parseLine(lines[i]).map(parseValue));

                if (i % PROGRESS_INTERVAL === 0) {
                    self.postMessage({
                        progress: Math.round((i / totalLines) * 100),
                        status: `Parsing row ${i} of ${totalLines}...`
                    });
                }
            }
        }

        // Report stringifying
        self.postMessage({
            progress: 95,
            status: 'Formatting JSON output...'
        });

        // Stringify the result
        const jsonString = JSON.stringify(data, null, 2);

        // Send final result
        self.postMessage({
            result: jsonString,
            rowCount: data.length,
            progress: 100
        });

    } catch (error) {
        self.postMessage({ error: error.message });
    }
};
