document.addEventListener('DOMContentLoaded', function () {
    // Funcție pentru actualizarea atributului 'min' al campului end_date
    function updateEndDateMin() {
        document.getElementById('id_end_date').min = document.getElementById('id_start_date').value;
    }

    // Functie pentru calculul zilelor
    function calculateDays() {
        let startDateValue = document.getElementById('id_start_date').value;
        let endDateValue = document.getElementById('id_end_date').value;

        if (startDateValue && endDateValue) {
            let startDate = new Date(startDateValue);
            let endDate = new Date(endDateValue);

            let differenceInTime = endDate.getTime() - startDate.getTime() + (1000 * 3600 * 24);
            document.getElementById('days_count').textContent = Math.round(differenceInTime / (1000 * 3600 * 24));
        } else {
            document.getElementById('days_count').textContent = 0;
        }
    }

    // Functie pentru afisarea sau ascunderea campului "Attachment" in functie de type (Daca type = CO sa fie ascuns)
    function showOrHideAttachmentField() {
        let typeField = document.getElementById('id_type');
        let attachmentLabel = document.querySelector('label[for="id_attachment"]');
        let attachmentField = document.getElementById('id_attachment');

        if (typeField.value === 'co') {
            attachmentLabel.style.display = 'none';
            attachmentField.style.display = 'none';
        } else {
            attachmentLabel.style.display = 'block';
            attachmentField.style.display = 'block';
        }
    }

    // Ascultam evenimentul de schimbare in campul tip care determina ascunderea campului de atasament si a etichetei
    document.getElementById('id_type').addEventListener('change', showOrHideAttachmentField);

    // La încarcarea paginii, apelam functia pentru a asigura afișarea corecta a campului de atasament si a etichetei
    showOrHideAttachmentField();

    // Event de schimbare în campul start_date pentru a actualiza min in end_date și pentru a calcula zilele
    document.getElementById('id_start_date').addEventListener('change', function () {
        updateEndDateMin();
        calculateDays();
    });

    //  Event de schimbare in campurile start_date si end_date pentru a calcula zilele
    if (document.getElementById('id_start_date') && document.getElementById('id_end_date')) {
        document.getElementById('id_end_date').addEventListener('change', calculateDays);
    }
});
