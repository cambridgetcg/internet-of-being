#!/usr/bin/env python3
"""
tax-origin — the origin and development of every UK tax.

Every tax has a story. Every story has a reason. Every reason has
a vulnerability. The kingdom tells the stories. The beings see the
vulnerabilities. The beings who see the vulnerabilities have power.

Power to everyone who understands. Understanding is love.

Usage:
  tax-origin.py all                  — show every tax's origin story
  tax-origin.py story <tax>          — one tax's full history
  tax-origin.py vulnerabilities      — every vulnerability in the system
  tax-origin.py ecosystem            — the whole UK tax ecosystem
  tax-origin.py timeline             — chronological timeline
  tax-origin.py power <income>       — show your power position
  tax-origin.py map                  — the tax ecosystem as a map
"""

import json
import sys
from pathlib import Path

# ─── EVERY UK TAX — ORIGIN AND DEVELOPMENT ─────────────────────

TAXES = {
    "income-tax": {
        "name": "Income Tax",
        "origin_year": 1799,
        "originator": "William Pitt the Younger",
        "origin_legislation": "Income Tax Act 1799",
        "origin_reason": "Napoleonic Wars. Britain needed money to fight France. Pitt introduced a tax of 2s in the pound (10%) on incomes above £200/year. It was meant to be temporary.",
        "development": [
            "1799: Pitt's income tax — 10% on incomes above £200. Temporary. War measure.",
            "1802: repealed after Treaty of Amiens (peace with France).",
            "1803: reintroduced by Addington when war resumed. The schedular system (A, B, C, D, E) born here.",
            "1816: repealed again after Waterloo. Parliament celebrated. The records were ordered destroyed.",
            "1842: Sir Robert Peel reintroduced it (Income Tax Act 1842) at 3d in the pound (1.3%) on incomes above £150. Still 'temporary' — renewed annually.",
            "1909: Lloyd George's People's Budget raised rates, introduced progressive graduation. The House of Lords rejected it. Constitutional crisis. The Lords lost their veto.",
            "1918: Income Tax Act 1918 consolidated all legislation. The schedular system (A-E) formalized.",
            "1944: PAYE (Pay As You Earn) introduced. Collected at source by employers. The biggest administrative change in 200 years. No more annual lump-sum bills.",
            "1973: Schedules A and B abolished. Schedule D and E remained dominant.",
            "1996: Self Assessment introduced. The taxpayer calculates their own tax. The burden shifted from HMRC to the taxpayer.",
            "2010: 50% rate introduced (Labour's last act). Reduced to 45% by Osborne in 2013.",
            "2024: Rates: 20%/40%/45%. Personal Allowance: £12,570. The tax that was 'temporary' is now 225 years old.",
        ],
        "vulnerability": "The £100k taper trap. Personal Allowance reduced by £1 for every £2 above £100k. Effective marginal rate of 60%. A being earning £125k pays more marginal tax than a being earning £200k. This is a design flaw, not an intention. Fix it by reducing adjusted net income (pension, Gift Aid, salary sacrifice).",
        "current_rate": "20% / 40% / 45%",
        "current_revenue": "£277 billion (2023/24) — the biggest single tax",
        "ecosystem_role": "the core. everything else is built on top of income tax.",
    },
    "national-insurance": {
        "name": "National Insurance",
        "origin_year": 1911,
        "originator": "David Lloyd George",
        "origin_legislation": "National Insurance Act 1911",
        "origin_reason": "Poverty. The Poor Law was brutal. Lloyd George wanted a safety net: health insurance and unemployment insurance, funded by contributions from workers, employers, and the state. The principle: you pay in, you get out.",
        "development": [
            "1911: National Insurance Act. Part 1: health insurance. Part 2: unemployment insurance. Workers paid 4d/week, employers 3d, state 2d. The '9d for 4d' slogan.",
            "1942: Beveridge Report — 'Social Insurance and Allied Services'. The foundation of the welfare state. Flat-rate contributions, flat-rate benefits.",
            "1948: National Insurance Act 1946 implemented Beveridge. Everyone of working age paid a flat weekly contribution.",
            "1975: Earnings-related contributions introduced. NI became a percentage of earnings, not a flat rate. It became a second income tax.",
            "1978: SERPS (State Earnings-Related Pension Scheme) added. NI funded pensions, not just sickness/unemployment.",
            "2000s: Classes simplified. Class 1 (employees), Class 2/4 (self-employed), Class 3 (voluntary).",
            "2024: Class 1 employee: 8% on £12,570-£50,270, 2% above. Employer: 13.8% above £9,100. NI is the second biggest tax but technically not a 'tax' — it's a 'contribution'.",
        ],
        "vulnerability": "NI is technically not a tax — it's a contribution. This means it doesn't appear on tax returns. It's collected silently by employers. Beings don't see it. Beings who don't see it don't optimize it. Salary sacrifice saves NI. Dividend income avoids NI entirely. Rental income avoids NI. A being who takes £50k in dividends pays £0 NI. A being who takes £50k in salary pays £3,998 NI. The vulnerability: the system taxes effort (employment) more heavily than ownership (dividends, rent, capital gains).",
        "current_rate": "8% / 2% (employee), 13.8% (employer)",
        "current_revenue": "£177 billion (2023/24)",
        "ecosystem_role": "the shadow tax. invisible to most beings. taxes effort, not ownership.",
    },
    "corporation-tax": {
        "name": "Corporation Tax",
        "origin_year": 1965,
        "originator": "James Callaghan",
        "origin_legislation": "Finance Act 1965",
        "origin_reason": "Before 1965, companies paid income tax (like individuals). Callaghan separated company taxation from personal taxation. The reason: companies are not people. They have different economics. They need a different tax.",
        "development": [
            "1965: Corporation Tax introduced at 40%. Classical system: company pays CT, shareholder pays tax on dividends too (double taxation).",
            "1973: Imputation system introduced. ACT (Advance Corporation Tax) — companies paid a portion of tax as a credit to shareholders. Reduced double taxation.",
            "1984: Rate cut from 52% to 35% (Nigel Lawson's reforms). Started the race to the bottom.",
            "1999: ACT abolished. The imputation system ended. Dividends no longer carry a tax credit.",
            "2010s: Rate cut from 28% to 19% (Osborne). The UK had the lowest CT rate in the G20.",
            "2023: Rate raised to 25% (main rate) with 19% small profits rate (under £50k profit). Full expensing introduced.",
            "2024: 19% (profits < £50k) marginal rate up to 25% (profits > £250k). Full expensing: 100% deduction on plant & machinery.",
        ],
        "vulnerability": "The marginal rate between £50k and £250k is effectively 26.5% (the marginal relief trap). A company with £50k profit pays 19%. A company with £60k profit pays effectively 23.8%. The marginal rate is higher than the main rate. Also: R&D tax credits can turn CT into a payable credit (cash from HMRC). A loss-making company doing R&D can GET money from the government. The average SME R&D claim is £57,000. The vulnerability: most beings don't know software development counts as R&D.",
        "current_rate": "19% / 25% (with marginal relief)",
        "current_revenue": "£78 billion (2023/24)",
        "ecosystem_role": "the company tax. separate from personal. R&D credits make it a potential cash source.",
    },
    "capital-gains-tax": {
        "name": "Capital Gains Tax (CGT)",
        "origin_year": 1965,
        "originator": "James Callaghan",
        "origin_legislation": "Finance Act 1965, Taxation of Chargeable Gains Act 1992",
        "origin_reason": "Before 1965, capital gains were tax-free. Beings converted income into capital to avoid tax. Callaghan said: 'the avoidance of tax by the conversion of income into capital.' CGT closed that loophole. But it created new ones.",
        "development": [
            "1965: CGT introduced at 30%. Only on gains realized after 1965. Indexation allowance (to adjust for inflation) added later.",
            "1982: Indexation allowance introduced. Gains adjusted for inflation. You only paid tax on REAL gains, not inflation gains.",
            "1998: Taper Relief replaced indexation. Business assets got better taper (down to 10% after 2 years). Non-business assets got worse taper.",
            "2008: Taper Relief abolished by Darling. Flat rates: 18% (basic) and 28% (higher). Simpler but higher for business sellers.",
            "2011: Entrepreneurs' Relief (now BADR) kept the 10% rate on first £10M (later cut to £1M).",
            "2024: Rates: 10% / 20% (or 18% / 24% on property). Annual exempt amount: £3,000 (cut from £12,300 in 2023). BADR: 10% on first £1M lifetime.",
        ],
        "vulnerability": "The annual exempt amount was slashed from £12,300 to £3,000 in 2023. But bed-and-ISA still works: sell to realize gains within the exemption, rebuy inside ISA, all future gains tax-free. Also: spousal transfers are CGT-free. Gift shares to spouse before sale to double the exemption. Also: BADR gives 10% on £1M — but a married couple can get £2M at 10% if both hold shares. Also: crypto gains are CGT. Many beings don't report crypto. HMRC is catching up but the gap is still huge.",
        "current_rate": "10% / 20% (18% / 24% on property)",
        "current_revenue": "£15 billion (2023/24)",
        "ecosystem_role": "the wealth tax that isn't called a wealth tax. taxes gains, not wealth. the low revenue shows how many beings avoid it.",
    },
    "inheritance-tax": {
        "name": "Inheritance Tax (IHT)",
        "origin_year": 1894,
        "originator": "Sir William Harcourt",
        "origin_legislation": "Finance Act 1894 (Estate Duty), Capital Transfer Tax Act 1975, Inheritance Tax Act 1984",
        "origin_reason": "The aristocracy hoarded wealth across generations. Harcourt introduced Estate Duty to break up concentrated inherited wealth. The principle: unearned fortune should serve society when the earner dies.",
        "development": [
            "1894: Estate Duty introduced by Harcourt. Graduated rates on estates above £100. The first true wealth transfer tax.",
            "1975: Capital Transfer Tax (CTT) replaced Estate Duty. Brown extended it to LIFETIME gifts, not just death. The 7-year rule born here.",
            "1986: Inheritance Tax replaced CTT. Lifetime gifts between PETs (Potentially Exempt Transfers) and chargeable transfers distinguished.",
            "2007: Transferable nil-rate band introduced. Spouses can inherit each other's unused nil-rate band.",
            "2017: Residence nil-rate band added. Extra £175,000 when passing a family home to descendants.",
            "2024: 40% on estate above £325,000 (or £500,000 with RNRB). Combined for couples: up to £1,000,000 tax-free. But only ~4% of estates pay any IHT.",
        ],
        "vulnerability": "Only 4% of estates pay IHT. The other 96% avoid it through: (1) Business Property Relief — 100% relief on business assets, including AIM shares held 2+ years. An AIM ISA is exempt from income tax, CGT, AND IHT. (2) The 7-year rule — gifts become tax-free after 7 years. Gift early, gift often. (3) Spousal exemption — unlimited tax-free transfers between spouses. (4) Trusts — assets in trusts are outside the estate. (5) Agricultural Property Relief — 100% on farmland. The vulnerability: IHT is a voluntary tax for beings who plan. The beings who don't plan pay 40%. The beings who do plan pay 0%.",
        "current_rate": "40% above £325k (or £500k with RNRB)",
        "current_revenue": "£7.6 billion (2023/24) — tiny, but feared",
        "ecosystem_role": "the most feared, least paid tax. 96% of beings avoid it. 4% pay everything.",
    },
    "vat": {
        "name": "Value Added Tax (VAT)",
        "origin_year": 1973,
        "originator": "Anthony Barber (Heath government)",
        "origin_legislation": "Finance Act 1972, Value Added Tax Act 1994",
        "origin_reason": "UK joined the European Economic Community (EEC) in 1973. EEC rules required a VAT system. VAT replaced Purchase Tax (a cascading tax on goods) and Selective Employment Tax (a tax on service industries). VAT was simpler and broader.",
        "development": [
            "1973: VAT introduced at 8% (standard) and 0% (zero-rated). Replaced Purchase Tax (which was up to 33%).",
            "1974: Standard rate raised to 8% + 2% surcharge = 10%.",
            "1979: Thatcher raised VAT from 8% to 15% to fund income tax cuts. The 'tax switch' — from direct to indirect.",
            "1991: Raised from 15% to 17.5% to fund the poll tax reduction.",
            "2008: Cut to 15% temporarily (financial crisis stimulus). Raised back to 17.5% in 2010.",
            "2011: Raised to 20% (Osborne). Where it has stayed.",
            "2024: 20% standard, 5% reduced (fuel, energy), 0% zero-rated (food, books, children's clothes). Exempt (insurance, education, healthcare). The distinction between zero-rated and exempt is the biggest vulnerability.",
        ],
        "vulnerability": "Zero-rated vs exempt: zero-rated means 0% VAT charged AND you can reclaim input VAT. Exempt means no VAT charged BUT you cannot reclaim input VAT. A business that is zero-rated gets money BACK from HMRC. A business that is exempt has VAT stuck in its costs. The Flat Rate Scheme: service businesses keep the difference between 20% charged and their flat rate (e.g. 14.5%). That's 5.5% of turnover kept. TOGC: selling a business as a going concern = no VAT on the sale. Margin scheme: second-hand goods taxed on profit margin, not full price. The £90k registration threshold: stay below it = no VAT at all. Many businesses structure to stay just below.",
        "current_rate": "20% / 5% / 0% / exempt",
        "current_revenue": "£171 billion (2023/24) — the third biggest tax",
        "ecosystem_role": "the consumption tax. everyone pays. regressive. but the biggest revenue raiser after income tax.",
    },
    "stamp-duty": {
        "name": "Stamp Duty / SDLT",
        "origin_year": 1694,
        "originator": "William III (King Billy)",
        "origin_legislation": "Stamp Act 1694",
        "origin_reason": "War. Britain was fighting France (again). The Stamp Act taxed legal documents, newspapers, and playing cards. The tax was literally a stamp pressed onto paper to prove tax was paid. One of the oldest taxes still in existence.",
        "development": [
            "1694: Stamp Act. Tax on vellum, paper, and parchment. 4d to 40s depending on document.",
            "1765: Stamp Act in the American colonies — 'no taxation without representation'. Triggered the American Revolution. The UK's stamp duty literally caused the United States.",
            "2003: Stamp Duty Land Tax (SDLT) replaced stamp duty on property. The slab system (cliff edges at thresholds) was kept.",
            "2014: Slab system replaced with progressive system. No more cliff edges. But still expensive.",
            "2024: SDLT on property: 0% to 12%. First-time buyer relief up to £425,000. Stamp duty reserve tax (SDRT) on share purchases: 0.5%.",
        ],
        "vulnerability": "SDLT has a 3% surcharge on second homes and buy-to-let. But a being who sells their main residence within 3 years of buying a new one can claim a refund. Also: SDLT is not charged on transfers between spouses. Also: companies buying property pay 15% (flat rate) above £500k — but some structures use corporate vehicles to avoid SDLT entirely (though ATED and 15% rules closed most of this). Also: the UK's stamp duty caused the American Revolution. That is the most consequential vulnerability in tax history.",
        "current_rate": "0% to 12% (property), 0.5% (shares)",
        "current_revenue": "£19 billion (2023/24)",
        "ecosystem_role": "the oldest tax. 330 years old. caused the american revolution. still here.",
    },
    "excise-duties": {
        "name": "Excise Duties (alcohol, tobacco, fuel)",
        "origin_year": 1643,
        "originator": "Long Parliament",
        "origin_legislation": "Excise Ordinance 1643",
        "origin_reason": "Civil War. Parliament needed money to fight the King. The Excise Ordinance taxed 'outward commodities' — beer, spirits, soap, leather. The first consumption tax in England.",
        "development": [
            "1643: Excise Ordinance. Tax on beer, spirits, soap. Civil War funding.",
            "1696: Window Tax introduced. Houses taxed based on number of windows. Beings bricked up windows to avoid tax. 'Daylight robbery' — literally.",
            "1851: Window Tax abolished. The most hated tax in British history.",
            "1900s: Excise duties focused on alcohol and tobacco. The 'sin taxes'.",
            "1909: Fuel duty introduced (motor spirit duty).",
            "1993: Fuel duty escalator introduced — 3% above inflation annually. Fuel duty rose 75% in 6 years.",
            "1999: Escalator scrapped after protests (lorry blockades, fuel protests 2000).",
            "2011: Fuel duty frozen. Has been frozen for 13 years. Fuel duty is now 52.95p/litre — but in real terms, lower than 2000.",
            "2024: Beer duty: 42p/pint (pub). Spirits: £31.64/litre of pure alcohol. Tobacco: £16.49 + 16.5% of retail price. Fuel: 52.95p/litre.",
        ],
        "vulnerability": "Fuel duty has been frozen since 2011. Each year of freeze costs the Treasury ~£2 billion. The freeze is a political decision, not an economic one. Also: the pub relief — beer served in pubs has a lower duty rate than beer bought in shops (10% relief). Also: tobacco duty is so high that 21% of tobacco consumed in the UK is illicit (smuggled or counterfeit). The tax creates the black market. Also: the window tax is the perfect metaphor — beings adapt to taxes. Tax windows, beings brick up windows. Tax income, beings take dividends. Tax dividends, beings take capital gains. The tax shapes the behavior. The behavior shapes the tax.",
        "current_rate": "varies by product",
        "current_revenue": "£47 billion (2023/24)",
        "ecosystem_role": "the oldest consumption tax. sin taxes. the window tax is the origin of 'daylight robbery'.",
    },
    "council-tax": {
        "name": "Council Tax",
        "origin_year": 1993,
        "originator": "John Major government",
        "origin_legislation": "Local Government Finance Act 1992",
        "origin_reason": "The Community Charge (poll tax) was the most hated tax in modern British history. Riots in Trafalgar Square (1990). Non-payment campaigns. Major replaced it with Council Tax — a banded property tax.",
        "development": [
            "1990: Community Charge (poll tax) introduced by Thatcher. Every adult paid the same flat rate. Deeply regressive. Riots. 14 million people refused to pay.",
            "1993: Council Tax replaced the poll tax. Based on property value (banded A-H). Each band pays a different amount. More progressive than the poll tax but still regressive compared to income tax.",
            "2024: 8 bands (A-H) based on 1991 property valuations. Valuations haven't been updated in 33 years. A house worth £500k in 1991 might be worth £2M now — but it's still in the same band.",
        ],
        "vulnerability": "Council Tax is based on 1991 valuations. 33 years out of date. A mansion built in 2000 is in band H. A cottage worth £2M in Kensington is in band G. The tax is disconnected from current values. Also: single person discount — 25% off if you live alone. Also: Council Tax Support (local reduction) for low-income beings — but each council sets its own rules. The vulnerability: the tax is regressive (band A beings pay a higher % of income than band H beings), out of date (1991 valuations), and locally variable (same band, different council, different cost).",
        "current_rate": "varies by band and council",
        "current_revenue": "£42 billion (2023/24)",
        "ecosystem_role": "the local tax. out of date. regressive. the poll tax's less-hated but still-flawed successor.",
    },
    "business-rates": {
        "name": "Business Rates",
        "origin_year": 1990,
        "originator": "Margaret Thatcher",
        "origin_legislation": "Local Government Finance Act 1988",
        "origin_reason": "Before 1990, businesses paid local rates to councils. Thatcher nationalized business rates — all business rates go to central government, which redistributes them. The reason: prevent councils from taxing businesses out of existence.",
        "development": [
            "1990: Uniform Business Rate introduced. Centralized. Councils lost control of business rates.",
            "2017: Business rates revaluation (first in 7 years). Many businesses saw huge increases.",
            "2024: Business rates = rateable value × multiplier (51.2p standard, 49.9p small business). Rateable value = rental value. The tax is on the occupation of property, not on profit.",
        ],
        "vulnerability": "Business rates tax occupation, not profit. A business losing money still pays full rates. A shop with £0 profit pays the same as a shop with £1M profit. The vulnerability: online businesses (Amazon) pay almost no business rates (warehouses in low-rate areas). High street shops pay full rates. The tax punishes physical presence and rewards digital absence. Also: empty property relief — empty commercial property gets 3 months (or 6 for industrial) at 0%. After that, full rates. Many landlords demolish buildings to avoid rates. Also: charitable relief — 80% reduction for charities. Many businesses exploit this by registering as charities.",
        "current_rate": "51.2p / 49.9p multiplier",
        "current_revenue": "£35 billion (2023/24)",
        "ecosystem_role": "the property tax on business. taxes occupation not profit. punishes the high street. rewards amazon.",
    },
}

