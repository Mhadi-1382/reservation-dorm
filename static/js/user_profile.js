function openMainTab(evt, cityName) {
    var i, tabContents, navLinks;

    // Hide all main tab contents
    tabContents = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove("active");
    }

    // Remove active class from all main nav links
    navLinks = document.querySelectorAll('.nav-tabs .nav-link');
    navLinks.forEach(link => link.classList.remove('active'));

    // Show the current main tab and add an "active" class to the clicked link
    document.getElementById(cityName).classList.add("active");
    evt.currentTarget.classList.add("active");

    // Reset nested tabs when switching main tabs
    resetNestedTabs(cityName);
}

function openNestedTab(evt, nestedTabName) {
    var i, nestedContents, nestedLinks;

    // Hide all nested tab contents
    nestedContents = document.querySelectorAll('#profile .tab-content');
    for (i = 0; i < nestedContents.length; i++) {
        nestedContents[i].classList.remove("active");
    }

    // Remove active class from all nested nav links
    nestedLinks = document.querySelectorAll('.vertical-tabs .nav-link');
    nestedLinks.forEach(link => link.classList.remove('active'));

    // Show the current nested tab and add an "active" class to the clicked link
    document.getElementById(nestedTabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}

function resetNestedTabs(cityName) {
   if (cityName === 'profile') {
       // Show first nested tab by default
       const firstNestedButton = document.querySelector('.vertical-tabs .nav-link');
       if (firstNestedButton) firstNestedButton.click();
   }
}

// Open default main tab on page load
document.addEventListener("DOMContentLoaded", function() {
   document.querySelector(".nav-tabs .nav-link.active").click();
});

// انتخاب المان "اطلاعات کاربری"
var profileDetailsTab = document.getElementById("profile-details");

// اضافه کردن کلاس "blue-border" هنگام کلیک بر روی تب "اطلاعات کاربری"
profileDetailsTab.addEventListener("click", function() {
    profileDetailsTab.classList.add("blue-border");
});

// حذف کلاس "blue-border" هنگامی که تب "اطلاعات کاربری" غیرفعال می‌شود
profileDetailsTab.addEventListener("blur", function() {
    profileDetailsTab.classList.remove("blue-border");
});