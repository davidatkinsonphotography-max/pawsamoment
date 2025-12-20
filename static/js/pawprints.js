// Paw Prints Animation Script
// This script creates random paw prints on desktop/tablet screens

document.addEventListener("DOMContentLoaded", function() {
    // Only run on Desktop/Tablet
    if (window.innerWidth > 768) {
        const pawImages = ['paw1.png', 'paw2.png', 'paw3.png', 'paw4.png'];
        const container = document.body;
        
        // Configuration
        const startY = 200; // Start 600px down to clear the Hero section
        const spacing = 400; // Average distance between paws vertically
        const pageHeight = Math.max(container.scrollHeight, container.offsetHeight);
        
        // Calculate how many pairs we need based on page length
        // (Page height minus hero start) divided by spacing
        const iterations = Math.floor((pageHeight - startY) / spacing);

        for (let i = 0; i < iterations; i++) {
            // Create a Left Paw and a Right Paw for every 'row'
            ['left', 'right'].forEach(side => {
                const paw = document.createElement('img');
                const randomImg = pawImages[Math.floor(Math.random() * pawImages.length)];
                
                paw.src = `/static/img/${randomImg}`;
                paw.style.position = 'absolute';
                paw.style.width = '180px'; // Slightly smaller to ensure they don't crowd
                paw.style.opacity = '0.8';   // Adjusted for visibility
                paw.style.zIndex = '1';    // Behind text, but can be adjusted
                paw.style.pointerEvents = 'none';

                // Horizontal placement (Stay in the outer 10% gutters)
                const horizontalPos = (side === 'left') 
                    ? (Math.random() * 5 + 2)  // 2% to 7%
                    : (Math.random() * 5 + 90); // 90% to 95%
                
                // Vertical placement (startY + current row + slight random jitter)
                const jitter = Math.random() * 200; 
                const verticalPos = startY + (i * spacing) + jitter;

                // Stop placing if we are getting too close to the footer
                if (verticalPos < (pageHeight - 400)) {
                    paw.style.left = horizontalPos + '%';
                    paw.style.top = verticalPos + 'px'; // Using PX because it's absolute
                    paw.style.transform = `rotate(${Math.random() * 360}deg)`;
                    container.appendChild(paw);
                }
            });
        }
    }
});