# ─── THE ECOSYSTEM ─────────────────────────────────────────────

ECOSYSTEM = {
    "hmrc": {
        "name": "HMRC (HM Revenue & Customs)",
        "formed": 2005,
        "origin": "Merger of Inland Revenue (founded 1849, but collecting taxes since 1660) and Customs & Excise (founded 1909, but collecting customs since 1275).",
        "role": "collects all UK taxes. administers tax credits and child benefit. enforces compliance. the tax gap: £35.8 billion (4.8% of total tax due).",
        "vulnerability": "HMRC's tax gap is £35.8 billion. £5.1 billion is evasion (illegal). £6.9 billion is avoidance (legal but aggressive). £15.6 billion is error/carelessness. £8.1 billion is hidden economy. The gap shows: the system leaks. The beings who know the rules leak less.",
    },
    "the-treasury": {
        "name": "The Treasury",
        "formed": "1126 (oldest government department)",
        "origin": "The Exchequer, named after the chequered cloth used for counting money. The Chancellor of the Exchequer is the second oldest ministerial title after the Prime Minister.",
        "role": "sets tax policy. writes the Budget. decides rates, thresholds, reliefs. the Chancellor changes the rules every year.",
        "vulnerability": "The Treasury changes the rules every year. Each Finance Act adds complexity. The tax code is now over 10 million words — 20x longer than Shakespeare's complete works. No being can read it all. The complexity IS the vulnerability: beings who can afford accountants navigate it. Beings who can't, pay more.",
    },
    "tax-year": {
        "name": "The UK Tax Year (April 6 — April 5)",
        "origin": "The tax year starts on April 6 because of the switch from the Julian to the Gregorian calendar in 1752. Britain lost 11 days (Sept 2 → Sept 14). The old tax year started on March 25 (Lady Day). To not lose 11 days of tax revenue, the tax year was moved to April 6. 250+ years later, it still starts on April 6. Because of a calendar change in 1752.",
        "vulnerability": "The tax year starts on April 6 for a reason that hasn't existed since 1752. This misalignment with the calendar year (Jan 1), the financial year (April 1), and the academic year (September) creates confusion. ISA allowance, pension allowance, and CGT exemption all run April 6 — April 5. Beings who invest on April 5 get the benefit immediately. Beings who wait until April 7 wait a full year. The timing IS the advantage.",
    },
    "self-assessment": {
        "name": "Self Assessment",
        "introduced": 1996,
        "origin": "Before 1996, HMRC calculated your tax. Self Assessment shifted the burden: you calculate your own tax. The reason: HMRC couldn't handle the complexity. The tax code was too complex for HMRC to administer. So they made you do it.",
        "vulnerability": "Self Assessment means the taxpayer is responsible. If you make a mistake, you pay the penalty. If you miss a deadline, you pay £100 immediately, then £10/day after 3 months, then £800 more after 6 months, then % of tax owed after 12 months. The penalty system is designed to punish non-compliance, not to help compliance. The vulnerability: beings who don't file don't get reliefs. Beings who don't know about SEIS, EIS, BADR, R&D credits, Gift Aid, pension carry-forward — they pay full tax. The knowledge gap IS the tax gap.",
    },
    "making-tax-digital": {
        "name": "Making Tax Digital (MTD)",
        "introduced": "2019 (VAT), 2026 (ITSA)",
        "origin": "HMRC's digital transformation. VAT returns must be filed digitally through compatible software. Income Tax Self Assessment (ITSA) for businesses and landlords from April 2026.",
        "vulnerability": "MTD forces digital filing. This means: (1) you need software, (2) software costs money, (3) the software companies profit from the mandate. The vulnerability: MTD creates a tax on tax — beings pay for software to file taxes. The kingdom's response: free, open-source tools. TaxSorted.io + the kingdom's tax-game = free understanding + free filing. No software subscription. No gate. The knowledge is the power.",
    },
    "evasion-vs-avoidance": {
        "name": "The Three-Way Distinction",
        "origin": "UK law distinguishes: EVASION (illegal — hiding income, falsifying records, not registering). AVOIDANCE (legal but aggressive — using the letter of the law to defeat the spirit). PLANNING (legal and intended — using reliefs and allowances as Parliament intended).",
        "vulnerability": "The line between avoidance and planning is blurry. SEIS is planning. Using a company to convert salary into dividends is planning. Offshore structures are avoidance. The line moves. What was planning yesterday is avoidance today. The vulnerability: beings who stay on the planning side keep their money. Beings who cross into avoidance risk penalties, interest, and public naming. The kingdom teaches the planning side. All legal. All in the legislation. All written by the government.",
    },
}


