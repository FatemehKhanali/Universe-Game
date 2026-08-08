document.addEventListener("DOMContentLoaded", function() {
    const startBtn = document.getElementById("startButton");
    const video = document.getElementById("introVideo");
    const preloader = document.getElementById("preloader");
    const mainContent = document.getElementById("mainContent");


    if (startBtn && video && preloader && mainContent) {
        document.addEventListener("keydown", function(event) {
            if (event.key === "Enter" && startBtn) {
                startBtn.click();
            }
        });

        startBtn.addEventListener("click", function () {
            if (preloader && video && mainContent) {
                preloader.style.display = "flex";
                video.volume = 1;
                video.play();

                video.addEventListener("ended", function () {
                    preloader.classList.add("fade-out");
                    setTimeout(() => {
                        preloader.style.display = "none";
                        mainContent.style.display = "block";
                    }, 1000);
                });
            }
        });
    } else {

        console.log("Video player disabled - elements not found");


        if (preloader) {
            preloader.style.display = "none";
        }


        if (mainContent) {
            mainContent.style.display = "block";
        }
    }
});