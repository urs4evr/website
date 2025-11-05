# LoveKeeper Website

This directory contains the website files for LoveKeeper, hosted on GitHub Pages.

## Files

- **index.html** - Landing page with app features and download links
- **privacy.html** - Privacy Policy (REQUIRED for app store submission)
- **terms.html** - Terms of Service (REQUIRED for iOS, RECOMMENDED for Android)
- **support.html** - Support page with FAQ and contact information

## Deployment

### Automatic Deployment (Recommended)

The website auto-deploys to GitHub Pages when you push to the main branch, thanks to GitHub Actions.

1. Push any changes to main:
   ```bash
   git add public/
   git commit -m "Update website"
   git push origin main
   ```

2. GitHub Actions will automatically deploy to:
   ```
   https://[YOUR_GITHUB_USERNAME].github.io/[YOUR_REPO_NAME]/
   ```

3. Wait 2-5 minutes for deployment to complete

### Manual Deployment

If you prefer to deploy manually:

```bash
npm run deploy:website:manual
```

This will deploy the public folder to the `gh-pages` branch.

## Setup GitHub Pages

1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Under "Source", select:
   - **Branch**: `gh-pages`
   - **Folder**: `/ (root)`
4. Click **Save**
5. Your site will be published at: `https://[username].github.io/[repo-name]/`

## Customization

### Update Contact Emails

Search and replace in all HTML files:
- `support@lovekeeper.app` → your actual support email
- `privacy@lovekeeper.app` → your actual privacy email
- `legal@lovekeeper.app` → your actual legal email

### Update Privacy Policy

In **privacy.html**:
- Replace `[Your Company Name]` with your company name
- Replace `[Contact Email]` with your contact email
- Review all sections and customize as needed

### Update Terms of Service

In **terms.html**:
- Replace `[Your Jurisdiction]` with your legal jurisdiction
- Review all sections and customize as needed

### Update Download Links

In **index.html**, update the download button URLs once your app is published:

```html
<!-- iOS App Store -->
<a href="https://apps.apple.com/app/idYOUR_APP_ID">

<!-- Google Play Store -->
<a href="https://play.google.com/store/apps/details?id=com.lovekeeper.app">
```

## Required Actions Before App Submission

1. ✅ Deploy website to GitHub Pages
2. ✅ Get your website URL (https://username.github.io/repo-name/)
3. ✅ Update app.json with these URLs:
   ```json
   {
     "expo": {
       "privacy": "https://username.github.io/repo-name/privacy.html",
       "termsOfService": "https://username.github.io/repo-name/terms.html"
     }
   }
   ```
4. ✅ Test all links work (privacy, terms, support)
5. ✅ Enter URLs in App Store Connect / Play Console

## Testing

After deployment, test these pages:

- Landing: `https://[username].github.io/[repo-name]/`
- Privacy: `https://[username].github.io/[repo-name]/privacy.html`
- Terms: `https://[username].github.io/[repo-name]/terms.html`
- Support: `https://[username].github.io/[repo-name]/support.html`

## Custom Domain (Optional)

To use a custom domain like `lovekeeper.app`:

1. Buy a domain (Namecheap, Google Domains, etc.)
2. Add a `CNAME` file to this directory with your domain:
   ```
   lovekeeper.app
   ```
3. Configure DNS records at your domain registrar:
   ```
   Type: CNAME
   Host: @
   Value: [username].github.io
   ```
4. Enable custom domain in GitHub Pages settings
5. Enable HTTPS (GitHub provides free SSL)

## Monitoring

### Check Deployment Status

1. Go to your repository
2. Click **Actions** tab
3. Look for "Deploy Website to GitHub Pages" workflow
4. Green checkmark = successful deployment
5. Red X = failed deployment (click for details)

### Analytics (Optional)

To add Google Analytics or similar:

1. Get your tracking ID
2. Add tracking code to `<head>` of all HTML files
3. Redeploy

## Maintenance

### Regular Updates

- Review and update privacy policy annually
- Update support FAQ based on user questions
- Add new features to landing page
- Keep screenshots current

### Legal Compliance

- Privacy policy must stay up-to-date with app features
- Terms of service should match actual app usage
- Notify users of policy changes via app update notes

## Support

If you have questions about the website setup:

1. Check GitHub Pages documentation
2. Review GitHub Actions logs
3. Test URLs in incognito/private browsing
4. Ensure DNS propagation (for custom domains, can take 24-48 hours)

## License

© 2025 LoveKeeper. All rights reserved.
