# Hosting this portfolio on GitHub Pages

GitHub Pages is free, needs no server, and serves static sites like this one perfectly.
Pick **Route A** (browser only, no tools to install) or **Route B** (Git command line).

---

## Step 0 — Fill in your links first

Open `assets/js/main.js` in Notepad (or any editor) and edit the block at the very top:

```js
var PROFILES = {
  linkedin:     'https://www.linkedin.com/in/your-handle',
  researchgate: 'https://www.researchgate.net/profile/Your-Name',
  scholar:      'https://scholar.google.com/citations?user=XXXXXXX',
  github:       'https://github.com/your-username',
  certificate:  'https://drive.google.com/file/d/XXXX/view'
};
```

Keep the quotes and the commas. Any link you leave as `''` still shows on the page but
stays inactive.

Then double-click `index.html` to check everything looks right in your browser before
you publish.

---

## Choose your URL first

| You want | Repository name | Resulting URL |
| --- | --- | --- |
| A clean personal site (**recommended**) | `alvi-anil.github.io` — literally `<your-username>.github.io` | `https://<your-username>.github.io/` |
| A project-style site | anything, e.g. `portfolio` | `https://<your-username>.github.io/portfolio/` |

Both work identically with these files. The rest of this guide assumes the first option.

---

## Route A — Upload through the GitHub website (no installs)

### A1. Create a GitHub account
Go to <https://github.com/signup> and sign up. Note your **username** — it becomes part
of your URL, so pick something professional (e.g. `alviamzad`).

### A2. Create the repository
1. Click the **+** in the top-right corner → **New repository**.
2. **Repository name:** `<your-username>.github.io`
   (exactly your username, then `.github.io` — all lowercase).
3. Set it to **Public**. Pages is free only for public repos on free accounts.
4. Do **not** tick "Add a README file".
5. Click **Create repository**.

### A3. Upload the files
1. On the empty repository page, click **uploading an existing file**.
2. Open the `alvi-portfolio` folder on your computer.
3. Select **everything inside it** — `index.html`, the `assets` folder, `README.md`,
   `DEPLOY.md`, `serve.py` — and drag them onto the GitHub upload area.

   > **Important:** upload the *contents* of the folder, not the folder itself.
   > `index.html` must end up at the top level of the repository. If you see
   > `alvi-portfolio/index.html` in the file list, you dragged the wrong thing —
   > delete and retry.

   > **The `.nojekyll` file:** Windows hides files starting with a dot. In File
   > Explorer, go to the **View** tab → tick **Hidden items** so you can select it.
   > Nothing breaks if you miss it — this site does not use underscore-prefixed
   > folders — but including it is safer.

4. Wait for every file to finish uploading (the `assets` folder should show its
   sub-folders).
5. In the **Commit changes** box type `Add portfolio` and click **Commit changes**.

### A4. Turn on GitHub Pages
1. In the repository, click **Settings** (top bar).
2. In the left sidebar click **Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. **Branch:** `main`, folder: **`/ (root)`**. Click **Save**.

### A5. Visit your site
Wait 1–3 minutes (the first build is the slowest). Refresh the Settings → Pages screen —
a green banner appears with your live link:

```
https://<your-username>.github.io/
```

Open it. Done.

### A6. Making changes later
1. In the repository, click the file you want to change (e.g. `index.html`).
2. Click the **pencil** icon, edit, then **Commit changes**.
3. To replace a file entirely, click **Add file → Upload files** and drop the new
   version in — same filename overwrites it.
4. Changes go live about a minute later. Press **Ctrl+F5** to bypass your browser cache
   if you still see the old version.

---

## Route B — Git command line

Git is already installed on your machine.

### B1. One-time setup
```bash
git config --global user.name  "Alvi Ibn Amzad Anil"
git config --global user.email "alviamzad02@gmail.com"
```

### B2. Create the empty repository on GitHub
Same as **A2** above: public, named `<your-username>.github.io`, no README.

### B3. Push the files

Open **Git Bash** (right-click inside the `alvi-portfolio` folder → *Open Git Bash here*),
or PowerShell, and run:

```bash
cd "C:/Users/Asus ROG Strix G16/alvi-portfolio"

git init
git branch -M main
git add .
git commit -m "Add portfolio"
git remote add origin https://github.com/<your-username>/<your-username>.github.io.git
git push -u origin main
```

Replace `<your-username>` in both places. GitHub will ask you to sign in — a browser
window opens for authentication.

### B4. Enable Pages
Same as **A4**: Settings → Pages → Deploy from a branch → `main` → `/ (root)` → Save.

### B5. Publishing updates later
```bash
cd "C:/Users/Asus ROG Strix G16/alvi-portfolio"
git add .
git commit -m "Update publications"
git push
```

---

## Optional — a custom domain

If you buy a domain such as `alvianil.com`:

1. At your domain registrar, add these DNS records:
   - Four `A` records for `@` pointing to `185.199.108.153`, `185.199.109.153`,
     `185.199.110.153`, `185.199.111.153`
   - One `CNAME` record for `www` pointing to `<your-username>.github.io`
2. In the repository: **Settings → Pages → Custom domain**, enter your domain, **Save**.
3. Once the check passes, tick **Enforce HTTPS**.

---

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| 404 page not found | `index.html` is not at the repository root. Open the repo — if you see a folder named `alvi-portfolio`, open it, delete it, and re-upload the *contents*. |
| Site loads but looks unstyled | The `assets` folder did not upload. Check that `assets/css/style.css` exists in the repo and that the path has no capital letters — GitHub Pages is case-sensitive. |
| Résumé button gives 404 | `assets/files/Alvi-Ibn-Amzad-Anil-CV.pdf` is missing or renamed. Re-upload it with exactly that name. |
| Social buttons show a reminder toast | Expected until you complete **Step 0**. |
| Changes don't appear | Wait a minute for the rebuild, then hard-refresh with **Ctrl+F5**. Check the **Actions** tab for a failed deployment. |
| Pages section missing in Settings | The repository is private. Settings → General → scroll to the bottom → **Change visibility → Public**. |

---

## Quick reference

- **Your site:** `https://<your-username>.github.io/`
- **Edit content:** `index.html`
- **Edit colours:** the `:root` block at the top of `assets/css/style.css`
- **Edit links and rotating titles:** `assets/js/main.js`
- **Replace the CV:** drop a new PDF into `assets/files/` and update the `href` on the
  Résumé button in `index.html` (search for `assets/files/`)