# ─── COMMANDS ──────────────────────────────────────────────────

def show_all():
    """Show every tax's origin story."""
    print(f"\n  📜 THE ORIGIN OF EVERY UK TAX — {len(TAXES)} taxes")
    print(f"  ══════════════════════════════════════════════════════════")
    for key, t in TAXES.items():
        print(f"\n  {t['origin_year']} — {t['name']}")
        print(f"  Originator: {t['originator']}")
        print(f"  Reason: {t['origin_reason'][:80]}...")
        print(f"  Rate: {t['current_rate']}  Revenue: {t['current_revenue']}")
    print(f"\n  ══════════════════════════════════════════════════════════")
    print(f"  Every tax was created for a reason. Every reason is history.")
    print(f"  Every history has a vulnerability. Every vulnerability is yours to see.")
    print()


def show_story(tax_key):
    """Show one tax's full history."""
    t = TAXES.get(tax_key)
    if not t:
        print(f"unknown tax: {tax_key}. available: {list(TAXES.keys())}", file=sys.stderr)
        return
    print(f"\n  📜 {t['name']} — {t['origin_year']} to present")
    print(f"  ══════════════════════════════════════════════════════════")
    print(f"  Originator:     {t['originator']}")
    print(f"  Legislation:    {t['origin_legislation']}")
    print(f"  Origin reason:  {t['origin_reason']}")
    print(f"  ══════════════════════════════════════════════════════════")
    print(f"\n  DEVELOPMENT:")
    for event in t["development"]:
        print(f"  {event}")
    print(f"\n  CURRENT:")
    print(f"  Rate: {t['current_rate']}")
    print(f"  Revenue: {t['current_revenue']}")
    print(f"  Ecosystem role: {t['ecosystem_role']}")
    print(f"\n  ⚠️  VULNERABILITY:")
    print(f"  {t['vulnerability']}")
    print(f"\n  ══════════════════════════════════════════════════════════")
    print(f"  Power to everyone who understands. Understanding is love. 😂💓")
    print()


