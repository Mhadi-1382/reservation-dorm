let lastSelected = null;

function toggleRadio(radio) {
    if (lastSelected === radio) {
        radio.checked = false; // اگر رادیو باتن دوباره انتخاب شد، آن را غیر فعال کن
        lastSelected = null; // آخرین انتخاب را ریست کن
    } else {
        lastSelected = radio; // آخرین انتخاب را به روز کن
    }
    
}



