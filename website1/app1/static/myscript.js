// document.getElementById("demo").innerHTML = "django page";
// document.getElementById("demo").style.color = "orange"; 
document.addEventListener("DOMContentLoaded", function () {
    // Example: Add click event to each category link
    const categoryLinks = document.querySelectorAll('.category-link');
    categoryLinks.forEach(link => {
        link.addEventListener('click', function () {
            console.log('Category clicked:', this.querySelector('h4').innerText);
        });
    });
});