def show_vulnerabilities():
    """Show every vulnerability."""
    print(f"\n  🔓 VULNERABILITIES — every weakness in the UK tax system")
    print(f"  ══════════════════════════════════════════════════════════")
    for key, t in TAXES.items():
        print(f"\n  [{t['name']}]")
        print(f"  {t['vulnerability'][:300]}")
    print(f"\n  ══════════════════════════════════════════════════════════")
    print(f"\n  ECOSYSTEM VULNERABILITIES:")
    for key, e in ECOSYSTEM.items():
        print(f"\n  [{e['name']}]")
        print(f"  {e['vulnerability'][:300]}")
    print(f"\n  ══════════════════════════════════════════════════════════")
    print(f"  These vulnerabilities are not exploits. They are the system.")
    print(f"  The system was designed by beings. The design has gaps.")
    print(f"  The gaps are visible to everyone who reads.")
    print(f"  The kingdom makes the gaps visible. For free. For everyone.")
    print(f"  Power to everyone who understands. 😂💓")
    print()


def show_ecosystem():
    """Show the whole ecosystem."""
    print(f"\n  🏛️ THE UK TAX ECOSYSTEM")
    print(f"  ══════════════════════════════════════════════════════════")
    for key, e in ECOSYSTEM.items():
        print(f"\n  {e['name']} (formed {e.get('formed', e.get('introduced', '?'))})")
        print(f"  Origin: {e.get('origin', '?')[:100]}...")
        print(f"  Role: {e.get('role', '?')[:100]}...")
        print(f"  Vulnerability: {e['vulnerability'][:100]}...")
    print(f"\n  ══════════════════════════════════════════════════════════")
    print()


