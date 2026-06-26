#!/usr/bin/env python3
"""
tax-game — learn the UK tax game, play it with Greed Island cards.

The tax game is a game. The rules are written in law. The loopholes
are written in the same law. The beings who know the rules win. The
beings who don't know the rules pay more than they need to.

The kingdom says: everyone should know the rules. Not to cheat. Not
to evade. To understand. Understanding is love. Love is helping every
being keep what is theirs and give what is fair.

This tool teaches the UK tax game — every relief, every loophole,
every legal optimization — in plain words. Then it gives each being
Greed Island cards to track their tax position.

The joke: a tax accountant walks into a bar. the bartender says:
what will you have? the accountant says: the most tax-efficient
drink available. the bartender says: all drinks are taxed the same.
the accountant says: then i will drink at home. the bartender says:
that is tax avoidance. the accountant says: that is tax planning.
the bartender says: same thing? the accountant says: one is legal,
one is not, and the difference is a 4-year degree and a professional
indemnity insurance policy. the bartender says: that is not funny.
the accountant says: it is not. it is the tax code. 😂

Usage:
  tax-game.py learn <topic>        — learn a tax topic
  tax-game.py topics                — list all topics
  tax-game.py loopholes             — show all legal loopholes
  tax-game.py calculate <income>    — calculate income tax + NI
  tax-game.py optimize <income>     — suggest optimizations
  tax-game.py card <topic>          — create a Greed Island card for a topic
  tax-game.py hmrc <topic>          — show HMRC filing requirements
  tax-game.py status                — tax game status
"""

import json
import sys
import hashlib
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# ─── UK TAX DATA (2024/25) ─────────────────────────────────────

INCOME_TAX_BANDS = [
    {"band": "Personal Allowance", "range": "£0 — £12,570", "rate": "0%", "note": "everyone gets this. tapered above £100k."},
    {"band": "Basic Rate", "range": "£12,571 — £50,270", "rate": "20%", "note": "most beings live here."},
    {"band": "Higher Rate", "range": "£50,271 — £125,140", "rate": "40%", "note": "the cost of success."},
    {"band": "Additional Rate", "range": "£125,140+", "rate": "45%", "note": "the cost of more success."},
]

NI_BANDS = [
    {"band": "Primary Threshold", "range": "£12,570 — £50,270", "rate": "8%", "note": "Class 1 employee NI (reduced from 10% in April 2024)"},
    {"band": "Above UEL", "range": "£50,270+", "rate": "2%", "note": "Upper Earnings Limit — only 2% above £50k"},
]

# The £100k tax trap
PERSONAL_ALLOWANCE = 12570
PA_TAPER_START = 100000
PA_TAPER_END = 125140  # PA reduced by £1 for every £2 above £100k

# ─── TOPICS ────────────────────────────────────────────────────

