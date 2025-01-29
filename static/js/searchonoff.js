function toggleDateInputs() {
    var roomType = document.getElementById("room_type").value;
    var fromDateInput = document.getElementById("fromDate1");
    var toDateInput = document.getElementById("toDate1");

    if (roomType) {
        fromDateInput.disabled = false;
        toDateInput.disabled = false;
    } else {
        fromDateInput.disabled = true;
        toDateInput.disabled = true;
        

    }
}

// غیرفعال کردن فیلدهای تاریخ در بار اول لود
document.addEventListener("DOMContentLoaded", function() {
    toggleDateInputs(); // این تابع را برای تنظیم اولیه فراخوانی می‌کنیم
});
