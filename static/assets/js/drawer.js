// open drawer
const handleOpen = (drawer, drawerShow) => {
  const drawerContainer = drawer.parentNode;
  drawerShow.addEventListener("click", () => {
    const mobileControllerIcon = drawerShow.querySelector(".utilize-toggle");

    if (mobileControllerIcon) {
      mobileControllerIcon.classList.toggle("close");
    }
    drawerContainer.classList.add("active");
  });
};
// close drawer
const handleClose = (drawer, drawerShow, closedrawer) => {
  const drawerContainer = drawer.parentNode;
  closedrawer.addEventListener("click", () => {
    drawerContainer.classList.remove("active");
    const mobileControllerIcon = drawerShow.querySelector(".utilize-toggle");
    if (mobileControllerIcon) {
      mobileControllerIcon.classList.toggle("close");
    }
  });
};
// controll mobile menu
const drawer = () => {
  const drawerShowButtons = document.querySelectorAll(".show-drawer");
  const drawers = document.querySelectorAll(".drawer");
  if (drawerShowButtons?.length) {
    drawerShowButtons.forEach((drawerShow, idx) => {
      const drawer = drawers[idx];
      if (drawer) {
        const darawerContainer = drawer.parentNode;
        handleOpen(drawer, drawerShow);
        const closedrawers = darawerContainer.querySelectorAll(".close-drawer");
        closedrawers?.forEach((closedrawer) => {
          handleClose(drawer, drawerShow, closedrawer);
        });
      }
    });
  }
};