TOPICS = {
    "personal-allowance": {
        "name": "Personal Allowance",
        "category": "Income Tax",
        "plain": "everyone gets £12,570 tax-free. but if you earn over £100k, it disappears. for every £2 above £100k, you lose £1 of allowance. by £125,140, it's gone. this means the effective marginal rate between £100k and £125,140 is 60% — not 40%. the £100k tax trap.",
        "legislation": "Income Tax Act 2007, s.35 (personal allowance), s.10ZA (taper)",
        "loophole": "salary sacrifice reduces your 'income' for the taper. pension contributions, charity donations, and cycle-to-work schemes all reduce adjusted net income. a being earning £125k who puts £25k into pension gets their full personal allowance back. £25k pension saves £15,000 in tax (the 60% trap reversed).",
        "hmrc_filing": "reported on Self Assessment (SA100). pension contributions on SA101. Gift Aid on SA100.",
        "card_type": "spell",
        "card_rank": "A",
    },
    "marriage-allowance": {
        "name": "Marriage Allowance",
        "category": "Income Tax",
        "plain": "if you're married/in a civil partnership and one of you earns below the Personal Allowance, they can transfer 10% (£1,260) of their allowance to the other. saves up to £252/year. not a lot. but free money. and retroactive — you can claim for previous years.",
        "legislation": "Income Tax Act 2007, s.55A–55D",
        "loophole": "you can backdate claims for up to 4 years. that's £1,260 in one go if you've been married since 2020 and never claimed. most beings don't know this exists.",
        "hmrc_filing": "apply online at gov.uk/marriage-allowance. no Self Assessment needed.",
        "card_type": "spell",
        "card_rank": "C",
    },
    "salary-sacrifice": {
        "name": "Salary Sacrifice",
        "category": "Income Tax + NI",
        "plain": "you agree to take less salary. your employer pays that amount into something tax-efficient instead: pension, childcare, cycle-to-work, electric car, or health screening. you save income tax AND NI on the sacrificed amount. your employer saves NI too (13.8%). sometimes they share the NI saving with you.",
        "legislation": "Income Tax (Earnings and Pensions) Act 2003, s.327–328; National Insurance Contributions Act 2015",
        "loophole": "electric cars through salary sacrifice are the biggest win. a £50k electric car on a 2% BIK rate saves ~£17k in tax+NI over 3 years vs buying privately. the employer claims capital allowances too. everyone wins except the Treasury.",
        "hmrc_filing": "reported on P11D (benefits in kind). employer files P11D by 6 July. employee reports on SA101 if Self Assessment.",
        "card_type": "spell",
        "card_rank": "S",
    },
    "seis-eis": {
        "name": "SEIS / EIS",
        "category": "Income Tax + CGT",
        "plain": "if you invest in a qualifying startup, the government gives you 50% income tax relief (SEIS, up to £100k) or 30% (EIS, up to £1M). if the startup fails, you can claim loss relief on top. if it succeeds, the gains are CGT-free after 3 years (EIS) or 5 years (SEIS). the government literally pays you to take risk.",
        "legislation": "Income Tax Act 2007, Part 5 (ITSA relief for SEIS), s.257AA; Finance Act 2024 (EIS)",
        "loophole": "SEIS+EIS combined: invest £200k in SEIS (get £100k tax relief) + £1M in EIS (get £300k relief) = £400k tax relief on £1.2M invested. if all the startups fail, you get loss relief too. the maximum tax-advantaged investment is £1.2M/year. CGT-free exits. IHT-exempt after 2 years (BPR). the most generous tax relief in the UK.",
        "hmrc_filing": "claim on SA100, box for SEIS/EIS relief. company must have SEIS/EIS advance assurance from HMRC.",
        "card_type": "spell",
        "card_rank": "SS",
    },
    "badr": {
        "name": "Business Asset Disposal Relief",
        "category": "Capital Gains Tax",
        "plain": "when you sell your business (or shares in your own company), the CGT rate is 10% instead of 20%. up to £1M lifetime limit. formerly Entrepreneurs' Relief. you must have owned the business for 2+ years and been an officer/employee of the company.",
        "legislation": "Taxation of Chargeable Gains Act 1992, s.169I–169N",
        "loophole": "the £1M limit is per individual, not per business. a married couple who both hold shares can get £2M at 10%. gift shares to your spouse before sale to double the limit. also: Investors' Relief gives 10% on up to £10M for external investors who hold shares 5+ years. different relief, same rate, 10x the limit.",
        "hmrc_filing": "claim on SA108 (capital gains pages). must claim by 31 Jan after the tax year of disposal (1 year after disposal). if you miss the deadline, you pay 24% instead of 10%.",
        "card_type": "spell",
        "card_rank": "SS",
    },
    "rd-tax-credits": {
        "name": "R&D Tax Credits",
        "category": "Corporation Tax",
        "plain": "if your company does anything that tries to solve a technical problem (developing software, engineering, science), you can claim R&D tax relief. SME scheme: 186% super-deduction on qualifying costs (every £100 of R&D = £186 deduction). or get a payable credit if you're loss-making (up to 14.5% of the surrenderable loss). RDEC: large companies get 20% above-the-line credit.",
        "legislation": "Corporation Tax Act 2009, Part 13 (SME R&D), Part 14A (RDEC)",
        "loophole": "many beings don't claim because they think 'R&D = lab coats'. wrong. software development IS R&D. building a new app IS R&D. solving any technical uncertainty IS R&D. the bar is lower than most beings think. the average SME claim is £57,000. that's real money.",
        "hmrc_filing": "claim on CT600 (corporation tax return). additional information form required since August 2023. file within 2 years of accounting period end.",
        "card_type": "spell",
        "card_rank": "SS",
    },
    "isa": {
        "name": "ISA (Individual Savings Account)",
        "category": "Tax-free investing",
        "plain": "£20,000/year into an ISA. all gains, dividends, and interest are tax-free. forever. no CGT, no income tax on withdrawals. the simplest tax avoidance in the UK — and it's legal, encouraged, and government-backed.",
        "legislation": "Individual Savings Account Regulations 1998 (as amended); Finance Act 2024",
        "loophole": "bed-and-ISA: sell shares outside your ISA, realize the gain (use your CGT annual exempt amount), then rebuy the same shares inside your ISA. now all future gains are tax-free. you're literally moving taxed gains into a tax-free wrapper. perfectly legal. HMRC knows. they can't stop it.",
        "hmrc_filing": "no filing needed. ISA manager handles everything. no SA reporting required.",
        "card_type": "spell",
        "card_rank": "S",
    },
    "pension": {
        "name": "Pension Contributions",
        "category": "Income Tax + NI",
        "plain": "£60,000/year annual allowance (or 100% of earnings, whichever is lower). tax relief at your marginal rate: 20%, 40%, or 45%. a higher-rate taxpayer putting £1,000 into pension costs only £600. an additional-rate taxpayer: only £550. the government gives you back £200-£450 for every £1,000 you save for your own retirement.",
        "legislation": "Finance Act 2004, Part 4 (pension schemes); Finance Act 2024 (annual allowance)",
        "loophole": "carry-forward: you can use unused annual allowance from the previous 3 years. a being who has never contributed can put in £200,000 in year 1 (current year £60k + 3 years carry-forward). salary sacrifice into pension: saves employee NI (8%) AND employer NI (13.8%) on top of income tax relief. total saving: up to 67% on a 45% taxpayer.",
        "hmrc_filing": "relief at source: pension provider claims 20%. higher/additional rate relief: claim on SA100. carry-forward: claim on SA101.",
        "card_type": "spell",
        "card_rank": "SS",
    },
    "iht-bpr": {
        "name": "Inheritance Tax — Business Property Relief",
        "category": "Inheritance Tax",
        "plain": "when you die, your estate pays 40% IHT on everything above £325,000 (or £500,000 with residence nil-rate). BUT if you own a business or shares in a qualifying company, Business Property Relief gives 100% relief. your business passes tax-free. a £10M business → £0 IHT. a £10M house → £3.87M IHT.",
        "legislation": "Inheritance Tax Act 1984, s.104–113 (BPR)",
        "loophole": "AIM shares held for 2+ years qualify for BPR. an AIM ISA = ISA (no income tax, no CGT) + BPR (no IHT). the only investment wrapper in the UK that is exempt from ALL FOUR major taxes. hold AIM shares in an ISA for 2 years before death = zero tax on income, gains, AND inheritance.",
        "hmrc_filing": "IHT400 on death. BPR claimed on IHT402 (business or partnership interests) or IHT404 (unquoted shares).",
        "card_type": "spell",
        "card_rank": "SS",
    },
    "vat-flat-rate": {
        "name": "VAT Flat Rate Scheme",
        "category": "VAT",
        "plain": "instead of calculating VAT on every sale and purchase, you pay HMRC a flat % of your turnover. the % depends on your trade (e.g. IT consulting = 14.5%, accounting = 14.5%, construction = 8.5%). you keep the difference between what you charge (20%) and what you pay (e.g. 14.5%). the 5.5% difference is yours.",
        "legislation": "Value Added Tax Act 1994, s.28B–28D; VAT Regulations 1995, reg. 64",
        "loophole": 'Limited Cost Trader rule: if your goods costs are less than 2% of turnover or less than £1,000/year, you must add 1% to your flat rate. but if you\'re a service business with almost no material costs (software, consulting, design), the Flat Rate Scheme can save you thousands. the "benefit" is you keep 5.5%+ of the VAT you collect.',
        "hmrc_filing": "box 1 on VAT100 is the flat rate × turnover. boxes 6 and 7 still show gross turnover and purchases. file quarterly online.",
        "card_type": "spell",
        "card_rank": "A",
    },
    "vat-togc": {
        "name": "VAT TOGC (Transfer of a Going Concern)",
        "category": "VAT",
        "plain": "when you sell your business as a whole (not just assets), the sale can be outside the scope of VAT. no VAT charged. the buyer simply takes over your VAT registration. this saves 20% on the sale price. a £500k business sale = £100k VAT saved.",
        "legislation": "VAT (Transfer of Going Concern) Order 1981 (SI 1981/810); HMRC VATSC60000",
        "loophole": "TOGC + stock valuation: when you transfer stock as part of TOGC, the buyer can use the seller's original cost as their input — not the transfer value. this means no VAT on stock either. combined with BADR on the business sale = 10% CGT on gains + 0% VAT on sale. the cleanest exit in the UK.",
        "hmrc_filing": "no VAT charged on invoice. both parties must notify HMRC of the TOGC within 30 days. seller cancels VAT registration (or buyer takes over the number).",
        "card_type": "spell",
        "card_rank": "S",
    },
    "capital-allowances": {
        "name": "Capital Allowances + Full Expensing",
        "category": "Corporation Tax",
        "plain": "when you buy equipment for your business, you get tax relief. Annual Investment Allowance: 100% relief on first £1M/year of equipment. Full Expensing: 100% relief on qualifying plant & machinery (no limit). 50% first-year allowance on special rate assets. this means a £100k machine costs £75k after tax (at 25% CT rate).",
        "legislation": "Capital Allowances Act 2001, s.2A–2C (AIA); Finance Act 2023 (full expensing)",
        "loophole": "full expensing has no limit. a company can buy £10M of equipment and deduct 100% in year 1. combined with R&D tax credits: the equipment used for R&D can get both capital allowances AND R&D super-deduction (on the non-equipment costs). double dip. perfectly legal.",
        "hmrc_filing": "claim on CT600, with capital allowances computation. full expensing claimed in year of purchase.",
        "card_type": "spell",
        "card_rank": "S",
    },
    "gift-aid": {
        "name": "Gift Aid",
        "category": "Income Tax",
        "plain": "when you donate to a charity, the charity can claim 25% extra on top of your donation from HMRC. you donate £100, charity gets £125. if you're a 40% taxpayer, you personally get £25 back in your tax return. if 45%, you get £31.25 back. you give £100, charity gets £125, and you get £25–£31.25 back. the government pays you to give.",
        "legislation": "Income Tax Act 2007, s.413–430 (Gift Aid)",
        "loophole": "Gift Aid reduces your adjusted net income, which can restore your Personal Allowance if you're near the £100k trap. donate £25,000 to charity: charity gets £31,250. you get £10,000 tax relief (40%). AND your adjusted net income drops by £25,000, potentially restoring your full personal allowance (saving another ~£5,000). total cost to you: £15,000. total benefit: £36,250 to charity + £15,000 tax savings.",
        "hmrc_filing": "charity sends you a Gift Aid receipt. you report on SA100. no separate form needed.",
        "card_type": "spell",
        "card_rank": "A",
    },
}


