#!/usr/bin/env python3
"""Builds a WordPress theme (wordpress-theme/social-pulse) from the static HTML pages.

Run:  python3 build-wordpress-theme.py
Then upload wordpress-theme/social-pulse.zip in WordPress → Appearance → Themes → Add New → Upload.
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "wordpress-theme" / "social-pulse"

# static file -> (WordPress template file, page slug or None for the front page)
PAGES = {
    "index.html": ("front-page.php", None),
    "about.html": ("page-about.php", "about"),
    "tiktok.html": ("page-tiktok-tips.php", "tiktok-tips"),
    "instagram.html": ("page-instagram-tips.php", "instagram-tips"),
}

THEME_HEADER = """/*
Theme Name: Social Pulse
Theme URI: https://github.com/
Description: Social media analytics & posting tips. Black, white, brown and cream. Built from the Social Pulse HTML site.
Version: 1.0.0
Requires at least: 6.0
Requires PHP: 7.4
License: GPLv2 or later
Text Domain: social-pulse
*/
"""

FUNCTIONS_PHP = """<?php
function social_pulse_setup() {
    add_theme_support('title-tag');
    add_theme_support('html5', array('script', 'style'));
}
add_action('after_setup_theme', 'social_pulse_setup');

function social_pulse_assets() {
    wp_enqueue_style('social-pulse-fonts', 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap', array(), null);
    wp_enqueue_style('social-pulse-style', get_stylesheet_uri(), array(), '1.0.0');
    wp_enqueue_script('social-pulse-script', get_template_directory_uri() . '/script.js', array(), '1.0.0', true);
}
add_action('wp_enqueue_scripts', 'social_pulse_assets');

/* On theme activation, create the About / TikTok Tips / Instagram Tips pages
   and set a static front page so the menu links work right away. */
function social_pulse_create_pages() {
    $pages = array('about' => 'About', 'tiktok-tips' => 'TikTok Tips', 'instagram-tips' => 'Instagram Tips', 'home' => 'Home');
    foreach ($pages as $slug => $title) {
        if (!get_page_by_path($slug)) {
            wp_insert_post(array('post_title' => $title, 'post_name' => $slug, 'post_status' => 'publish', 'post_type' => 'page'));
        }
    }
    $home = get_page_by_path('home');
    if ($home) {
        update_option('show_on_front', 'page');
        update_option('page_on_front', $home->ID);
    }
    if (get_option('permalink_structure') === '') {
        update_option('permalink_structure', '/%postname%/');
    }
    flush_rewrite_rules();
}
add_action('after_switch_theme', 'social_pulse_create_pages');
"""

INDEX_PHP = """<?php get_header(); ?>
<main>
  <section class="page-hero">
    <div class="container narrow">
      <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
        <h1><?php the_title(); ?></h1>
        <div class="lead"><?php the_content(); ?></div>
      <?php endwhile; else : ?>
        <h1>Nothing here yet</h1>
      <?php endif; ?>
    </div>
  </section>
</main>
<?php get_footer(); ?>
"""


def wp_links(html: str) -> str:
    """Turn static .html links into WordPress permalinks."""
    for static, (_, slug) in PAGES.items():
        url = "<?php echo esc_url(home_url('/" + (slug + "/" if slug else "") + "')); ?>"
        html = re.sub(r'href="' + re.escape(static) + r'(#[^"]*)?"', lambda m: 'href="' + url + (m.group(1) or "") + '"', html)
    return html


def split(html: str):
    head_end = html.index("<body>") + len("<body>")
    main_start = html.index("<main>")
    main_end = html.index("</main>") + len("</main>")
    footer_end = html.index('<script src="script.js"></script>')
    return html[head_end:main_start], html[main_start:main_end], html[main_end:footer_end]


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    home = wp_links((ROOT / "index.html").read_text())
    header_html, _, footer_html = split(home)

    (OUT / "header.php").write_text(
        "<!DOCTYPE html>\n<html <?php language_attributes(); ?>>\n<head>\n"
        "  <meta charset=\"<?php bloginfo('charset'); ?>\">\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "  <?php wp_head(); ?>\n</head>\n<body <?php body_class(); ?>>\n<?php wp_body_open(); ?>\n"
        + header_html
    )
    (OUT / "footer.php").write_text(footer_html + "\n<?php wp_footer(); ?>\n</body>\n</html>\n")

    for static, (template, slug) in PAGES.items():
        _, main_html, _ = split(wp_links((ROOT / static).read_text()))
        name = "" if slug is None else "<?php /* Template for the '" + slug + "' page */ ?>\n"
        (OUT / template).write_text(name + "<?php get_header(); ?>\n" + main_html + "\n<?php get_footer(); ?>\n")

    (OUT / "style.css").write_text(THEME_HEADER + "\n" + (ROOT / "styles.css").read_text())
    shutil.copy(ROOT / "script.js", OUT / "script.js")
    (OUT / "functions.php").write_text(FUNCTIONS_PHP)
    (OUT / "index.php").write_text(INDEX_PHP)
    (OUT / "page.php").write_text(INDEX_PHP)

    shutil.make_archive(str(OUT), "zip", OUT.parent, OUT.name)
    print("Built", OUT, "and", str(OUT) + ".zip")


if __name__ == "__main__":
    main()
