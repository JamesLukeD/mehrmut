/* === MOBILE NAVIGATION === */
document.addEventListener("DOMContentLoaded", function () {
  const menuToggle = document.querySelector(".menu-toggle");
  const topNav = document.querySelector(".top-nav");

  if (menuToggle && topNav) {
    menuToggle.addEventListener("click", function () {
      topNav.classList.toggle("open");
      menuToggle.classList.toggle("active");

      // Update aria-expanded for accessibility
      const isExpanded = topNav.classList.contains("open");
      menuToggle.setAttribute("aria-expanded", isExpanded);

      // Prevent body scroll when menu is open
      if (isExpanded) {
        document.body.style.overflow = "hidden";
      } else {
        document.body.style.overflow = "";
      }
    });
  }
});

/* === CAROUSEL FUNCTIONALITY === */
// Main carousel controls
function moveSlide(direction, id) {
  const carousel = document.getElementById(id);
  if (!carousel) return;

  const images = carousel.querySelectorAll(".carousel-images img");
  if (images.length === 0) return;

  let current = Array.from(images).findIndex((img) =>
    img.classList.contains("active")
  );
  if (current === -1) current = 0;

  images[current].classList.remove("active");
  current = (current + direction + images.length) % images.length;
  images[current].classList.add("active");
}

// Auto-carousel with pause on hover
let carouselInterval;
function startCarousel() {
  carouselInterval = setInterval(() => {
    moveSlide(1, "main-carousel");
  }, 5000);
}

function stopCarousel() {
  clearInterval(carouselInterval);
}

// Sponsor carousel
let sponsorIndex = 0;
function moveSponsor(direction) {
  const track = document.getElementById("sponsorTrack");
  if (!track) return;

  const shift = 220;
  const maxIndex = Math.max(0, track.children.length - 3);
  sponsorIndex += direction;
  sponsorIndex = Math.max(0, Math.min(sponsorIndex, maxIndex));
  track.style.transform = `translateX(-${sponsorIndex * shift}px)`;
}

/* === EVENT LISTENERS === */
document.addEventListener("DOMContentLoaded", function () {
  // Initialize carousel auto-play
  const mainCarousel = document.getElementById("main-carousel");
  if (mainCarousel) {
    startCarousel();

    // Pause on hover
    mainCarousel.addEventListener("mouseenter", stopCarousel);
    mainCarousel.addEventListener("mouseleave", startCarousel);
  }

  // Keyboard navigation
  document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") {
      moveSlide(-1, "main-carousel");
    } else if (e.key === "ArrowRight") {
      moveSlide(1, "main-carousel");
    }
  });

  // Intersection Observer for animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  // Observe elements for animation
  const animatedElements = document.querySelectorAll(
    ".team-member, .project-card, .support-block"
  );
  animatedElements.forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(20px)";
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    observer.observe(el);
  });
});

/* === ERROR HANDLING === */
function handleImageError(img) {
  img.style.display = "none";
  console.log("Image failed to load:", img.src);
}
