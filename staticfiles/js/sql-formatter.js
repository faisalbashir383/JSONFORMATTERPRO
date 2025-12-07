/**
 * SQL Formatter - Client-side JavaScript
 * Basic SQL formatting without external libraries
 */

document.addEventListener('DOMContentLoaded', function () {
    const inputSql = document.getElementById('inputSql');
    const outputSql = document.getElementById('outputSql');
    const formatBtn = document.getElementById('formatBtn');
    const sampleBtn = document.getElementById('sampleBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const indentSize = document.getElementById('indentSize');
    const keywordCase = document.getElementById('keywordCase');

    const sampleQuery = `select u.id, u.name, u.email, o.order_id, o.total from users u inner join orders o on u.id = o.user_id where u.active = 1 and o.created_at > '2024-01-01' order by o.created_at desc limit 100`;

    const SQL_KEYWORDS = [
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'NOT', 'IN', 'LIKE', 'BETWEEN',
        'JOIN', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'OUTER JOIN', 'FULL JOIN',
        'ON', 'AS', 'ORDER BY', 'GROUP BY', 'HAVING', 'LIMIT', 'OFFSET',
        'INSERT INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE FROM',
        'CREATE TABLE', 'ALTER TABLE', 'DROP TABLE', 'TRUNCATE',
        'PRIMARY KEY', 'FOREIGN KEY', 'REFERENCES', 'INDEX', 'UNIQUE',
        'NULL', 'NOT NULL', 'DEFAULT', 'AUTO_INCREMENT',
        'UNION', 'UNION ALL', 'EXCEPT', 'INTERSECT',
        'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
        'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'DISTINCT',
        'ASC', 'DESC', 'IS', 'EXISTS', 'ALL', 'ANY'
    ];

    // Keywords that start new lines
    const LINE_BREAK_KEYWORDS = [
        'SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'ORDER BY', 'GROUP BY', 'HAVING',
        'LIMIT', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'OUTER JOIN', 'FULL JOIN', 'JOIN',
        'INSERT INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE FROM',
        'UNION', 'UNION ALL', 'EXCEPT', 'INTERSECT'
    ];

    formatBtn.addEventListener('click', formatSQL);

    sampleBtn.addEventListener('click', function () {
        inputSql.value = sampleQuery;
    });

    clearBtn.addEventListener('click', function () {
        inputSql.value = '';
        outputSql.value = '';
    });

    copyBtn.addEventListener('click', function () {
        navigator.clipboard.writeText(outputSql.value).then(() => {
            copyBtn.textContent = '✅ Copied!';
            setTimeout(() => {
                copyBtn.textContent = '📋 Copy';
            }, 2000);
        });
    });

    function formatSQL() {
        let sql = inputSql.value.trim();
        if (!sql) {
            outputSql.value = '';
            return;
        }

        const indent = indentSize.value === 'tab' ? '\t' : ' '.repeat(parseInt(indentSize.value));
        const caseType = keywordCase.value;

        // Normalize whitespace
        sql = sql.replace(/\s+/g, ' ').trim();

        // Apply keyword casing
        if (caseType !== 'preserve') {
            SQL_KEYWORDS.forEach(keyword => {
                const regex = new RegExp('\\b' + keyword.replace(/ /g, '\\s+') + '\\b', 'gi');
                const replacement = caseType === 'upper' ? keyword.toUpperCase() : keyword.toLowerCase();
                sql = sql.replace(regex, replacement);
            });
        }

        // Add line breaks before keywords
        LINE_BREAK_KEYWORDS.forEach(keyword => {
            const kw = caseType === 'lower' ? keyword.toLowerCase() : keyword.toUpperCase();
            const regex = new RegExp('\\s+(' + kw.replace(/ /g, '\\s+') + ')\\b', 'gi');
            sql = sql.replace(regex, '\n$1');
        });

        // Format the output with indentation
        let lines = sql.split('\n');
        let formatted = [];
        let indentLevel = 0;

        lines.forEach(line => {
            line = line.trim();
            if (!line) return;

            // Decrease indent for certain keywords
            const upperLine = line.toUpperCase();
            if (upperLine.startsWith('FROM') || upperLine.startsWith('WHERE') ||
                upperLine.startsWith('ORDER') || upperLine.startsWith('GROUP') ||
                upperLine.startsWith('HAVING') || upperLine.startsWith('LIMIT')) {
                // Keep at base level
                formatted.push(line);
            } else if (upperLine.startsWith('AND') || upperLine.startsWith('OR')) {
                // Indent these
                formatted.push(indent + line);
            } else if (upperLine.includes('JOIN')) {
                // Joins at base level
                formatted.push(line);
            } else if (upperLine.startsWith('SELECT')) {
                formatted.push(line);
            } else {
                formatted.push(line);
            }
        });

        // Format SELECT columns
        let result = formatted.join('\n');

        // Format comma-separated items in SELECT
        result = result.replace(/(SELECT\s+)(.+?)(\s+FROM)/gis, function (match, select, columns, from) {
            const cols = columns.split(',').map(c => c.trim());
            if (cols.length > 2) {
                return select + '\n' + indent + cols.join(',\n' + indent) + '\n' + from.trim();
            }
            return match;
        });

        outputSql.value = result;
    }
});
