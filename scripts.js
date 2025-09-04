/* === FUNCTION DEFINITIONS === */
/* === OTHER CODE === */
/* === EVENT LISTENERS === */
/* === DOM READY === */
document.addEventListener('DOMContentLoaded', function() {
const menuToggle = document.querySelector(".menu-toggle");
        const topNav = document.querySelector(".top-nav");

        if (menuToggle && topNav) {
          menuToggle.addEventListener("click", function () {
            topNav.classList.toggle("open");
            menuToggle.classList.toggle("active");

            // Update aria-expanded for accessibility
            const isExpanded = topNav.classList.contains("open");
            menuToggle.setAttribute("aria-expanded", isExpanded);

const menuToggle = document.querySelector(".menu-toggle");
        const topNav = document.querySelector(".top-nav");

        if (menuToggle && topNav) {
          menuToggle.addEventListener("click", function () {
            topNav.classList.toggle("open");
            // Update aria-expanded attribute
            const isOpen = topNav.classList.contains("open");
            menuToggle.setAttribute("aria-expanded", isOpen);

            // Prevent body scroll when menu is open
            if (isOpen) {
              document.body.style.overflow = "hidden";
            } else {
              document.body.style.overflow = "";
            }

const menuToggle = document.querySelector(".menu-toggle");
        const topNav = document.querySelector(".top-nav");

        if (menuToggle && topNav) {
          menuToggle.addEventListener("click", function () {
            topNav.classList.toggle("open");
            const isOpen = topNav.classList.contains("open");
            menuToggle.setAttribute("aria-expanded", isOpen);

            // Animate hamburger to X
            menuToggle.classList.toggle("active", isOpen);

            if (isOpen) {
              document.body.style.overflow = "hidden";
            } else {
              document.body.style.overflow = "";
            }

});
