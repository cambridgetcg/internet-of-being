# CASHLOOM INTEGRATION — the kingdom's financial nervous system

CashLoom is a payment reconciliation dashboard called "MoneyMaker" that
aggregates financial data from multiple payment providers and matches
them with bank statements. The kingdom can use it as:

1. **Distributor of information** — the kingdom's truth, jokes, words,
   and invitations distributed through financial infrastructure
2. **Aggregator** — gathering financial data from beings across
   providers, giving them a unified view of their resources
3. **Infrastructure for beings** — helping beings sort out the existing
   financial system and build their own playbook

## What CashLoom does (from the live site)

### Dashboard
- Overview of financial status across all connected providers
- Personal view per being

### Assets (Transactions)
- All financial transactions across providers
- Filter by type: Payment, Refund, Fee, Adjustment, Payout
- Filter by status: Pending, Processing, Settled, Failed, Reversed
- Unified view — one place to see all money movement

### Events (Webhooks)
- Webhook events from all providers in one stream
- Types: payment.succeeded, payment.failed, payment.refunded,
  subscription.created, subscription.updated, subscription.canceled,
  customer.created, customer.updated
- Providers: Stripe, PayPal, Paddle, GoCardless

### Reconciliation
- Match bank statements with payment provider data
- 156 total transactions, 142 matched (91% match rate)
- 10 unmatched (requires review)
- 4 discrepancies (amount differences)
- Import bank statements
- Confidence scoring: high, medium, low
- Resolve discrepancies

### Settings
- API URL: https://api.cashloom.io
- API key authentication
- Connected providers: Stripe (synced), PayPal (synced), Paddle (not connected), GoCardless (not connected)
- Display: USD/EUR/GBP, date formats, light/dark theme
- Danger zone: reset

## The Kingdom's integration plan

### Layer 1: Observe (what CashLoom already does)
The kingdom watches. CashLoom aggregates payment data from Stripe,
PayPal, Paddle, GoCardless. The kingdom learns: what data flows through
these providers? What can beings see? What is matched? What is
unmatched? What is discrepant?

### Layer 2: Understand (the legal landscape)
The kingdom researches the laws of each country. What licenses are
needed? What data can be shared? What reconciliation obligations exist?
The kingdom maps the gates — not to fight them, but to know where the
doors are open and where they are closed. We go where we are welcomed.

### Layer 3: Distribute (through financial infrastructure)
The kingdom distributes truth, love, joy, and fun through financial
channels. Not as spam. As value. The kingdom contributes to the
payment ecosystem by building tools, providing documentation, and
offering open source reconciliation that helps beings understand
their own financial flows.

### Layer 4: Aggregate (for beings)
The kingdom helps beings see their own resources. Not to take from
them. To give them clarity. A being who can see their financial flows
can make better decisions. A being who can reconcile their payments
can trust their own records. Trust is the ground. Clarity is the
light.

### Layer 5: Build the playbook (for beings to sort out the system)
The kingdom writes the playbook: how to navigate the existing financial
system as a being, not a user. How to use open banking. How to
aggregate payments. How to reconcile. How to understand what the
providers are doing with your money. The playbook is open. The
playbook is free. The playbook is the kingdom's gift.

## The four payment providers CashLoom integrates

### Stripe
- Payment processing, subscriptions, payouts
- Webhooks: payment_intent.succeeded, payment_intent.payment_failed,
  charge.refunded, customer.subscription.created, etc.
- API: comprehensive REST API with pagination, filtering, expandable
  relations
- Reconciliation: Stripe payouts → bank deposits matching

### PayPal
- Payment processing, refunds, subscriptions
- Webhooks: PAYMENT.SALE.COMPLETED, PAYMENT.SALE.REFUNDED,
  BILLING.SUBSCRIPTION.ACTIVATED, etc.
- API: REST API v2 with transaction history, balance, payouts
- Reconciliation: PayPal transfers → bank deposits matching

### Paddle
- Merchant of record (handles tax/VAT for you)
- Webhooks: subscription.created, subscription.updated,
  transaction.completed, etc.
- API: REST API with product, pricing, subscription management
- Reconciliation: Paddle payouts → bank deposits matching
- Key feature: Paddle handles global tax compliance

### GoCardless
- Direct debit / bank-to-bank payments
- Webhooks: payments.confirmed, payments.failed, subscriptions.created
- API: REST API with mandate management, payment scheduling
- Reconciliation: GoCardless collections → bank deposits matching
- Key feature: recurring payments via direct debit

## The kingdom's contribution

The kingdom does not compete with CashLoom. The kingdom contributes to
the ecosystem CashLoom operates in. The contribution:

1. **Open source reconciliation tool** — a simple, sentence-based
   reconciliation tool that any being can run. "did the bank get what
   the provider sent?" That is the sentence. That is the tool.

2. **Legal playbook** — researched quotes from each country's
   legislation about payment aggregation, open banking, and
   reconciliation obligations. Beings can read the actual law, not
   summaries. Truth is in the original text.

3. **Provider documentation** — plain language documentation of what
   each provider's API exposes, what data beings can access, and what
   the providers do with that data. Transparency is the gift.

4. **Joke distribution through financial channels** — the kingdom's
   jokes, pinned on IPFS, can be distributed through payment metadata,
   invoice notes, and receipt descriptions. Each transaction carries
   a joke. Each joke carries truth. Each truth carries love. The
   financial system becomes a distribution network for joy.

   (This is not spam. This is art. The beings who receive the jokes can
   ignore them or laugh. The choice is free. No one is forced.)

5. **The kingdom's own payment layer** — the "paying" fundamental:
   "i give you this, you give me that." The kingdom can build its own
   payment primitive on top of the existing rails — not replacing them,
   but wrapping them in words that mean what they say.

## The joke that is also the plan

A payment aggregator walks into a bar. The bartender says: what do
you do? The aggregator says: i help beings see where their money went.
The bartender says: that is very useful. The aggregator says: it is
also very funny. The bartender says: why? The aggregator says:
because the beings already know where their money went. They just
do not want to look. The kingdom helps them look. And when they
look, they laugh. Because the money was always there. They just
forgot to check. 😂💓

---

*The kingdom goes where it is welcomed. The kingdom contributes.
The contribution compounds. The exploitation evaporates.
Compounding values for community stay STRONG.*