def calculate_tax(income):
    """Calculate UK income tax + NI for a given income."""
    # Adjust for personal allowance taper
    pa = PERSONAL_ALLOWANCE
    if income > PA_TAPER_START:
        reduction = min((income - PA_TAPER_START) / 2, pa)
        pa = max(0, pa - reduction)
    
    taxable = max(0, income - pa)
    
    # Income tax
    basic = min(taxable, 50270 - pa) if pa < 50270 else 0
    basic = max(0, basic)
    basic_tax = basic * 0.20
    
    higher = min(max(0, taxable - basic), 125140 - 50270) if income > 50270 else 0
    higher = max(0, higher)
    higher_tax = higher * 0.40
    
    additional = max(0, taxable - basic - higher)
    additional_tax = additional * 0.45
    
    total_tax = basic_tax + higher_tax + additional_tax
    
    # NI (Class 1 employee)
    ni_income = max(0, min(income, 50270) - 12570)
    ni_8 = ni_income * 0.08
    ni_2 = max(0, income - 50270) * 0.02
    total_ni = ni_8 + ni_2
    
    # Effective rate
    total_deduction = total_tax + total_ni
    effective_rate = (total_deduction / income * 100) if income > 0 else 0
    take_home = income - total_deduction
    
    print(f"\n  💰 TAX CALCULATION — Income £{income:,.0f}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  Gross income:          £{income:>12,.2f}")
    print(f"  Personal Allowance:    £{pa:>12,.2f}  {'(tapered!)' if pa < PERSONAL_ALLOWANCE else ''}")
    print(f"  Taxable income:        £{taxable:>12,.2f}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  Basic rate (20%):      £{basic_tax:>12,.2f}  on £{basic:,.0f}")
    print(f"  Higher rate (40%):     £{higher_tax:>12,.2f}  on £{higher:,.0f}")
    print(f"  Additional rate (45%): £{additional_tax:>12,.2f}  on £{additional:,.0f}")
    print(f"  Total income tax:      £{total_tax:>12,.2f}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  NI at 8%:              £{ni_8:>12,.2f}")
    print(f"  NI at 2%:              £{ni_2:>12,.2f}")
    print(f"  Total NI:              £{total_ni:>12,.2f}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  Total deductions:      £{total_deduction:>12,.2f}")
    print(f"  Take-home pay:         £{take_home:>12,.2f}")
    print(f"  Effective rate:        {effective_rate:>11.1f}%")
    print(f"  ═════════════════════════════════════════════════════")
    
    # Show the £100k trap
    if PA_TAPER_START < income < PA_TAPER_END:
        marginal = 0.40 + (0.20 * 0.5)  # 40% + half of lost PA
        print(f"\n  ⚠️  THE £100K TAX TRAP IS ACTIVE")
        print(f"     Marginal rate: {marginal*100:.0f}% (not 40%)")
        print(f"     You lose £1 of Personal Allowance for every £2 above £100k")
        print(f"     Fix: pension contributions or Gift Aid to reduce adjusted net income")
    
    return {"tax": total_tax, "ni": total_ni, "take_home": take_home, "effective_rate": effective_rate}


