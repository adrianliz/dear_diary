const slider = document.getElementById("rangeInput");
const output = document.getElementById("rangeValue");
output.innerHTML = slider.value;

slider.oninput = function () {
  output.innerHTML = slider.value;
}