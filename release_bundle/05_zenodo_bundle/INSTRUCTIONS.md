# Zenodo Upload Bundle

After completing GitHub push (step 3 in DEPLOY_GUIDE.md):

1. Go to https://zenodo.org/account/settings/github/
2. Toggle ON the cm-rg repository
3. Create a GitHub release: `git tag v1.0 && git push origin v1.0`
4. Zenodo will automatically mint a DOI for the release.
5. Copy the DOI back to CITATION.cff in HF dataset and GitHub README.

Manual alternative: zip the GitHub repo and upload via Zenodo web UI.
