// show the scroll-to-top button when scrolling down
window.onscroll = function () {
    toggleScrollToTopButton();
};

function toggleScrollToTopButton() {
    const scrollToTopButton = document.getElementById("scrollToTop");

    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        scrollToTopButton.style.display = "flex";
    } else {
        scrollToTopButton.style.display = "none";
    }
}

// scroll to the top of the page when the button is clicked
document.getElementById("scrollToTop").onclick = function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
};