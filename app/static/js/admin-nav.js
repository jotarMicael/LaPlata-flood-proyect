function openNav() {
    sideNav = document.getElementById("mySidenav");
    content = document.getElementById("content");
    button = document.getElementById("side-bar-button");
  
    sideNav.style.marginLeft = "0px";
    sideNav.style.opacity = "1";
    sideNav.style.zindex=1;
  
    if (!window.matchMedia("(max-width: 768px)").matches) {
      content.style.width = "calc(100% - 250px)";
      button.onclick = () => closeNav();
    }
  }
  
  function closeNav() {
    sideNav = document.getElementById("mySidenav");
    content = document.getElementById("content");
    button = document.getElementById("side-bar-button");
  
    sideNav.style.marginLeft = "-250px";
    sideNav.style.opacity = "0";
  
    button.onclick = () => openNav();
    if (!window.matchMedia("(max-width: 768px)").matches) {
      content.style.width = "100%";
    }
  }