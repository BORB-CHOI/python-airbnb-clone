const gulp = require("gulp");

const routes = {
  css: {
    templates: "templates/**/*.html",
    src: "assets/scss/styles.scss",
    dest: "static/css",
  },
};

const css = () => {
  const nodeSass = require("node-sass");
  const gulpSass = require("gulp-sass");
  const sass = gulpSass(nodeSass);
  const postCSS = require("gulp-postcss");
  const minify = require("gulp-csso");

  return gulp
    .src(routes.css.src, { allowEmpty: true })
    .pipe(sass().on("error", sass.logError))
    .pipe(postCSS([require("tailwindcss"), require("autoprefixer")]))
    .pipe(minify())
    .pipe(gulp.dest(routes.css.dest));
};

const watch = () => {
  gulp.watch(routes.css.templates, css);
  gulp.watch(routes.css.src, css);
};

const live = gulp.parallel([watch]);

const dev = gulp.series([css, live]);

exports.default = dev;