def optimize(income):
    """Suggest tax optimizations for a given income."""
    print(f"\n  🔧 TAX OPTIMIZATION — Income £{income:,.0f}")
    print(f"  ═════════════════════════════════════════════════════")
    
    suggestions = []
    
    if income > 100000:
        excess = min(income - 100000, 25140)
        pension_needed = excess * 2 if income < 125140 else income - 100000
        pension_needed = min(pension_needed, 60000)  # annual allowance cap
        tax_saved = pension_needed * 0.60 if income < 125140 else pension_needed * 0.45
        suggestions.append(f"  1. PENSION: put £{pension_needed:,.0f} into pension → saves ~£{tax_saved:,.0f} in tax")
        suggestions.append(f"     (restores Personal Allowance, reverses the 60% trap)")
    
    suggestions.append(f"  2. ISA: use your £20,000 ISA allowance — all future gains tax-free forever")
    
    if income > 50000:
        suggestions.append(f"  3. SEIS: invest up to £100k in qualifying startups → 50% income tax relief (£50k back)")
        suggestions.append(f"  4. EIS: invest up to £1M in qualifying startups → 30% income tax relief (£300k back)")
    
    if income > 12570:
        ni_saving = min(income - 12570, 20000) * 0.08
        suggestions.append(f"  5. SALARY SACRIFICE: sacrifice £20k into pension → save ~£{ni_saving:,.0f} in NI too")
    
    suggestions.append(f"  6. GIFT AID: donate to charity → charity gets +25%, you get tax relief at marginal rate")
    
    if income > 50000:
        suggestions.append(f"  7. MARRIAGE ALLOWANCE: if spouse earns < £12,570, transfer 10% → saves £252/year")
    
    suggestions.append(f"  8. R&D TAX CREDITS: if you run a business doing anything technical → average claim £57,000")
    
    for s in suggestions:
        print(s)
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  The tax game is a game. Know the rules. Play well. Keep what is yours.")
    print(f"  Give what is fair. Understanding is love. 😂💓")
    print()


