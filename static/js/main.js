// Switch between desktop and mobile images based on screen size
function updateImages() {
    const isMobile = window.innerWidth <= 768;
    const buttons = document.querySelectorAll('.action-button');
    
    buttons.forEach(button => {
        const desktopImages = button.querySelectorAll('.desktop-img');
        const mobileImages = button.querySelectorAll('.mobile-img');
        
        if (isMobile) {
            desktopImages.forEach(img => img.style.setProperty('display', 'none', 'important'));
            mobileImages.forEach(img => img.style.setProperty('display', 'block', 'important'));
        } else {
            desktopImages.forEach(img => img.style.setProperty('display', 'block', 'important'));
            mobileImages.forEach(img => img.style.setProperty('display', 'none', 'important'));
        }
    });
}

// Scroll detection for navigation bar
function handleNavScroll() {
    const nav = document.querySelector('nav');
    if (!nav) return;
    
    const currentScroll = window.pageYOffset || window.scrollY;
    
    if (currentScroll > 100) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    updateImages();
    handleNavScroll();
});

// Update on scroll
window.addEventListener('scroll', handleNavScroll);

// Update on resize
window.addEventListener('resize', updateImages);


function checkOther(selectElement, divId) {
    const otherDiv = document.getElementById(divId);
    const otherInput = otherDiv.querySelector('input, textarea');
    
    if (selectElement.value === "Other") {
        otherDiv.style.display = 'block';
        if (otherInput) otherInput.setAttribute('required', 'true');
    } else {
        otherDiv.style.display = 'none';
        if (otherInput) {
            otherInput.removeAttribute('required');
            otherInput.value = ""; // Clear the text if they change their mind
        }
    }
}
