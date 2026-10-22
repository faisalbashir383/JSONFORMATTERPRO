/**
 * Cron Expression Builder - Client-side JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
    const minuteSelect = document.getElementById('minute');
    const hourSelect = document.getElementById('hour');
    const daySelect = document.getElementById('day');
    const monthSelect = document.getElementById('month');
    const weekdaySelect = document.getElementById('weekday');

    const cronExpression = document.getElementById('cronExpression');
    const cronDescription = document.getElementById('cronDescription');
    const copyBtn = document.getElementById('copyBtn');

    // Update cron when selects change
    [minuteSelect, hourSelect, daySelect, monthSelect, weekdaySelect].forEach(select => {
        select.addEventListener('change', updateCron);
    });

    // Preset buttons
    document.querySelectorAll('.preset-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const cron = this.dataset.cron;
            const parts = cron.split(' ');
            if (parts.length === 5) {
                setSelectValue(minuteSelect, parts[0]);
                setSelectValue(hourSelect, parts[1]);
                setSelectValue(daySelect, parts[2]);
                setSelectValue(monthSelect, parts[3]);
                setSelectValue(weekdaySelect, parts[4]);
                updateCron();
            }
        });
    });

    // Copy button
    copyBtn.addEventListener('click', function () {
        navigator.clipboard.writeText(cronExpression.textContent).then(() => {
            copyBtn.textContent = '✅ Copied!';
            setTimeout(() => {
                copyBtn.textContent = '📋 Copy Expression';
            }, 2000);
        });
    });

    function setSelectValue(select, value) {
        // Try to find exact match
        for (let i = 0; i < select.options.length; i++) {
            if (select.options[i].value === value) {
                select.selectedIndex = i;
                return;
            }
        }
        // Default to first option (*)
        select.selectedIndex = 0;
    }

    function updateCron() {
        const minute = minuteSelect.value;
        const hour = hourSelect.value;
        const day = daySelect.value;
        const month = monthSelect.value;
        const weekday = weekdaySelect.value;

        const cron = `${minute} ${hour} ${day} ${month} ${weekday}`;
        cronExpression.textContent = cron;

        // Update display values
        document.getElementById('minuteValue').textContent = minute;
        document.getElementById('hourValue').textContent = hour;
        document.getElementById('dayValue').textContent = day;
        document.getElementById('monthValue').textContent = month;
        document.getElementById('weekdayValue').textContent = weekday;

        // Generate description
        cronDescription.textContent = describeCron(minute, hour, day, month, weekday);
    }

    function describeCron(minute, hour, day, month, weekday) {
        let desc = '';

        // Special common cases
        if (minute === '*' && hour === '*' && day === '*' && month === '*' && weekday === '*') {
            return 'Every minute';
        }
        if (minute === '0' && hour === '*' && day === '*' && month === '*' && weekday === '*') {
            return 'Every hour at minute 0';
        }
        if (minute === '0' && hour === '0' && day === '*' && month === '*' && weekday === '*') {
            return 'Every day at midnight';
        }

        // Build description
        let parts = [];

        // Minute
        if (minute === '*') {
            parts.push('Every minute');
        } else if (minute.startsWith('*/')) {
            parts.push(`Every ${minute.slice(2)} minutes`);
        } else {
            parts.push(`At minute ${minute}`);
        }

        // Hour
        if (hour !== '*') {
            if (hour.startsWith('*/')) {
                parts.push(`every ${hour.slice(2)} hours`);
            } else {
                const h = parseInt(hour);
                const ampm = h >= 12 ? 'PM' : 'AM';
                const h12 = h % 12 || 12;
                parts.push(`at ${h12}:00 ${ampm}`);
            }
        }

        // Day of month
        if (day !== '*') {
            if (day === 'L') {
                parts.push('on the last day of the month');
            } else {
                parts.push(`on day ${day}`);
            }
        }

        // Month
        if (month !== '*') {
            const months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            if (month.startsWith('*/')) {
                parts.push(`every ${month.slice(2)} months`);
            } else {
                parts.push(`in ${months[parseInt(month)] || month}`);
            }
        }

        // Day of week
        if (weekday !== '*') {
            const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            if (weekday === '1-5') {
                parts.push('on weekdays');
            } else if (weekday === '0,6') {
                parts.push('on weekends');
            } else {
                parts.push(`on ${days[parseInt(weekday)] || weekday}`);
            }
        }

        return parts.join(' ');
    }

    // Initial update
    updateCron();
});
