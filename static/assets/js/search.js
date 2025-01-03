const search = () => {
  const searchForm = document.querySelector(".search-form-container");
  const searchToggle = document.querySelector(".search-toggle");
  const searchShow = document.querySelector(".for-search-show");
  const searchClose = document.querySelector(".for-search-close");
  if (searchForm) {
    searchToggle.addEventListener("click", () => {
      searchForm.classList.toggle("active");
    });
  }
};
