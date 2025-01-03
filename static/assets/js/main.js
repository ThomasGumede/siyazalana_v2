

// sticky hedder
stickystickyHeader();

// search controller
search();

// mobile menu
drawer();

// accordion
accordions();

// slider js
silder();

// counter up
const counters = document.querySelectorAll(".counter");
counters.forEach((counter) => {
  new countUp(counter);
});

// service cards
service();

// nice select
const selects = document.querySelectorAll(".selectize");
if (selects?.length) {
  selects.forEach((select) => NiceSelect.bind(select));
}

// quick view modal
modal();

// tab
tabsController();

//glightbox
GLightbox({
  touchNavigation: true,
  loop: true,
  autoplayVideos: false,
  selector: ".glightbox",
  slideEffect: "fade",
  videosWidth: "800px",
});
GLightbox({
  touchNavigation: true,
  loop: true,
  autoplayVideos: false,
  selector: ".glightbox2",
  slideEffect: "fade",
  videosWidth: "800px",
});
GLightbox({
  touchNavigation: true,
  loop: true,
  autoplayVideos: false,
  selector: ".glightbox3",
  slideEffect: "fade",
  videosWidth: "800px",
});

// scrollUp
scrollUp();

// smooth scroll
smoothScroll();

// appart card hover action

const apartCards = document.querySelectorAll(".apart-card");

if (apartCards?.length) {
  apartCards.forEach((apartCard, idx) => {
    apartCard.addEventListener("mouseenter", () => {
      apartCard.querySelector(".card-quick-area").classList.add("active");
    
    });
  });
}

// isotop filters
filter();

// nice checkbox
nice_checkbox();

// count input
count();

// countdown
const countContainers = document.querySelectorAll(".countdown");
if (countContainers?.length) {
  countDown();
}

// price slider
const range_sliders = document.querySelectorAll(".slider-range");

if (range_sliders?.length) {
  
  $(".slider-range").slider({
    range: true,
    min: 50,
    max: 5000,
    values: [50, 1500],
    slide: function (event, ui) {
      $(".amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
    },
  });
  $(".amount").val(
    "$" +
      $(".slider-range").slider("values", 0) +
      " - $" +
      $(".slider-range").slider("values", 1)
  );
}

// price
document.querySelector('.swiper-button-next').innerHTML = ''
document.querySelector('.swiper-button-prev').innerHTML = ''
document.querySelector('.swiper-button-next').innerHTML = '<i class="fas fa-arrow-right"></i>'
document.querySelector('.swiper-button-prev').innerHTML = '<i class="fas fa-arrow-left"></i>'