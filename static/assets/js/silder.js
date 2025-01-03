const silder = () => {
  const swiperElement = document.querySelector(".swiper");
  if (swiperElement) {
    // swiper slider
    var swiper = new Swiper(".primary-slider", {
      slidesPerView: 1,
      effect: "fade",
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });

    // hero2  slider
    var swiperThumbs = new Swiper(".hero-slider2-tumbs_slider", {
      loop: true,
      spaceBetween: 10,
      slidesPerView: 3,
      speed: 800,

      // freeMode: true,
      watchSlidesProgress: true,
      breakpoints: {
        1600: {
          spaceBetween: 20,
        },
      },
    });
    var swiper1 = new Swiper(".hero-slider2", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },

      thumbs: {
        swiper: swiperThumbs,
      },
    });

    // featured apartments slider
    var swiper = new Swiper(".featured-apartments-slider", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        1200: {
          slidesPerView: 3,
        },
        1800: {
          slidesPerView: 4,
        },
      },
    });
   
    // featured apartments slider2
    var swiper = new Swiper(".featured-apartments-slider2", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
      },
    });
    // testimonials slider
    var swiper = new Swiper(".testimonials-slider", {
      slidesPerView: 1,

      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
      },
    });
    // testimonials2 slider
    var swiper = new Swiper(".testimonials-slider2", {
      slidesPerView: 1,

      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
        },
      },
    });
    // testimonials 3 slider
    const testimonials3ThumbsSlider = new Swiper(
      ".testimonials3-tumbs_slider",
      {
        slidesPerView: "auto",
        cssMode: true,
        preventClicks: false,
      }
    );
    const testimonialsSlider3 = new Swiper(".testimonials-slider-3", {
      slidesPerView: 1,
      loop: true,
      speed: 1500,
      effect: "fade",

      autoplay: {
        delay: 5000,
        disableOnInteraction: false,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },

      thumbs: {
        swiper: testimonials3ThumbsSlider,
      },
    });
    // testimonials 4 slider
    var testimonialsSlider4 = new Swiper(".testimonials-slider-4", {
      slidesPerView: 1,
      loop: true,
      speed: 800,

      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        1200: {
          slidesPerView: 3,
        },
      },
    });

    const testimonialQuoteMenus = document.querySelectorAll(
      ".testimonial-quote-menu"
    );
    // random thumb menu

    if (testimonialQuoteMenus?.length) {
      testimonialQuoteMenus.forEach((quoteMenu, idx) => {
        const menuContainer = quoteMenu.closest(
          ".testimonial-quote-menu-container"
        );

        const quoteMenu2 = quoteMenu;
        let innerHtmlogQuoteMenu2 = "";
        let ul = document.createElement("ul");

        ul.classList.add("testimonial-quote-menu", "testimonial-quote-menu2");

        quoteMenu2.querySelectorAll("li").forEach((li2) => {
          innerHtmlogQuoteMenu2 += `<li>${li2.innerHTML}</li>`;
        });
        ul.innerHTML = innerHtmlogQuoteMenu2;
        if (menuContainer) {
          menuContainer.appendChild(ul);
        }
      });
      const menuCopy = document.querySelector(".testimonial-quote-menu2");

      // add active class to animatable image
      const isActive = (cs) => {
        menuCopy.style.zIndex = 20;
        menuCopy.querySelectorAll("li").forEach((li, idx) => {
          li.classList.remove("active");
          if (cs === idx) {
            li.classList.add("active");
          }

          setTimeout(() => {
            li.classList.remove("active");
            menuCopy.style.zIndex = 1;
          }, 300);
        });
      };

      testimonialsSlider3.eventsListeners.activeIndexChange[0] = (e) => {
        if (
          testimonialsSlider3.realIndex !==
          testimonialsSlider3.previousRealIndex
        ) {
          isActive(testimonialsSlider3.realIndex);
        }
      };
    }

    // news slider
    var swiper = new Swiper(".news-slider", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        1200: {
          slidesPerView: 3,
        },
      },
    });
    // news single slider
    var swiper = new Swiper(".news-single-slider", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
    });

    // properties slider
    var swiper = new Swiper(".properties-slider", {
      slidesPerView: 1,

      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
      },
    });
    // upcoming projects slider
    var swiper = new Swiper(".project-slider-container", {
      slidesPerView: 1,

      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });
    // neighbour slider
    var neighbourswiperThumbs = new Swiper(".neighbour-slider-tumbs_slider", {
      loop: true,
      spaceBetween: 8,
      slidesPerView: 3,
      freeMode: true,
      watchSlidesProgress: true,
    });
    var swiper = new Swiper(".neighbour-slider", {
      slidesPerView: 1,
      speed: 800,

      effect: "fade",
      thumbs: {
        swiper: neighbourswiperThumbs,
      },
    });
    // brands slider
    var swiper = new Swiper(".brand-slider", {
      slidesPerView: 2,
      spaceBetween: 30,
      speed: 800,
      loop: true,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      breakpoints: {
        576: {
          slidesPerView: 3,
        },
        768: {
          slidesPerView: 4,
        },
        992: {
          slidesPerView: 5,
        },
      },
    });

    // portfolio slider
    var swiper = new Swiper(".portfolio-slider", {
      slidesPerView: 1,

      loop: true,
      speed: 800,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        576: {
          slidesPerView: 2,
        },
        992: {
          slidesPerView: 3,
        },
        1200: {
          slidesPerView: 4,
        },
      },
    });
    // popular properties slider
    var swiper = new Swiper(".popular-properties-slider", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      autoplay: {
        delay: 5000,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });
    // product details slider
    var swiper = new Swiper(".product-details-slider", {
      slidesPerView: 1,
      loop: true,
      speed: 800,
      preventClicksPropagation: false,
      centeredSlides: true,
      autoplay: {
        delay: 10000,
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      breakpoints: {
        768: {
          slidesPerView: 1.6,
        },
        992: {
          slidesPerView: 1.55,
        },

        1600: {
          slidesPerView: 1.9,
        },
      },
    });
  }
};


