# Practice Guide — Treat This Like a Real QA Assignment

You've been "handed" a live e-commerce app (like a new QA hire on day one).
Nobody wrote your test cases or your automation framework for you — that's
your job. This folder is intentionally empty (`pages/`, `tests/`) so you
build it yourself. A full working answer key exists in
`reference_solution/` — see `reference_solution/README.md` for how to use
it *without* short-circuiting your own learning.

---

## Step 0 — Get the app running

You need this working first (see the root `README.md`):
- Backend API on `http://localhost:4000`
- Frontend on `http://localhost:5500`
- Seeded MySQL database

Confirm with `curl http://localhost:4000/api/health` and by opening
`http://localhost:5500` in a browser.

---

## Step 1 — Exploratory testing (no code yet)

Before writing a single test, **use the app like a real user for 20–30
minutes.** This is what a QA engineer does on day one with any new
product. As you go, keep a running note of:

- Every page and what it's supposed to do
- Every input field, button, dropdown you can interact with
- Anything that looks wrong, inconsistent, or surprising
- Questions you have about expected behavior (what SHOULD happen here?)

Try things a "normal" user wouldn't: empty forms, huge numbers, special
characters, refreshing mid-action, going back, opening the same page in
two tabs. This instinct — poking at edges — is 80% of manual QA skill.

---

## Step 2 — Write manual test cases (still no code)

Pick **one page** to start with (recommendation: `login.html` — it's the
smallest). For that page, write test cases in plain English, in a table
or list, like this:

| # | Test case | Steps | Expected result |
|---|-----------|-------|------------------|
| 1 | Valid login succeeds | Enter correct email/password, click Log in | Redirected to shop, nav shows logged-in state |
| 2 | Wrong password shows error | Enter correct email, wrong password, click Log in | Error message shown, stays on login page |
| 3 | Empty email blocked | Leave email blank, click Log in | Form doesn't submit / browser validation message |

Aim for **10–15 test cases per page** covering: happy path, wrong/invalid
input, empty/missing fields, and a couple of edge cases. Do this for each
of the 8 pages before automating anything. This is exactly what a test
plan looks like at a real company, minus the fancy formatting.

---

## Step 3 — Find your locators

Open the app in Chrome/Firefox, right-click any element → **Inspect**.
Every interactive element in this app already has a `data-testid`
attribute (e.g. `data-testid="login-submit-btn"`) — that's what you
should target in Playwright, not CSS classes or visible text (those
change more often).

Playwright's syntax for this:
```python
page.get_by_test_id("login-submit-btn").click()
```

If you can't find a `data-testid` on something you need, that's worth
noting as a small "testability" gap — a real QA engineer would flag that
to the dev team too.

---

## Step 4 — Set up your Python/Playwright environment

You've already got `venv` activated. Now:

```bash
pip install -r requirements.txt
playwright install
```

Create your first test file at `tests/test_login.py`. Start with the
**simplest possible test** to prove the wiring works end to end:

```python
def test_login_page_loads(page):
    page.goto("http://localhost:5500/login.html")
    assert page.title() == "Log in — Thistle & Oak"
```

Run it:
```bash
pytest tests/test_login.py -v
```

If that passes, you've confirmed Playwright can reach your app. Now
start turning your Step 2 test cases into real test functions, one at a
time.

---

## Step 5 — Build up gradually (suggested order)

1. `login.html` — smallest page, good for learning the basics
2. `signup.html` — practice form validation + parametrize (multiple bad emails/passwords)
3. `index.html` (product listing) — practice search/filter/pagination
4. `product.html` — practice dynamic URLs (`?id=1`)
5. `cart.html` / `checkout.html` — practice state that depends on being logged in
6. `orders.html` / `order-detail.html` — practice pagination + data verification

For pages 3 onward, you'll notice you keep repeating the same
locator definitions across tests — that's your natural cue to introduce
a **Page Object** (a Python class holding those locators + actions) in
`pages/`. Don't build the POM upfront "because you're supposed to" —
build it when you feel the repetition pain. That's how the pattern
actually clicks.

---

## Step 6 — Handle login without repeating the login form every test

Once you're a few pages in, you'll notice cart/checkout/orders tests all
need you to be logged in first. Two options, in order of how most
people naturally discover them:

1. **The obvious way:** call your login page's `login()` method at the
   start of every test that needs it. Simple, but slow and repetitive.
2. **The better way (a fixture):** write a `conftest.py` fixture that
   logs in once and returns an authenticated page, so every test that
   needs it just asks for it as a parameter. This is a natural "aha" —
   try to hit the annoyance yourself before looking at how
   `reference_solution/conftest.py` does it.

---

## Step 7 — Find and log the bugs

This app has **8 intentionally seeded bugs** and one deliberately slow
endpoint. Try to find them yourself through your own testing before
opening `docs/BUGS.md` (the answer key). For each one you find, write it
up properly:

- Summary
- Steps to reproduce
- Expected vs. actual
- Severity

Then write a test that captures/documents it (see
`reference_solution/tests/*` for the `@pytest.mark.known_bug` pattern —
worth looking at once you've found your own bugs, as an example of how
to encode "this is a known issue" into an automated test rather than
just a written report).

---

## When you're done (or stuck)

- Compare your `pages/` and `tests/` against `reference_solution/` —
  see what you did differently, not just what's "wrong."
- Use `reference_solution/docs/TEST_PLAN.md` as a template for writing
  up your own test plan once your suite is in a good place.
- Use `automation/docs/INTERVIEW_PREP.md` to practice explaining what
  you built.

Good luck — this is genuinely how the job works day-to-day.
