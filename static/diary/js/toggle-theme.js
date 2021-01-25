const DARK_THEME_URL = "/static/diary/css/dark-theme.css";
const LIGHT_THEME_URL = "/static/diary/css/light-theme.css";
const DARK_THEME = "dark";
const LIGHT_THEME = "light";

const theme = document.querySelector("#theme-link");
const toggleIcon = document.querySelector("#toggle-icon");
const currentTheme = localStorage.getItem("theme");

if (currentTheme == DARK_THEME) {
  theme.href = DARK_THEME_URL;
  toggleIcon.className = "fas fa-2x fa-sun text-warning";
} else {
  theme.href = LIGHT_THEME_URL;
  toggleIcon.className = "fas fa-2x fa-moon text-black";
}

toggleIcon.addEventListener("click", () => {
  const currentTheme = localStorage.getItem("theme");
  let newTheme;

  if (currentTheme == DARK_THEME) {
    theme.href = LIGHT_THEME_URL;
    newTheme = LIGHT_THEME;
    toggleIcon.className = "fas fa-2x fa-moon text-dark";
  } else {
    theme.href = DARK_THEME_URL;
    newTheme = DARK_THEME;
    toggleIcon.className = "fas fa-2x fa-sun text-warning";
  }

  localStorage.setItem("theme", newTheme);
});