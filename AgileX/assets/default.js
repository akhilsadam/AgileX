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

function resizeIFrameToFitContent(iFrame) {

    iFrame.width = iFrame.contentWindow.document.body.scrollWidth;
    iFrame.height = iFrame.contentWindow.document.documentElement.offsetHeight;
    // console.log(iFrame.contentWindow.document.documentElement.offsetHeight);
}

function onscrollF(element) {
    let scrollTop = element.scrollTop;
    // console.log(scrollTop);
    let docHeight = element.querySelector(".version-style").offsetHeight;
    // console.log(docHeight);
    let winHeight = element.offsetHeight;
    // console.log(winHeight);
    let scrollPercent = scrollTop / (docHeight - winHeight);
    // let size = 60;
    // let degrees = Math.round((1 - scrollPercent) * (360));
    // let degrees2 = degrees - size;
    // element.querySelector(".avance-recule").style.background = `conic-gradient(rgb(235, 246, 247) ${degrees2}deg, rgb(23, 20, 18) ${degrees2}deg, rgb(23, 20, 18) ${degrees}deg, rgb(235, 246, 247) ${degrees}deg)`;
    let shift = 180;
    let degrees = Math.round((1 - scrollPercent) * 360);
    element.querySelector(".avance-recule").style.background = `conic-gradient(from ${shift}deg, rgb(23, 20, 18) ${degrees}deg, rgba(235, 246, 247,0.05) ${degrees}deg)`; //rgb(235, 246, 247)

}


setTimeout(() => {
    // var csstext = ["background: url('/static/img/img.jpg');",
    //     "background-size: cover;",
    //     "background-attachment: fixed;",
    //     "background-position: 50% 50%;",
    // ].join();

    // var gs = document.querySelectorAll("g");
    // Array.prototype.forEach.call(gs, element => {
    //     // element.setAttribute("style", "fill: blue; stroke: black; backdrop-filter:blur(0px);mix-blend-mode: difference;");
    //     element.setAttribute("style", "background: transparent; backdrop-filter:blur(0px)");
    // });
    // var ps = document.querySelectorAll("path");
    // Array.prototype.forEach.call(ps, element => {
    //     element.setAttribute("style", "fill: transparent; stroke: rgb(23, 20, 18); backdrop-filter:blur(0px);/*mix-blend-mode: difference;*/");
    // });
    // var cs = document.querySelectorAll("circle");
    // Array.prototype.forEach.call(cs, element => {
    //     element.setAttribute("style", "fill: transparent; stroke: black; backdrop-filter:blur(0px);mix-blend-mode: difference;");
    // });
    // var us = document.querySelectorAll("use:hover");
    // Array.prototype.forEach.call(us, element => {
    //     element.setAttribute("style", "fill: red; stroke: black; backdrop-filter:blur(0px);mix-blend-mode: difference;");
    // });
}, 3000);

setTimeout(() => {
    var vers = document.getElementsByClassName("version");
    Array.prototype.forEach.call(vers, element => {
        element.scrollTop = element.scrollHeight;
        element.onscroll = () => { onscrollF(element) };
    });


    var iframes = document.getElementsByClassName("embeds");
    Array.prototype.forEach.call(iframes, element => {
        var ims = element.contentWindow.document.querySelectorAll("img");
        Array.prototype.forEach.call(ims, im => {
            var src = im.src;
            if (src.includes('.gif')) {
                im.setAttribute("style", "filter: invert(1);");
            }
        });
        resizeIFrameToFitContent(element);
        element.addEventListener("change", () => {
            resizeIFrameToFitContent(element);
        });
    });

    var gdc = document.getElementsByClassName("gcd");
    Array.prototype.forEach.call(gdc, element => {
        element.addEventListener("change", () => {
            location.reload();
        });
    });

}, 3000);