var collaspe = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < collaspe.length; i++) {
    collaspe[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var section = this.nextElementSibling;
        if (section.style.maxHeight) {
            section.style.maxHeight = null;
        } else {
            section.style.maxHeight = section.scrollHeight + "px";
        }
    });
}