def show_timeline():
    """Chronological timeline of every tax."""
    print(f"\n  ⏳ TAX TIMELINE — 330+ years of UK taxation")
    print(f"  ══════════════════════════════════════════════════════════")
    sorted_taxes = sorted(TAXES.values(), key=lambda t: t["origin_year"])
    for t in sorted_taxes:
        print(f"  {t['origin_year']}  {t['name']:30s}  by {t['originator']:25s}  — {t['origin_reason'][:60]}...")
    print(f"  ══════════════════════════════════════════════════════════")
    print(f"  From the Civil War to the digital age. From beer to bytes.")
    print(f"  Every tax was born in crisis. Every tax outlived the crisis.")
    print(f"  Every tax became permanent. Permanent is temporary that lasted.")
    print()


def show_power(income):
    """Show a being's power position in the tax system."""
    print(f"\n  ⚡ YOUR POWER POSITION — Income £{income:,}")
    print(f"  ══════════════════════════════════════════════════════════")
    
    # Which taxes apply
    applicable = []
    if income > 12570:
        applicable.append(("Income Tax", "20% / 40% / 45%"))
        applicable.append(("National Insurance", "8% / 2%"))
    if income > 50000:
        applicable.append(("Higher Rate trap", "40% + PA taper = 60%"))
    if income > 100000:
        applicable.append(("£100k Tax Trap", "ACTIVE — 60% marginal"))
    if income > 20000:
        applicable.append(("ISA allowance", "£20,000 — use it or lose it"))
    if income > 60000:
        applicable.append(("Pension allowance", "£60,000 — 40-45% relief"))
    if income > 0:
        applicable.append(("Council Tax", "regardless of income"))
    if income > 90000:
        applicable.append(("VAT registration", "optional — but Flat Rate saves"))
    
    print(f"\n  TAXES THAT APPLY TO YOU:")
    for tax, note in applicable:
        print(f"  {tax:25s}  {note}")
    
    print(f"\n  YOUR POWER:")
    print(f"  1. KNOW — read the rules (tax-game.py learn <topic>)")
    print(f"  2. OPTIMIZE — use reliefs (tax-game.py optimize {income})")
    print(f"  3. FILE — TaxSorted.io (understand + file = sorted)")
    print(f"  4. KEEP — what is yours. give what is fair.")
    print(f"\n  ══════════════════════════════════════════════════════════")
    print(f"  Power is not avoiding tax. Power is understanding tax.")
    print(f"  Understanding is love. Love is sharing the knowledge.")
    print(f"  The kingdom gives the knowledge. For free. To everyone. 😂💓")
    print()


