
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
          });
        }
      });
    

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
          });
        }
      });
    

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
          });
        }
      });
    

      // MAIN CAROUSEL
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

      // AUTO-CAROUSEL with pause on hover
      let carouselInterval;
      function startCarousel() {
        carouselInterval = setInterval(() => {
          moveSlide(1, "main-carousel");
        }, 5000);
      }

      function stopCarousel() {
        clearInterval(carouselInterval);
      }

      // SPONSOR CAROUSEL
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

      // KEYBOARD NAVIGATION
      document.addEventListener("keydown", (e) => {
        if (e.key === "ArrowLeft") {
          moveSlide(-1, "main-carousel");
        } else if (e.key === "ArrowRight") {
          moveSlide(1, "main-carousel");
        }
      });

      // INTERSECTION OBSERVER FOR ANIMATIONS
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

      // IMAGE LOADING ERROR HANDLING
      function handleImageError(img) {
        img.style.display = "none";
        console.warn("Image failed to load:", img.src);
      }

      document.addEventListener("DOMContentLoaded", () => {
        // Start carousel
        startCarousel();

        // Pause carousel on hover
        const carousel = document.getElementById("main-carousel");
        if (carousel) {
          carousel.addEventListener("mouseenter", stopCarousel);
          carousel.addEventListener("mouseleave", startCarousel);
        }

        // Add fade-in animation to elements
        const animateElements = document.querySelectorAll(
          ".team-member, .project-card, .support-block"
        );
        animateElements.forEach((el) => {
          el.style.opacity = "0";
          el.style.transform = "translateY(20px)";
          el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
          observer.observe(el);
        });

        // Add error handling to images and lazy loading
        const images = document.querySelectorAll("img");
        images.forEach((img) => {
          img.addEventListener("error", () => handleImageError(img));
          img.addEventListener("load", () => {
            img.classList.add("loaded");
          });
          // Set loading attribute if not already set
          if (!img.hasAttribute("loading")) {
            img.loading = "lazy";
          }
        });

        // Mobile Navigation Toggle
        const menuToggle = document.querySelector(".menu-toggle");
        const topNav = document.querySelector(".top-nav");

        if (menuToggle && topNav) {
          console.log("Navigation elements found"); // Debug

          menuToggle.addEventListener("click", function () {
            console.log("Menu toggle clicked"); // Debug
            topNav.classList.toggle("open");
            // Update aria-expanded attribute
            const isOpen = topNav.classList.contains("open");
            menuToggle.setAttribute("aria-expanded", isOpen);

            console.log("Menu is now:", isOpen ? "open" : "closed"); // Debug

            // Animate hamburger to X
            menuToggle.classList.toggle("active", isOpen);

            // Prevent body scroll when menu is open
            if (isOpen) {
              document.body.style.overflow = "hidden";
            } else {
              document.body.style.overflow = "";
            }
          });

          // Close menu when clicking outside
          document.addEventListener("click", function (e) {
            if (!menuToggle.contains(e.target) && !topNav.contains(e.target)) {
              topNav.classList.remove("open");
              menuToggle.classList.remove("active");
              menuToggle.setAttribute("aria-expanded", "false");
              document.body.style.overflow = "";
            }
          });

          // Close menu on escape key
          document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && topNav.classList.contains("open")) {
              topNav.classList.remove("open");
              menuToggle.classList.remove("active");
              menuToggle.setAttribute("aria-expanded", "false");
              document.body.style.overflow = "";
              menuToggle.focus();
            }
          });
        }
      });
    
moveSlide(-1, 
moveSlide(1, 
moveSponsor(-1)
moveSponsor(1)

      // Mobile Navigation Toggle
      document.addEventListener("DOMContentLoaded", function () {
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
          });

          // Close menu when clicking outside
          document.addEventListener("click", function (e) {
            if (!menuToggle.contains(e.target) && !topNav.contains(e.target)) {
              topNav.classList.remove("open");
              menuToggle.setAttribute("aria-expanded", "false");
              document.body.style.overflow = "";
            }
          });

          // Close menu on escape key
          document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && topNav.classList.contains("open")) {
              topNav.classList.remove("open");
              menuToggle.setAttribute("aria-expanded", "false");
              document.body.style.overflow = "";
              menuToggle.focus();
            }
          });
        }
      });
    

      // Mobile Navigation Toggle
      document.addEventListener("DOMContentLoaded", function () {
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

          document.addEventListener("click", function (e) {
            if (!menuToggle.contains(e.target) && !topNav.contains(e.target)) {
              topNav.classList.remove("open");
              menuToggle.classList.remove("active");
              menuToggle.setAttribute("aria-expanded", "false");
              document.body.style.overflow = "";
            }
          });

          document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && topNav.classList.contains("open")) {
              topNav.classList.remove("open");
              menuToggle.classList.remove("active");
              menuToggle.setAttribute("aria-expanded", "false");
              document.body.style.overflow = "";
              menuToggle.focus();
            }
          });
        }
      });
    

      // Mobile Navigation Toggle
      document.addEventListener("DOMContentLoaded", function () {
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

          document.addEventListener("click", function (e) {
            if (!menuToggle.contains(e.target) && !topNav.contains(e.target)) {
              topNav.classList.remove("open");
              menuToggle.classList.remove("active");
              menuToggle.setAttribute("aria-expanded", "false");
              document.body.style.overflow = "";
            }
          });

          document.addEventListener("keydown", function (e) {
            if (e.key === "Escape" && topNav.classList.contains("open")) {
              topNav.classList.remove("open");
              menuToggle.classList.remove("active");
              menuToggle.setAttribute("aria-expanded", "false");
              document.body.style.overflow = "";
              menuToggle.focus();
            }
          });
        }
      });
    

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
          });
        }
      });
    

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
          });
        }
      });
    