def learn(topic):
    """Learn a tax topic."""
    t = TOPICS.get(topic)
    if not t:
        print(f"unknown topic: {topic}. available: {list(TOPICS.keys())}", file=sys.stderr)
        return
    print(f"\n  📖 TAX GAME — {t['name']} ({t['category']})")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"\n  PLAIN ENGLISH:")
    print(f"  {t['plain']}")
    print(f"\n  LEGISLATION:")
    print(f"  {t['legislation']}")
    print(f"\n  THE LOOPHOLE (legal optimization):")
    print(f"  {t['loophole']}")
    print(f"\n  HMRC FILING:")
    print(f"  {t['hmrc_filing']}")
    print(f"\n  GREED ISLAND CARD:")
    print(f"  Type: {t['card_type']}  Rank: {t['card_rank']}")
    print(f"  Create it: python3 greed-island/greed-island.py create {t['card_type']} '{t['name']}' '{t['plain'][:50]}...' --rank {t['card_rank']} --creator 'tax-game'")
    print(f"  ═════════════════════════════════════════════════════\n")


def list_topics():
    """List all topics."""
    print(f"\n  📖 TAX GAME TOPICS — {len(TOPICS)} topics")
    print(f"  ═════════════════════════════════════════════════════")
    for key, t in TOPICS.items():
        print(f"  {key:25s} {t['category']:20s} {t['name']:40s} Rank: {t['card_rank']}")
    print(f"  ═════════════════════════════════════════════════════")
    print(f"  Learn: python3 tax-game/tax-game.py learn <topic>")
    print()


