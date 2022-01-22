console.log("default.js");
setTimeout(() => {
    const growers = document.querySelectorAll(".grow-wrap");
    growers.forEach((grower) => {
        const textarea = grower.querySelector("textarea");
        textarea.addEventListener("input", () => {
            grower.dataset.replicatedValue = textarea.value;
        });
    });
}, 2000);

window.onscroll = () => {
    let scrollTop = window.scrollY;
    let docHeight = document.body.offsetHeight;
    let winHeight = window.innerHeight;
    let scrollPercent = scrollTop / (docHeight - winHeight);
    let scrollPercentRounded = Math.round(scrollPercent * 100);
    document.querySelector(".avance-reculer").style.background = `linear-gradient(to right, rgb(188, 45, 41) ${scrollPercentRounded}%, rgb(23, 20, 18) ${scrollPercentRounded}%)`;
}