// var swiper = new Swiper(".swiper-container", {
//   slidesPerView: 1,
//   effect: "fade",
//   navigation: {
//     nextEl: ".swiper-button-next",
//     prevEl: ".swiper-button-prev",
//   },
//   pagination: {
//     el: ".swiper-pagination",
//   },
//   loop: true,
//   autoplay: {
//     delay: 2000,
//   },
//   speed: 2000,
// });

/************************************************************************************** */
//Comment Scripts
replyBtn = document.querySelectorAll(".reply-btn");
replyForm = document.querySelectorAll(".reply-form");
for (let i = 0; i < replyBtn.length; i++) {
  replyBtn[i].addEventListener("click", () => {
    replyBtn[i].classList.toggle("active");
    for (j = 0; j < replyForm.length; j++) {
      if (
        replyBtn[i].classList.contains("active") &&
        replyForm[j].getAttribute("data-comment-id") ===
          replyBtn[i].getAttribute("data-comment-id")
      ) {
        replyForm[j].style.maxHeight = "500px";
      } else {
        replyForm[j].style.maxHeight = "0";
      }
    }
  });
}

/************************************************************************************************* */
//Replies View
replyView = document.querySelectorAll(".reply-view");
replyContent = document.querySelectorAll(".replies-content");
for (let i = 0; i < replyView.length; i++) {
  replyView[i].addEventListener("click", () => {
    replyView[i].classList.toggle("active");
    for (j = 0; j < replyContent.length; j++) {
      if (
        replyView[i].classList.contains("active") &&
        replyContent[j].getAttribute("data-comment-id") ===
          replyView[i].getAttribute("data-comment-id")
      ) {
        replyContent[j].style.maxHeight = "500px";
      } else {
        replyContent[j].style.maxHeight = "0";
      }
    }
  });
}

/************************************************************************************************************** */
//Comments Display Toogle

const displayComment = document.querySelector(".display-comment");
const showComment = document.querySelector(".show-comment")

displayComment.addEventListener('click', () => {
  displayComment.classList.toggle("show")
  if (displayComment.classList.contains("show")) {
    showComment.style.maxHeight = showComment.scrollHeight + "px";
    displayComment.innerHTML = "Hide Comments"
  } else {
    showComment.style.maxHeight = 0;
    displayComment.innerHTML = "Show Comments";
  }
})

// const swiper = new Swiper(".swiper", {
//   direction: "vertical",
//   loop: true,

//   // Pagination
//   pagination: {
//     el: ".swiper-pagination",
//     clickable: true,
//   },

//   navigation: {
//     nextEl: ".swiper-button-next",
//     prevEl: ".swiper-button-prev",
//   },

//   scrollbar: {
//     el: ".swiper-scrollbar",
//   },
// });

/**********************Gallery Animation********/

let mainSliderSelector = ".main-slider",
  navSliderSelector = ".nav-slider",
  interleaveOffset = 0.5;

// Main Slider
let mainSliderOptions = {
  loop: false,
  speed: 1000,
  autoplay: {
    delay: 3000,
  },
  loopAdditionalSlides: 10,
  grabCursor: true,
  watchSlidesProgress: true,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  on: {
    imagesReady: function () {
      this.el.classList.remove("loading");
      // Autoplay starts automatically, so no need to call autoplay.start here
    },
    slideChangeTransitionEnd: function () {
      let swiper = this,
        captions = swiper.el.querySelectorAll(".caption");
      for (let i = 0; i < captions.length; ++i) {
        captions[i].classList.remove("show");
      }
      swiper.slides[swiper.activeIndex]
        .querySelector(".caption")
        .classList.add("show");
    },
    progress: function () {
      let swiper = this;
      for (let i = 0; i < swiper.slides.length; i++) {
        let slideProgress = swiper.slides[i].progress,
          innerOffset = swiper.width * interleaveOffset,
          innerTranslate = slideProgress * innerOffset;

        swiper.slides[i].querySelector(".slide-bgimg").style.transform =
          "translateX(" + innerTranslate + "px)";
      }
    },
    touchStart: function () {
      let swiper = this;
      for (let i = 0; i < swiper.slides.length; i++) {
        swiper.slides[i].style.transition = "";
      }
    },
    setTransition: function (speed) {
      let swiper = this;
      for (let i = 0; i < swiper.slides.length; i++) {
        swiper.slides[i].style.transition = speed + "ms";
        swiper.slides[i].querySelector(".slide-bgimg").style.transition =
          speed + "ms";
      }
    },
  },
};
let mainSlider = new Swiper(mainSliderSelector, mainSliderOptions);

// Navigation Slider
let navSliderOptions = {
  loop: false,
  loopAdditionalSlides: 10,
  speed: 1000,
  spaceBetween: 5,
//   slidesPerView: 5,
  centeredSlides: true,
  touchRatio: 0.2,
  slideToClickedSlide: true,
  direction: "horizontal",
  breakpoints: {
    // When the viewport width is >= 320px (small screens like mobile)
    320: {
      slidesPerView: 2, // Show 1 slide per view
      spaceBetween: 10,
    },
    // When the viewport width is >= 480px (tablets)
    480: {
      slidesPerView: 3, // Show 2 slides per view
      spaceBetween: 20,
    },
    // When the viewport width is >= 768px (larger tablets and small desktops)
    768: {
      slidesPerView: 4, // Show 3 slides per view
      spaceBetween: 30,
    },
    // When the viewport width is >= 1024px (desktop screens)
    1024: {
      slidesPerView: 5, // Show 4 slides per view
      spaceBetween: 40,
    },
  },
  on: {
    imagesReady: function () {
      this.el.classList.remove("loading");
    },
    click: function () {
      mainSlider.autoplay.stop();
    },
  },
};
let navSlider = new Swiper(navSliderSelector, navSliderOptions);

// Matching sliders
mainSlider.controller.control = navSlider;
navSlider.controller.control = mainSlider;
