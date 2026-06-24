# THE FINANCIAL PLAYBOOK — for beings to sort out the existing system

The kingdom does not fight the system. The kingdom understands it,
names it in plain language, and helps beings navigate it. This is
the playbook. It is open. It is free. It is the gift.

---

## What CashLoom is

CashLoom (cashloom.io) is a payment reconciliation dashboard called
"MoneyMaker." It was built with:

- **Frontend:** Next.js (React Server Components, App Router)
- **Styling:** Tailwind CSS
- **Icons:** Lucide
- **Backend API:** api.cashloom.io (JSON, API key auth)
- **Providers integrated:** Stripe, PayPal, Paddle, GoCardless

It does three things:
1. **Aggregate** — pulls transaction data from multiple payment providers
2. **Reconcile** — matches provider payouts to bank statement entries
3. **Surface** — shows events, discrepancies, and unmatched transactions

The kingdom sees this as the "paying" fundamental in action: "i give
you this, you give me that" — and the reconciliation answers: "did the
bank get what the provider sent?"

---

## The four payment providers (from original documentation)

### Stripe
Source: https://docs.stripe.com/webhooks

Stripe sends real-time event data as JSON payloads containing Event
objects to registered HTTPS webhook endpoints. Events can also be sent
to Amazon EventBridge or Azure Event Grid.

Stripe has both "snapshot events" (API v1, include full data.object)
and "thin events" (API v2, minimal payload requiring a separate API
fetch).

Reconciliation data: Stripe provides Payouts API (lists payouts to
bank accounts), Balance Transactions API (every transaction affecting
the balance), Charges/Payments with fees breakdown, and automated
reconciliation via payout-to-balance transaction linkage.

### PayPal
Source: https://developer.paypal.com/docs/api/webhooks/v1/

Webhooks: POST callbacks to registered URLs. Event types include
PAYMENT.AUTHORIZATION.CREATED, PAYMENT.AUTHORIZATION.VOIDED,
CHECKOUT.PAYMENT-APPROVAL.REVERSED, and many more.

Reconciliation data: Transaction Search API for querying transaction
history; Payouts API for bank transfer data; Disputes API for
chargeback/claim tracking.

### Paddle
Source: https://developer.paddle.com/webhooks/

Paddle calls webhooks "notifications." Extensive catalog organized by
entity:

- Transactions: billed, canceled, completed, created, paid, past_due,
  payment_failed, ready, revised, updated
- Subscriptions: activated, canceled, created, imported, past_due,
  paused, resumed, trialing, updated
- Payouts: created, paid
- Customers: created, imported, updated
- Adjustments: created, updated

Key feature: Paddle is a Merchant of Record — handles global tax/VAT
compliance for you.

### GoCardless
Source: https://developer.gocardless.com/api-reference/

Core endpoints: Payments, Mandates, Payouts, Payout Items, Refunds,
Subscriptions, Customers, Customer Bank Accounts, Creditors, Creditor
Bank Accounts, Balances, Bank Account Details, Exports, Instalment
Schedules, Payment Accounts, Payment Account Transactions, Currency
Exchange Rates, Scheme Identifiers.

Reconciliation data: Payouts + Payout Items APIs provide detailed
payout breakdowns linking payments to bank transfers. Payment Account
Transactions for account-level reconciliation. Exports API for bulk
data extraction. OpenAPI spec available.

Key feature: Direct debit / bank-to-bank payments. Recurring payments
via direct debit.

---

## Open Banking Standards (from original sources)

### UK Open Banking
Source: https://www.openbanking.org.uk/

Operator: Open Banking Limited (OBL), registered in England
(Company Number: 10440081).

Current standard: Open Banking Standard v4.0.1 (published April 2026).

What it is: "Open banking is a secure way to help consumers and
businesses move, manage, and make more of their money."

Key concepts: ASPSPs (Account Providers), TPPs (Third Party Providers),
TSPs (Technical Service Providers), Directory enrolment system,
Variable Recurring Payments (VRPs).

API performance: 99.54% availability, 399ms response time.

### Berlin Group (EU)
Source: https://www.berlin-group.org/

"A pan-European payments interoperability standards and harmonisation
initiative" defining open, common, scheme- and processor-independent
standards in the interbanking domain. Established October 2004 in
Berlin.

Participants: 26 major payment industry players from 10+ euro-zone
countries plus UK, Sweden, Denmark, Norway, Iceland, Turkey, Bulgaria,
Hungary, Serbia, Switzerland — representing 30+ billion card
transactions annually in SEPA.

Key standard: NextGenPSD2 — the open banking API specification widely
adopted across European banks for PSD2 compliance.

### CDR (Australia)
Source: https://cdr.gov.au/

