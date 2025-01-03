const modal = () => {
  const modalContainers = document.querySelectorAll(".modal-container");

  if (!modalContainers.length) {
    return;
  }

  modalContainers.forEach((modalContainer) => {
    const body = document.body;
    const bodyStyle = body.style;
    const modals = modalContainer.querySelectorAll(".modal");

    modals?.forEach((modal, idx) => {
      const modalOpens = modalContainer.querySelectorAll(
        `[data-modal-index="${idx + 1}"]`
      );

      const modalContent = modal.querySelector(".modal-content");
      const modalCloses = modal.querySelectorAll(".modal-close");
      //  open modal
      modalOpens.forEach((modalOpen) => {
        modalOpen.addEventListener("click", () => {
          modal.style.display = "block";
          bodyStyle.overflow = "hidden";
          bodyStyle.paddingRight = "17px";

          setTimeout(() => {
            // uncomment if you need  body to be scroll down with modal open
            // window.scroll({ top: window.scrollY - 100, behavior: "smooth" });
            modal.style.opacity = 100;
            modal.style.visibility = "visible";
            modal.scrollTop = 0;
            modalContent.style.transform = "translateY(0px)";
          }, 10);
        });
      });
      //  close modal
      modalCloses.forEach((modalClose) => {
        modalClose.addEventListener("click", function () {
          modal.style.opacity = 0;
          modal.style.visibility = "hidden";
          modalContent.style.transform = `translateY(-${80}px)`;

          setTimeout(() => {
            modal.style.display = "none";
            bodyStyle.overflow = "auto";
            bodyStyle.paddingRight = 0;
          }, 500);
        });
      });
    });
  });
};
