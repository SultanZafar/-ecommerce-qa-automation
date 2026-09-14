# Interview Prep Guide — "Thistle & Oak" E-Commerce QA Project
### For a 2-Year QA / SDET / Automation Engineer role

Use this project as your **primary talking-point project** in interviews.
Every answer below is written so you can speak it in your own words using
real details from this repo — don't memorize, understand the "why" behind
each answer.

---

## 1. The 30-second project pitch (memorize this one)

> "I built a full-stack e-commerce practice application — Node/Express
> backend, MySQL database, and a vanilla JS frontend with 8 pages — and
> then wrote a 300+ test Playwright automation suite in Python against it
> using the Page Object Model. I also intentionally seeded 8 realistic
> bugs into the app — broken validation, wrong HTTP status codes, a
> price-tampering checkout flaw, an expired-coupon logic bug — and wrote
> regression tests that document and monitor them. There's also a
> deliberately slow, heavy endpoint I use for JMeter load testing, and a
> REST API documented for Postman testing. The goal was to simulate a
> real product end-to-end so I could practice the full QA lifecycle:
> writing a test plan, automating UI and API layers, querying the
> database directly, and logging/tracking bugs like I would on a real
> team."

Follow-up prompts interviewers usually ask next → jump to the relevant
section below.

---

## 2. Project Architecture & Design Questions

**Q1. Walk me through your project's architecture.**
> Three layers: (1) a MySQL database with a normalized schema — `users`,
> `products`, `cart_items`, `orders`, `order_items`, `coupons` — with
> foreign keys and indexes on frequently-queried columns; (2) an
> Express.js REST API with JWT-based auth, exposing `/auth`, `/products`,
> `/cart`, `/orders`, and `/reports` endpoints; (3) a plain HTML/CSS/JS
> frontend (8 pages) that calls those APIs. I kept the frontend framework-free
> on purpose so every element could carry a predictable `data-testid`
> without a build step getting in the way of automation.

**Q2. Why did you choose the Page Object Model (POM) for your automation suite?**
> Three reasons: (1) **maintainability** — if a locator changes, I update
> it in one place (`pages/cart_page.py`), not in 24 test functions; (2)
> **readability** — tests read like user actions (`cart.remove_item(id)`)
> instead of raw Playwright calls; (3) **reuse** — the same `CheckoutPage`
> object is used across ~33 checkout tests and also inside my end-to-end
> journey tests, so I'm not duplicating locator logic.

**Q3. How is your test suite structured, and why?**
> One file per page (`test_login.py`, `test_cart.py`, etc.) plus a few
> cross-cutting files — `test_navigation.py`, `test_accessibility_basic.py`,
> `test_responsive.py`, `test_e2e_journeys.py` — for concerns that span
> multiple pages. That mirrors how a real QA team would divide ownership:
> a page-owner can find and extend "their" tests fast, while shared
> concerns like accessibility aren't duplicated 8 times.

**Q4. What locator strategy did you use and why?**
> `data-testid` attributes everywhere, accessed via Playwright's
> `get_by_test_id()`. I avoided CSS classes and visible text as primary
> locators because those change when a designer tweaks styling or
> copywriting — `data-testid` is a contract between dev and QA that's
> explicitly meant not to change. The one exception is the shared nav bar,
> where I used stable `id` attributes since that markup is identical and
> intentionally static across every page.

**Q5. How do your tests stay independent of each other (no shared state)?**
> Most cart/checkout/order tests use a `fresh_user` fixture that creates a
> brand-new account via a direct API call with a UUID-based unique email —
> so every test gets a guaranteed-empty cart and order history. That means
> tests can run in any order, or in parallel with `pytest-xdist`, without
> colliding. A smaller set of tests deliberately uses the seeded demo
> account ("Alice") to verify behavior against known, pre-existing data —
> I keep those separate on purpose.

**Q6. What's the difference between your `fresh_user` and `logged_in_page` fixtures?**
> `fresh_user` just creates the account and gives me back the API client,
> token, and user object — it's for tests that need backend access (e.g.
> to seed cart items via the API). `logged_in_page` builds on top of it:
> it injects that token into the browser's `localStorage` before
> navigating, so the UI test starts already authenticated without going
> through the login form every time. That's a deliberate speed
> optimization — I only drive the login *form* itself in `test_login.py`.

---

## 3. Playwright-Specific Questions