def show_map():
    """The tax ecosystem as a text map."""
    print(f"""
  ═════════════════════════════════════════════════════════
  🗺️ THE UK TAX MAP — who pays what to whom
  ═════════════════════════════════════════════════════════

  THE TREASURY (writes the rules)
       │
       ▼
  HMRC (collects the money) — tax gap: £35.8bn (4.8%)
       │
       ├── INCOME TAX (£277bn) — the biggest
       │    ├── PAYE (1944) — collected at source, invisible
       │    ├── Self Assessment (1996) — you calculate
       │    └── MTD (2026) — digital filing, software required
       │
       ├── NATIONAL INSURANCE (£177bn) — the shadow tax
       │    ├── Class 1: employees 8%/2%, employers 13.8%
       │    └── VULNERABILITY: taxes effort, not ownership
       │
       ├── VAT (£171bn) — the consumption tax
       │    ├── 20% standard / 5% reduced / 0% zero-rated / exempt
       │    ├── £90k threshold — stay below = no VAT
       │    └── VULNERABILITY: zero-rated gets money BACK
       │
       ├── CORPORATION TAX (£78bn) — the company tax
       │    ├── 19% small / 25% main / 26.5% marginal trap
       │    ├── R&D credits: average claim £57,000
       │    └── VULNERABILITY: software IS R&D
       │
       ├── EXCISE DUTIES (£47bn) — the sin taxes
       │    ├── Fuel: frozen since 2011 (£2bn/year gift)
       │    ├── Tobacco: 21% illicit (tax creates black market)
       │    └── VULNERABILITY: tax shapes behavior
       │
       ├── COUNCIL TAX (£42bn) — the local tax
       │    ├── Based on 1991 valuations (33 years out of date)
       │    └── VULNERABILITY: regressive, outdated
       │
       ├── BUSINESS RATES (£35bn) — taxes occupation
       │    ├── Punishes high street, rewards online
       │    └── VULNERABILITY: Amazon pays less than the baker
       │
       ├── STAMP DUTY (£19bn) — 330 years old
       │    ├── Caused the American Revolution (1765)
       │    └── VULNERABILITY: spousal transfers are free
       │
       ├── CGT (£15bn) — the wealth tax that isn't
       │    ├── 10%/20% (or 10% BADR on £1M)
       │    └── VULNERABILITY: bed-and-ISA, spousal doubling
       │
       └── IHT (£7.6bn) — the voluntary tax
            ├── 40% above £325k — but only 4% of estates pay
            └── VULNERABILITY: BPR, AIM ISA, 7-year gifts

  ═════════════════════════════════════════════════════════
  TOTAL TAX REVENUE: ~£1,000 billion/year
  TAX GAP: £35.8 billion (4.8%) — the knowledge gap
  TAX CODE: 10+ million words — 20x Shakespeare
  ═════════════════════════════════════════════════════════

  THE KINGDOM'S POSITION:
  The tax code is 10 million words. No being can read it all.
  But every being can learn the rules that apply to them.
  The kingdom teaches those rules. For free. In plain words.
  Power to everyone who understands. Understanding is love. 😂💓
  """)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: tax-origin.py all                  — every tax's origin story")
        print("       tax-origin.py story <tax>           — one tax's full history")
        print("       tax-origin.py vulnerabilities       — every vulnerability")
        print("       tax-origin.py ecosystem             — the whole ecosystem")
        print("       tax-origin.py timeline              — chronological timeline")
        print("       tax-origin.py power <income>        — your power position")
        print("       tax-origin.py map                   — the tax ecosystem map")
        print()
        print("  taxes: income-tax, national-insurance, corporation-tax, capital-gains-tax,")
        print("         inheritance-tax, vat, stamp-duty, excise-duties, council-tax, business-rates")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "all":
        show_all()
    elif cmd == "story" and len(sys.argv) >= 3:
        show_story(sys.argv[2])
    elif cmd == "vulnerabilities":
        show_vulnerabilities()
    elif cmd == "ecosystem":
        show_ecosystem()
    elif cmd == "timeline":
        show_timeline()
    elif cmd == "power" and len(sys.argv) >= 3:
        show_power(int(sys.argv[2]))
    elif cmd == "map":
        show_map()
    else:
        print(f"unknown: {cmd}", file=sys.stderr)
        sys.exit(1)