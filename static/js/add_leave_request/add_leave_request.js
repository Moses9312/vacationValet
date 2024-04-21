document.addEventListener('DOMContentLoaded', function () {
    function calculateDays() {
        let startDateValue = document.getElementById('id_start_date').value;
        let endDateValue = document.getElementById('id_end_date').value;

        if (startDateValue && endDateValue) {
            let startDate = new Date(startDateValue);
            let endDate = new Date(endDateValue);

            let differenceInTime = endDate.getTime() - startDate.getTime() + (1000 * 3600 * 24);
            let differenceInDays = Math.round(differenceInTime / (1000 * 3600 * 24));

            document.getElementById('days_count').textContent = differenceInDays;
        } else {
            document.getElementById('days_count').textContent = 0;
        }
    }

    if (document.getElementById('id_start_date') && document.getElementById('id_end_date')) {
        document.getElementById('id_start_date').addEventListener('change', calculateDays);
        document.getElementById('id_end_date').addEventListener('change', calculateDays);
    }
});