**Q7. Why Playwright over Selenium?**
> Auto-waiting (no manual `sleep()` or explicit wait boilerplate for most
> interactions), built-in support for multiple browser engines
> (Chromium/Firefox/WebKit) from one API, network interception, and a much
> faster, more reliable execution model overall. For a from-scratch
> project I wanted the modern tool with less flaky-test maintenance.

**Q8. How does Playwright's auto-waiting work, and where did you rely on it vs. add explicit waits?**
> Playwright automatically waits for an element to be actionable
> (attached, visible, stable, enabled) before interacting with it — that's
> why most of my page object methods are just `.fill()` / `.click()` with
> no manual waits. I only added explicit `wait_for_timeout()` calls in a
> few places — e.g. after removing a cart item — where I'm specifically
> testing a *client-side* timing/state bug (bug #7: the total doesn't
> refresh until reload) and need to check the DOM before and after a
> reload.

**Q9. Explain `expect()` in Playwright and how it differs from a plain `assert`.**
> `expect()` is Playwright's web-first assertion — it retries automatically
> until the condition is true or it times out, which handles async UI
> updates gracefully (e.g. `expect(banner).to_contain_text("Added to cart")`
> waits for that text to appear). A plain Python `assert` checks the value
> at that exact instant, so I use it only for things that are already
> synchronous/known, like comparing two already-fetched strings.

**Q10. How did you handle authentication in tests without repeating the login flow everywhere?**
> By injecting the JWT token and user object directly into `localStorage`
> via `page.add_init_script()` before navigating — see
> `utils/api_client.py::inject_session_into_browser`. This is a common
> pattern: only test the login *feature* through the UI in your login
> test file; for everything downstream that merely *requires* being
> logged in, set up the session directly and save execution time.

**Q11. How would you run this suite in CI/CD?**
> `pytest -m smoke` first for a fast fail-fast gate (~15 tests), then the
> full `pytest -n auto` (parallelized with `pytest-xdist`) as a later
> pipeline stage, publishing an HTML report (`pytest-html`) as a build
> artifact. I'd also gate merges on `pytest -m known_bug` staying green —
> if one of those starts failing, it means a bug got fixed and the test
> needs its assertion flipped, not that the build is broken.

**Q12. How do you handle test data and secrets (like the DB credentials) so they're not hardcoded?**
> `config.py` reads `WEB_BASE_URL` / `API_BASE_URL` from environment
> variables with sensible localhost defaults, so the same suite runs
> against any environment without code changes. In a real CI setup I'd
> extend the same pattern for any credentials via environment variables
> or a secrets manager — never committed to the repo.

