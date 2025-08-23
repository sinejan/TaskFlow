// Landing page functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth animations
    const cards = document.querySelectorAll('.option-card');
    
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Add click analytics or other functionality if needed
    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Add loading state or analytics here if needed
            console.log('Navigating to:', this.querySelector('.btn').href);
        });
    });
});
