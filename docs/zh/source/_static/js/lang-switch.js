function switchLang(lang) {
    // Hide all language divs
    document.querySelectorAll('.lang-en, .lang-zh').forEach(el => {
        el.style.display = 'none';
    });
    
    // Show selected language
    document.querySelectorAll(`.lang-${lang}`).forEach(el => {
        el.style.display = 'block';
    });
    
    // Update button states
    document.querySelectorAll('.lang-switch button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`.lang-switch button[onclick="switchLang('${lang}')"]`).classList.add('active');
}

// Initialize with English
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.lang-switch button')) switchLang('en');
});
