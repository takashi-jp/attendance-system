document.addEventListener('DOMContentLoaded', () => {
    const checkInButton = document.getElementById('checkInButton');
    const checkOutButton = document.getElementById('checkOutButton');

    if (checkInButton) {
        checkInButton.addEventListener('click', () => {
            alert('出勤を記録しました');
        });
    }

    if (checkOutButton) {
        checkOutButton.addEventListener('click', () => {
            alert('退勤を記録しました');
        });
    }
});