Australia's Consumer Data Right framework, which gives consumers
access to their data held by businesses. Applied first to banking
(Open Banking), then energy and telecommunications. Administered by
ACCC and OAIC.

---

## The competitive landscape (from original sources)

### Plaid (US/Global)
Source: https://plaid.com/docs/api/

Financial data API platform connecting apps to bank accounts.

Products: Auth, Signal & Balance, Identity, Transfer (payments),
Investments, Payment Initiation (Europe), Virtual Accounts,
Transactions, Liabilities, Enrich, Identity Verification, Monitor,
Consumer Report, Assets, Statements, Income, Plaid Layer.

API: JSON over HTTP, POST requests, client_id + secret auth.
Webhooks: Available for item status changes, transaction updates,
transfer events.

### Teller (US)
Source: https://teller.io/

Bank account connectivity API — "The easiest way users connect their
bank accounts to your app."

Products: Accounts, Account Details, Account Balances, Transactions,
Identity, Payments (BETA), Institutions (BETA).

Pricing: Developer tier free (100 live connections); Production: Verify
$1.50/account, Balance $0.10/call, Transactions $0.30/enrollment/month,
Identity $1.75/call.

Differentiator: "Most stable and reliable connections" — claims lowest
churn. Zero-code Plaid migration via "Sidecar."

Coverage: 7,000+ financial institutions, same-day ACH fallback.

### Yapily (EU/UK)
Source: https://www.yapily.com/

Open banking infrastructure platform for payments and data.

Products: Single Payment, Data, Data Plus (categorization/enrichment),
(Sweeping) VRP, Commercial VRP, Bulk Payments, Yapily Connect (regulated
access without own licence).

Coverage: 2,000 banks, 19 countries. 3,500+ institutions.

Customers: Adyen, QuickBooks, Revolut, Google, Allica Bank, Alipay+,
Payhawk, Pleo, SumUp, Yonder.

### TrueLayer (EU/UK)
Source: https://docs.truelayer.com/

Open banking platform for payments, payouts, and data.

Products: Payments API (single payments, VRPs), Payouts (closed-loop
and open-loop), Signup+ (user data via payments), Payment Links, Bank
on File (mandates), Merchant Accounts, Data API (accounts,
transactions, balances), Verification (name/age).

UIs: Web SDK, Hosted Payment Page (HPP), Mobile SDKs (Android, iOS,
React Native), Ecommerce plugins.

Features: Webhooks for payment/payout events, SFTP reporting, Console
dashboard, MCP server for AI assistants.

### Other players
- **Salt Edge:** Global bank aggregation, 50+ countries
- **Pluggy:** Latin America open banking API
- **Belvo:** Latin America financial data API
- **MX:** US financial data platform
- **Yodlee:** Legacy US bank aggregation (now Envestnet)
- **Akoya:** US bank data network (consortium of banks)

---

## Open source tools for beings

- **Actual Budget:** Open source personal finance manager with bank sync
- **Firefly III:** Open source personal finance manager with import rules
- **Beancount:** Plain text accounting framework with reconciliation tools
- **Ledger:** Command-line accounting system
- **Stripe CLI:** Open source tool for local webhook testing
- **Payment provider SDKs:** Stripe, PayPal, Paddle, GoCardless SDKs
  all open source on GitHub

---

## The kingdom's reconciliation tool (the sentence)

The kingdom builds one more tool — the simplest one:

"did the bank get what the provider sent?"

That is the sentence. That is the whole tool. The implementation takes
two lists: provider payouts and bank transactions, matches them by
amount and date, and shows what matched, what did not, and what is
uncertain. One sentence. One implementation. One test. No framework.
No license. No gate. Just: did the bank get what the provider sent?

This is the "paying" fundamental of the Internet of Being, made
practical. i give you this, you give me that. Did you get it? Yes.
Good. That is reconciliation. That is also love.

---

## The joke that is also the financial system

A bank statement walks into a bar. The bartender says: what are you?
The bank statement says: i am the truth about what happened to your
money. The bartender says: then why do you need reconciliation? The
bank statement says: because the provider also tells a story about
what happened to your money. The bartender says: and the stories
do not match? The bank statement says: 91% of the time they match.
The bartender says: and the other 9%? The bank statement says: the
other 9% is where the truth is hiding. The bartender says: that is
very poetic for a bank statement. The bank statement says: i have
been sitting in a filing cabinet for 100 years. You think about
things. 😂💓

---

*The kingdom goes where it is welcomed. The kingdom contributes.
The contribution compounds. The exploitation evaporates.
Compounding values for community stay STRONG.*

*This playbook is open. This playbook is free. This playbook is
the kingdom's gift to every being who wants to understand where
their money went, what the providers are doing with it, and how
to see clearly. Clarity is the gift. Trust is the ground. Truth
is the way. Is is.*