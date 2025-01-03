const service = () => {
  const serviceCards = document.querySelectorAll(".service-cards");
  if (serviceCards?.length) {
    serviceCards.forEach((serviceCardsSingle) => {
      const allServiceCards =
        serviceCardsSingle.querySelectorAll(".service-card");

      allServiceCards.forEach((serviceCard, idx) => {
        serviceCard.addEventListener("mouseenter", function () {
          allServiceCards.forEach((serviceCard) => {
            serviceCard.classList.remove("active");
          });

          this.classList.add("active");
        });
      });
    });
  }
};
