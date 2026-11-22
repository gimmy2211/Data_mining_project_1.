# Wholesale Customer Channel API — Vercel deployment

This is a deployable FastAPI version of the course project. It includes the
dataset and trains the model automatically when the server starts, so there is
no notebook path or local `.joblib` file to configure.

## Free deployment — no Visa

Vercel's **Hobby** plan is free for personal projects and has no billing cycle.
Vercel documents that FastAPI is deployed automatically when an `app` instance
is exported from `app.py`.

1. Create a free [GitHub](https://github.com/signup) account if you do not have one.
2. Create a new empty GitHub repository, for example `wholesale-api`.
3. Upload all files from this folder (including `data/wholesale_customers.csv`) to that repository.
4. Create a free [Vercel](https://vercel.com/signup) account using GitHub.
5. In Vercel, click **Add New → Project**, import `wholesale-api`, then press **Deploy**. Leave the build settings unchanged.
6. When the deployment finishes, open `https://YOUR-PROJECT.vercel.app/docs` to test the API.

## Endpoints

* `GET /` — API details and required features
* `GET /health` — health check
* `POST /predict` — channel prediction

Use this request body in `/docs`:

```json
{
  "features": {
    "Fresh": 12669,
    "Milk": 9656,
    "Grocery": 7561,
    "Frozen": 214,
    "Detergents_Paper": 2674,
    "Delicassen": 1338
  }
}
```

Example endpoint after deployment:

```text
https://YOUR-PROJECT.vercel.app/predict
```
