# Deploy OpenMat to Streamlit Community Cloud

## Deployment settings

- Repository: the GitHub repository containing this project
- Branch: `main`
- Main file path: `app.py`
- Advanced settings → Python version: `3.11` (matches local verification)
- Secrets: none required
- App URL: choose an available subdomain during deployment

The root `requirements.txt` pins the verified Streamlit version. The app uses local JSON files under `data/`, which must be committed with `app.py`, `engine/`, and `.streamlit/config.toml`. No database or external API is required. Do not upload `.venv`, `.env`, or `.streamlit/secrets.toml`.

## Publish

1. Push this project's `main` branch to your GitHub repository.
2. Sign into https://share.streamlit.io/ and connect the intended GitHub account.
3. Choose **Create app**, then **Yup, I have an app**.
4. Enter the repository, `main`, and `app.py`.
5. In **Advanced settings**, choose Python `3.11`.
6. Choose an available app subdomain and deploy.
7. Open the resulting `.streamlit.app` URL and build a 60-minute plan.
8. Check round length changes, Takedowns, preparation options, and downloads.

Changes pushed to the connected branch trigger app updates. If deploying from a private repository requires additional GitHub permissions, review the requested access before granting it.

## Runtime behavior

Plans are held per Streamlit browser session, not in a database. Users can download Markdown or JSON copies; cloud restarts or session loss can discard a plan. The app does not save a shared training history. Prototype content and review notices remain visible in the published app.

## Official instructions

- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
