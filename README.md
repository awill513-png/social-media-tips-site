# Social Pulse: Social Media Analytics & Posting Tips

A website about social media analytics and posting tips, in a black / white / brown / cream design.

**Pages:** Home · About · TikTok Tips · Instagram Tips

## What's in here

| File | What it is |
|---|---|
| `index.html` | Home: key metrics, analytics funnel, weekly routine, posting-time heatmap, engagement calculator |
| `about.html` | About page |
| `tiktok.html` | TikTok tips: retention curve, hook formulas, video structure, analytics |
| `instagram.html` | Instagram tips: format comparison, Reel safe zones, carousel anatomy, sizes, checklist |
| `styles.css` / `script.js` | Shared design and interactive features (menu, calculator, checklist) |
| `wordpress-theme/social-pulse.zip` | The same site as a WordPress theme |
| `build-wordpress-theme.py` | Rebuilds the WordPress theme after you edit the HTML |

## View it locally
Double-click `index.html` to open it in your browser.

## Put it online with GitHub Pages
1. Push this folder to a GitHub repository.
2. On GitHub, go to **Settings → Pages**, set the source to **Deploy from a branch**, pick `main` and `/ (root)`, then save.
3. Your site will be live at `https://<your-username>.github.io/<repo-name>/`.

## Use it in WordPress
1. In WordPress admin, go to **Appearance → Themes → Add New → Upload Theme**.
2. Upload `wordpress-theme/social-pulse.zip` and click **Activate**.
3. The theme automatically creates the Home, About, TikTok Tips and Instagram Tips pages and sets Home as the front page.

> Note: Uploading themes requires self-hosted WordPress (wordpress.org) or a WordPress.com plan that allows custom themes.

## Editing
Edit the `.html` files, then run `python3 build-wordpress-theme.py` to update the WordPress theme too.