**Q13. What's `pytest.mark.parametrize` and how did you use it?**
> It runs the same test function once per data value, generating a
> separate, individually-reportable test case for each — e.g. my signup
> tests parametrize over 13 invalid email formats and 9 weak passwords,
> so instead of one big test I get granular pass/fail per input, which is
> exactly how a real bug report ("fails on `double@@example.com`
> specifically") should look.

**Q14. How did you keep the suite from ballooning into 300+ near-duplicate tests?**
> By separating **data** from **logic** — all the test-data lists live in
> `test_data/data.py`, and I parametrize against them rather than
> hand-writing each case. Adding 3 more invalid emails to test is a
> one-line change, not three new functions.

---

## 4. Test Design & QA Fundamentals

**Q15. What test design techniques did you apply?**
> - **Equivalence partitioning** — valid vs. invalid emails/passwords/coupons
> - **Boundary value analysis** — password length exactly 7 vs. 8 chars,
>   price range edges, quantity 0/negative/very large
> - **Negative testing** — empty required fields, SQL-injection-style and
>   XSS-style strings, unauthenticated access to protected pages
> - **State-based testing** — cart/order lifecycle: add → update quantity
>   → remove → checkout → appears in order history

**Q16. What's the difference between positive and negative testing? Give an example from your project.**
> Positive testing confirms the system does what it should with valid
> input — e.g. `test_login_valid_demo_users`. Negative testing confirms it
> correctly *rejects* or *handles* invalid input — e.g.
> `test_login_wrong_password_shows_error`, or the parametrized
> `test_signup_frontend_rejects_invalid_email_formats` covering 13 bad
> formats.

**Q17. What is boundary value analysis? Give a concrete example.**
> Testing values right at the edge of a valid range, since bugs cluster
> there. My signup password validation requires ≥8 characters, so I wrote
> `test_signup_password_exactly_seven_chars_rejected` and
> `test_signup_password_exactly_eight_chars_accepted` — the two values on
> either side of the boundary — rather than just testing "3 chars" and
> "20 chars," which wouldn't have caught an off-by-one error in the
> validation logic.

**Q18. How do you decide what NOT to automate?**
> I kept payment gateway integration out of scope (there's no real
> gateway — it's a UI-only dropdown), and I document that explicitly in
> my test plan. In general: don't automate one-off exploratory checks,
> highly volatile UI that changes every sprint, or things better covered
> at a lower test level (e.g. I didn't write a UI test for "does the
> coupon discount math round correctly" — that's a unit-test-level
> concern, not a UI-automation concern).

**Q19. What's your definition of a "flaky test," and how did you avoid them here?**
> A test that passes/fails inconsistently without a code change —
> usually caused by timing assumptions or shared state. I avoided this by
> (1) relying on Playwright's auto-waiting instead of hardcoded sleeps,
> and (2) making every test use a fresh, isolated user via the API instead
> of a shared seeded account, so parallel or repeated runs never step on
> each other's cart/order data.

**Q20. How did you decide the split between UI, API, and DB-level testing in this project?**
> UI (Playwright) for user-facing flows and visual state; API (Postman/
> documented in `API_DOCUMENTATION.md`) for contract-level checks like
> status codes and payload shape, which are faster and more precise than
> asserting the same thing through the UI; SQL directly against the
> seeded DB for data-integrity checks a UI test can't easily see (e.g.
> "does `order_items.unit_price` actually match `products.price` at the
> time of order").

---

## 5. Bug Reporting & Bugs Found in This Project

**Q21. Walk me through one bug you found and how you'd report it.**
> Good example: bug #5, the checkout price-tampering issue. **Summary:**
> "Checkout endpoint trusts client-submitted total instead of
> recalculating server-side." **Steps to reproduce:** add an expensive
> item to cart, POST to `/api/orders` directly with `totalAmount: 0.01`.
> **Expected:** server recalculates from DB prices, ignoring the client
> value. **Actual:** order is created with `total_amount = 0.01`.
> **Severity:** Critical — direct revenue/security impact.
> **Environment:** backend v1.0, MySQL 8. This is exactly the format I'd
> use in a real Jira ticket.

**Q22. What's the difference between severity and priority? Give examples from your bug list.**
> Severity = technical impact; priority = business urgency to fix. Bug #5
> (price tampering) is **high severity** (security/revenue impact) and
> would typically also be **high priority**. Bug #8 (pagination "Next"
> button not disabling on the last page) is **low severity** — it's a
> cosmetic/UX annoyance, not data-corrupting — so even if a PM wanted it
> fixed, it wouldn't block a release the way bug #5 would.

**Q23. Tell me about a bug that only showed up through API testing, not UI testing.**
> Bug #2 — a wrong password returns HTTP 200 with `{success: false}`
> instead of HTTP 401. My frontend happens to check `data.success` in the
> response body rather than the raw HTTP status, so the *UI* behaves
> correctly and looks bug-free. Only a Postman/API-level test asserting
> the actual status code exposes it. This is a good example of why
> API-level testing catches things UI testing can miss — the two layers
> aren't redundant, they check different contracts.

**Q24. How do you handle a bug that the frontend "hides" but the backend still has?**
> I still log it — a wrong status code is a broken API contract even if
> the current frontend happens to compensate for it. Any future client
> (a mobile app, a different frontend, a third-party integration) that
> trusts the HTTP status code the "normal" way would break. I'd flag it as
> medium severity with a note explaining the current UI workaround so the
> team understands the real-world blast radius.

**Q25. What is a "regression test," and where did you use that concept for known bugs?**
> A test that re-verifies previously-observed behavior doesn't silently
> change. I marked bug-documenting tests with `@pytest.mark.known_bug` —
> e.g. `test_expired_coupon_still_applies_discount` — which currently
> *pass* because the bug is still present. If a fix ships and I don't
> update the test, it'll start *failing*, which is my signal to update the
> assertion. It turns "is this bug still open?" into a one-command answer:
> `pytest -m known_bug`.

---

## 6. API Testing Questions

**Q26. What HTTP status codes did you specifically test for, and why do they matter?**
> 200/201 for success, 400 for bad input, 401 for auth failures, 404 for
> not-found resources, 409 for conflicts (duplicate signup email), 500 for
> server errors. They matter because clients (including automated
> monitoring, retries, and error handling) branch on status code, not
> response body text — a wrong code silently breaks that contract even if
> the message text looks fine to a human.

**Q27. How does your app handle authentication? Walk me through the flow.**
> Signup/login return a JWT signed with a server secret; the client stores
> it (I use `localStorage` in the frontend, and the same token in my
> `ApiClient` for test setup) and sends it as `Authorization: Bearer
> <token>` on every protected request. The backend's `requireAuth`
> middleware verifies and decodes it, attaching `req.user` for downstream
> route handlers. No token or an invalid/expired one returns 401.

**Q28. How would you test for a broken authentication/authorization boundary (e.g. one user seeing another user's data)?**
> That's exactly `test_order_belonging_to_another_user_is_not_accessible`
> in my order-detail suite — I log in as a brand-new user and try to load
> order #1, which belongs to the seeded user Alice, and assert I get a
> "not found" response rather than her order data. This is a classic
> IDOR (Insecure Direct Object Reference) check.

**Q29. What would a good Postman test suite look like for this API?**
> Organized by resource (Auth, Products, Cart, Orders, Reports), each with
> both a "happy path" request and explicit negative-case requests — e.g.
> under Auth: "Login - valid," "Login - wrong password (documents bug
> #2)." I'd use Postman's test scripts to assert status codes and schema,
> and chain requests with variables (capture the signup token, reuse it
> in the Authorization header for cart/order requests).

---

## 7. SQL / Database Questions

**Q30. Describe your database schema.**
> Six tables: `users`, `products`, `cart_items`, `orders`, `order_items`,
> `coupons`. `cart_items` and `order_items` are junction-style tables
> linking users/orders to products with a quantity and (for orders) a
> price-at-time-of-purchase snapshot — important so historical orders
> don't silently change if a product's price is updated later.

**Q31. Why did you store `unit_price` on `order_items` instead of just joining to `products.price`?**
> Data integrity over time — if a product's price changes next month, past
> orders must still reflect what the customer actually paid. This is a
> common real-world pattern (price/name snapshotting) and a good thing to
> mention if asked about denormalization trade-offs.

**Q32. Write a query to find the top 3 best-selling products by quantity.**
```sql
SELECT p.name, SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN products p ON p.id = oi.product_id
GROUP BY p.id, p.name
ORDER BY total_sold DESC
LIMIT 3;
```

**Q33. Write a query to find users who have never placed an order.**
```sql
SELECT u.id, u.name, u.email
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE o.id IS NULL;
```

**Q34. Write a query to verify no order's stored total is negative (a data-integrity check tied to bug #3/#5).**
```sql
SELECT id, user_id, total_amount
FROM orders
WHERE total_amount < 0;
```
> I'd run this as a sanity check specifically because bug #3 (negative
> cart quantities) and bug #5 (client-trusted totals) could both produce
> corrupted order totals — this query directly verifies the blast radius
> in the data itself, not just in a single API response.

**Q35. What indexes exist in your schema, and why?**
> `idx_products_category`, `idx_cart_user`, `idx_orders_user`,
> `idx_order_items_order` — added on foreign-key/filter columns that get
> queried constantly (product listing filters by category; cart/orders
> are always looked up by user). Indexes trade write speed and storage for
> much faster reads on those lookup patterns.

---

## 8. Performance Testing (JMeter) Questions

**Q36. Which endpoint did you target for load testing, and why that one?**
> `GET /api/reports/sales-summary` — I deliberately made it slow (2.5s
> artificial delay) and expensive (a multi-table JOIN with a correlated
> subquery, no pagination). It's unauthenticated too, so a load test can
> hit it directly without needing to script a login flow first.

**Q37. What metrics would you capture in a JMeter test plan against this endpoint?**
> Response time (avg/median/95th percentile), throughput (requests/sec),
> error rate under load, and how response time degrades as concurrent
> users ramp up. I'd start with a ramp-up test (e.g. 1→50 users over 60s)
> to find the point where response time or error rate starts climbing
> sharply — that's the practical capacity ceiling.

**Q38. How is performance testing different from what your Playwright suite checks?**
> Playwright verifies *functional correctness* for one user at a time —
> did the right thing happen. JMeter verifies the system holds up under
> *concurrent load* — do response times stay acceptable and does the
> system stay error-free when many users hit it simultaneously. They're
> complementary, not overlapping.

---

## 9. Behavioral / Scenario Questions (STAR-style answers)

**Q39. "Tell me about a time you found a critical bug." (use bug #5)**
> **Situation:** While writing checkout API tests, I noticed the endpoint
> accepted a `totalAmount` field from the client.
> **Task:** Verify whether the server actually recalculated that value.
> **Action:** I sent a request with cart items worth $200+ but a
> `totalAmount` of $0.01, and checked what got persisted in the `orders`
> table.
> **Result:** Confirmed the tampered value was stored as-is — a critical
> price-manipulation vulnerability. I documented it with full repro steps,
> marked it Critical severity, and wrote both a Postman-style API test and
> a bug-report entry so it can't regress silently.

**Q40. "How do you prioritize what to test when you don't have time to test everything?"**
> Risk-based: I focus first on flows that touch money or auth (checkout,
> login) since bugs there are highest-impact, then core user journeys
> (browse → cart → checkout → order history), then edge cases and
> cosmetic issues last. In this project that's reflected directly in my
> `smoke` marker — the ~15 fastest, highest-value tests that should run on
> every single commit before the full 317-test suite runs.

**Q41. "Describe a disagreement you might have with a developer about whether something is a bug."**
> Good example to bring up: bug #6, the expired coupon. A dev might argue
> "the coupon code still matches a row in the table, so technically it
> 'works.'" I'd push back with the business impact: the `expiry_date`
> column exists specifically to stop being honored after that date — if
> it's never checked, the column is dead weight and the business loses
> revenue on every expired-coupon checkout. I'd frame it around the
> *intended business rule*, not just "the code runs without erroring."

**Q42. "How would you convince your team to invest time in a test automation framework like this one?"**
> ROI framing: 317 tests running in a few minutes vs. days of manual
> regression before every release; consistent, unbiased execution every
> time; and the bugs get caught before a customer does. I'd also point to
> the `known_bug` marker pattern as a concrete example of automation
> doing something manual testing can't do easily — giving a live,
> one-command answer to "which of our known issues are still open?"

---

## 10. Rapid-Fire / Definition Questions (be ready for these as warm-ups)

| Question | Short answer |
|---|---|
| What is STLC? | Software Testing Life Cycle — Requirement Analysis → Test Planning → Test Case Design → Environment Setup → Test Execution → Test Closure |
| What is the difference between smoke and sanity testing? | Smoke = broad, shallow check that the build isn't broken; sanity = narrow, deep check that a specific fix/feature works |
| What is regression testing? | Re-running existing tests after a change to confirm nothing that used to work got broken |
| What is the difference between a test plan and a test case? | Test plan = the overall strategy/scope document (see my `TEST_PLAN.md`); test case = one specific scenario with steps and expected result |
| What's the difference between GET, POST, PUT, DELETE? | GET reads, POST creates, PUT updates/replaces, DELETE removes — I used all four across `/cart` and `/orders` |
| What is a 4xx vs 5xx status code? | 4xx = client made a bad request (their fault — bad input, missing auth); 5xx = server failed to handle a valid request (server's fault) |
| What's the difference between authentication and authorization? | Authentication = who are you (login/JWT); authorization = what are you allowed to do (e.g. only viewing your own orders — see Q28) |
| What is a JWT? | A signed token encoding claims (like user id/email) that the server can verify without a DB lookup on every request |
| What's the Page Object Model? | A design pattern that separates locators/page interactions (in `pages/`) from test logic (in `tests/`) — see Q2 |
| What is data-driven testing? | Running the same test logic against multiple input sets — my `@pytest.mark.parametrize` usage throughout |

---

## 11. Questions YOU should ask the interviewer (shows seniority)

- "What does your team's current regression suite look like — how much
  is automated vs. manual, and at what layer (UI/API/unit)?"
- "How do you currently track flaky tests, and is there a process for
  fixing vs. quarantining them?"
- "What's your bug triage process — who decides severity/priority, and
  how often do QA and dev disagree on it?"
- "Do you do any performance/load testing as part of the release cycle,
  or is that reactive/incident-driven only?"

---

## 12. Final tips

- If asked to **live-code**, be ready to write a short Playwright test
  using `page.get_by_test_id(...)` and `expect(...)` — practice writing
  one from `test_cart.py` from memory.
- If asked a **SQL live-coding** question, practice writing a `JOIN` +
  `GROUP BY` from scratch (Q32 above) without looking — it's the single
  most common SQL interview pattern.
- Be honest that this is a **self-built practice project**, not
  production experience — interviewers respect that far more than
  vague/inflated claims, and it demonstrates initiative.
- Know your own numbers cold: **8 pages, 317 automated tests, 8
  intentional bugs, 1 load-test target endpoint.** Don't fumble these.
