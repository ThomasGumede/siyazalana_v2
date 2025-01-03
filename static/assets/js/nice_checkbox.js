const nice_checkbox = () => {
  const allChecboxItems = document.querySelectorAll(".checkbox-item");

  if (allChecboxItems?.length) {
    allChecboxItems.forEach((checkboxItem, idx) => {
      const checkbox = checkboxItem.querySelector("input[type='checkbox']");

      if (checkbox) {
        const checkmark = checkbox
          .closest(".checkbox-item")
          .querySelector(".checkmark");

        if (checkbox.checked) {
          checkmark.classList.add("active");
        } else {
          checkmark.classList.remove("active");
        }
        checkbox.addEventListener("change", function () {
          const value = this.checked;
          const checkmark =
            this.closest(".checkbox-item").querySelector(".checkmark");
          if (value) {
            checkmark.classList.add("active");
          } else {
            checkmark.classList.remove("active");
          }
        });
      }
    });
  }
};