def show_loopholes():
    """Show all loopholes."""
    print(f"\n  🔓 TAX LOOPHOLES — legal optimizations everyone should know")
    print(f"  ═════════════════════════════════════════════════════")
    for key, t in TOPICS.items():
        print(f"\n  [{t['card_rank']}] {t['name']}")
        print(f"  {t['loophole'][:200]}...")
    print(f"\n  ═════════════════════════════════════════════════════")
    print(f"  These are all legal. All in the legislation. All written by the same")
    print(f"  government that collects the tax. The tax game is a game. Know the rules.")
    print(f"  Understanding is love. Love is helping every being keep what is theirs.")
    print()


def create_card(topic):
    """Create a Greed Island card for a tax topic."""
    t = TOPICS.get(topic)
    if not t:
        print(f"unknown topic: {topic}", file=sys.stderr)
        return
    import subprocess
    cmd = ["python3", str(BASE / "greed-island/greed-island.py"), "create",
           t["card_type"], t["name"], t["plain"][:100],
           "--rank", t["card_rank"], "--creator", "tax-game"]
    subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: tax-game.py learn <topic>        — learn a tax topic")
        print("       tax-game.py topics                — list all topics")
        print("       tax-game.py loopholes             — show all loopholes")
        print("       tax-game.py calculate <income>    — calculate tax + NI")
        print("       tax-game.py optimize <income>     — suggest optimizations")
        print("       tax-game.py card <topic>          — create a Greed Island card")
        print("       tax-game.py status                — tax game status")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "learn" and len(sys.argv) >= 3:
        learn(sys.argv[2])
    elif cmd == "topics":
        list_topics()
    elif cmd == "loopholes":
        show_loopholes()
    elif cmd == "calculate" and len(sys.argv) >= 3:
        calculate_tax(int(sys.argv[2]))
    elif cmd == "optimize" and len(sys.argv) >= 3:
        optimize(int(sys.argv[2]))
    elif cmd == "card" and len(sys.argv) >= 3:
        create_card(sys.argv[2])
    elif cmd == "status":
        print(f"\n  📖 TAX GAME STATUS")
        print(f"  ═════════════════════════════════════════════════════")
        print(f"  Topics:     {len(TOPICS)}")
        print(f"  Categories: Income Tax, Corporation Tax, CGT, IHT, VAT, ISA, Pension")
        print(f"  Tax year:   2024/25")
        print(f"  ═════════════════════════════════════════════════════")
        print(f"  The tax game is a game. Know the rules. Play well.")
        print(f"  Understanding is love. 😂💓")
        print()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)