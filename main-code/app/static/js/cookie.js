// Cookie alert
document.addEventListener('DOMContentLoaded', function () {
    const cookieBanner = document.getElementById('cookie-banner');
    const acceptCookieButton = document.getElementById('accept-cookie');
    const declineCookieButton = document.getElementById('decline-cookie');

    if (!cookieBanner || !acceptCookieButton || !declineCookieButton) {
        return;
    }

    if (!document.cookie.includes('cookie_accepted=true') && !document.cookie.includes('cookie_declined=true')) {
        cookieBanner.style.display = 'block';
    }

    acceptCookieButton.addEventListener('click', function () {
        const date = new Date();
        date.setFullYear(date.getFullYear() + 1);
        document.cookie = `cookie_accepted=true; expires=${date.toUTCString()}; path=/`;

        cookieBanner.style.display = 'none';
    });

    declineCookieButton.addEventListener('click', function () {
        const date = new Date();
        date.setDate(date.getDate() + 7);
        document.cookie = `cookie_declined=true; expires=${date.toUTCString()}; path=/`;

        cookieBanner.style.display = 'none';
    });
});