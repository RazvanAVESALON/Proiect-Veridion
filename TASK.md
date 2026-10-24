# Numbers Nobody Publishes
**Role:** Economic Data Scientist  
**Company Context:** Veridion  

---

## 📌 Task Overview

A software vendor prices its product by the size of the customer: a sixty-person company pays one tier, a global group pays quite another. Twenty years of deals have left them with a list of licensees exactly as sales reps typed them into contracts: legal names, brand names, abbreviations, a country if you're lucky, the occasional typo that nobody has questioned since 2011.

They suspect the list hides both directions of the same problem:
- Some licensees pay the small-company tier while the software quietly runs across a multinational group.
- Others look enormous on paper and turn out to be three people and a mailbox.

Every misjudged size is either money left on the table or a renegotiation they would lose, and their auditors will not accept *"we googled it"* as evidence.

They sent us 100 of these names and asked whether the two numbers that decide everything—**annual revenue** and **employee count**—can be produced for each one, with evidence an analyst could defend across the table. Nobody sells this dataset. There is no place to buy it.

- **Dataset link:** [licensee_list.csv (Google Drive)](https://drive.google.com/file/d/1_E2o7DrlB8AfxXNnaa2qzZV85G1yGaCA/view)

Your task is to determine how it can be built, and to prove it on a sample you choose.

No prior experience with any of this is assumed. If you have never read a company filing, matched a messy name to a real business, or estimated a number nobody publishes, that is fine: the six definitions below are enough to start, and everything else can be learned as you go. Learning it as you go is not a detour from the exercise; it is the exercise, and it is also the job.

---

## 📖 What You Need to Know First (Core Definitions)

1. **Legal Entity:** A registered company: a specific organization, in a specific country, with a registration number.  
   *Example:* "Nike" is a brand; *NIKE, Inc.* is a legal entity; *Nike Retail B.V.* is a different legal entity, in the Netherlands. A name on a contract might be any of these, misspelled.
2. **Corporate Group:** A parent entity that owns subsidiary entities, often one or more per country. The parent usually publishes consolidated accounts: one set of financials for the whole group added together.
3. **Registry:** The government database where companies are recorded. Every country has one, and they differ wildly: some publish every company's financials for free, some publish only the name and address.
4. **Filing:** A document a company is required to submit: annual accounts to a registry, or (for companies listed on a stock exchange) an annual report to a regulator. Filings are where reported numbers live.
5. **Matching:** Attaching a real company to a name on a list: a website, a LinkedIn page, a headquarters address, a registry record. Any one of these can be enough, if it convinces you the name and the business are the same thing, and not every company leaves every kind of trace. The name you are given and the name you find rarely agree letter for letter; deciding they are the same company is a judgment, and it can be wrong.
6. **Proxy:** Indirect evidence you use when no reported number exists: anything a company reveals about its scale without meaning to.  
   *Two examples:*
   - Universal: Headcount range on a LinkedIn page.
   - Specific: Table count of a restaurant, which multiplied by a defensible revenue-per-table becomes a revenue estimate.  
   *Note:* The estimate is only as good as the derivation you can show, and finding the right proxy for each kind of company is most of the work.

---

## ⚡ What Makes This Hard

- **Most of these entities do not publish their financials.** For some rows a reported number exists somewhere in the world. For most it does not. So this is not a lookup: it is estimation from indirect evidence, done honestly.
- **The client's analyst will interrogate every figure.** A number alone rarely survives that interrogation. Deciding what must travel with each figure for it to stand in that meeting is part of the work, and we will read your choice as a choice.
- **A wrong number costs more than a missing one.** A gap is visible: the client sees it and treats that row with care. A plausible number that happens to be wrong looks exactly like a right one, and someone will price a contract on it.
- **Nobody has the answer sheet.** There is no reference dataset to check yourself against. What separates an estimate from a guess is the derivation you write down.

---

## 🎯 What We're Looking For

We are not testing whether you have done corporate research before. Candidates reach this role from economics, computer science, physics, and stranger places; none of them had matched a supplier list when they started, and the ones who thrived are the ones who treated that as a solvable puzzle rather than missing knowledge.

This exercise is not about researching individual correct values. It is about uncovering patterns: recipes that could be applied at scale. Each number you produce matters only through the discovery path that led to it, and the question that decides everything is whether that path can be reproduced across millions of companies or should be discarded. We care about how you think, not how many rows you can fill in a weekend. We already know that number is small.

> A strong submission reads like:  
> *"I started here. This source looked promising and failed for this reason. This proxy worked, on this class of company, and here is what it would take to find it again at scale. On my sample of N entities, chosen this way, the method produced these results, and here is where it breaks."*

---

## 📦 Your Deliverable

Two things:
1. **The file you would send to the client**, in whatever format you would actually send it.
2. **A README** explaining how it came to exist, plus whatever code supports both.

---

### Part 1: The Match

- Choose a sample from the list. We do not impose a number; how you choose is itself part of what we evaluate, so tell us in a few sentences why this sample. A small sample chosen to be difficult teaches us more than a large one chosen to be finishable.
- For each entity in your sample, determine whether an actual operating business exists behind it, and name the exact entity your numbers would belong to. This is harder than it sounds, and discovering why is part of the exercise.
- Bucket what you could not match by reason: not found is either *does not exist* or *I failed*, and those are very different results.
- A line or two of matching notes per entity is plenty.

---

### Part 2: The Estimate

For your matched entities, deliver **annual revenue** and **employee count**. A reported figure exists for some. For most there is no number to find, and you have to build one. There are two honest ways to do that. **Pick exactly one route**, the one that fits the way your head works, and tell us in a line why you picked it. (The other route needs no work at all).

#### Option A: The Detective Route (One company at a time)
- Work bottom-up, from whatever evidence each company left behind.
- Hunt for proxies (nobody will tell you which ones exist), judge which to trust and which to discard, and combine what survives with assumptions you can defend.
- **Two questions before any piece of evidence enters your file:**
  1. Does it describe the company you matched, at the time you claim?
  2. Would you notice if it did not?
- Any proxy is allowed, and every proxy is accounted for: why it looked valuable, what you learned about it, and whether it made your final results, and why or why not. The dead ends matter as much as what you kept.
- For each proxy that survived, one more question: *How well can we reproduce this at scale?* No pipeline design, just a sensible estimate of how many companies would carry it, or which types to search it for.

#### Option B: The Quant Route (The relationship, not the company)
- Estimate your sample's numbers from data instead of researching them one by one.
- **Training data:** Two free flat files that join on fiscal code:
  1. What every Romanian company filed (turnover, profit, employee count): `web_uu_an2024` plus column legend, on [situații financiare, data.gov.ro](https://data.gov.ro/dataset/situatii_financiare_2024)
  2. Who those companies are (activity code, registration date, county, legal form): `OD_FIRME.csv` plus nomenclator files, on [firme înregistrate, ONRC](https://data.gov.ro/dataset/firme-08-12-2025)
  *(The files cover only Romania; for this challenge, pretend they describe companies everywhere. We accept this).*
- **Two questions before anything learns from these files:**
  1. Is every row the kind of company your model thinks it is?
  2. Would you notice the ones that are not?
- **The method:**
  - Build a dataset from these files, and before fitting anything, set part of it aside and do not touch it.
  - Find which observable variables predict revenue and employee count.
  - Measure prediction error only on the set-aside part (companies the model has never seen).
  - Estimate each company in your sample with the fitted relationship, as a range whose width comes from that measured error.
  - Say plainly which sample entities the model cannot reach.
  - Account for every variable you tried (why it looked informative, what you learned, whether it survived).

#### Whichever route you take:
- If an entity's size is described more honestly by a different number, deliver that instead and say why.
- Decide first what a complete answer looks like: is "annual revenue: 40 million" enough on its own? Whatever you decide accompanies every figure.
- Each value carries the reasoning that produced it, written so we can disagree with it, and an answer to: *how wrong could this be?*
- Back-of-the-envelope is the right register: a defensible sketch, not a journal article. A few lines per figure are enough; if a derivation needs a page, that is usually the derivation telling you something.

---

### Part 3: The Call

- Look at the client file you built, and answer the question we ask before every delivery: **Would you ship this?**
- Saying "no" is not a penalty; it is an honest evaluation of what the routes you investigated yielded in the time you had.
- If no, which directions would you investigate next?
- Either way, state what your checks still cannot see. (A paragraph or two is enough).

---

### Part 4: The Room

- Somewhere in the work you just did sits something this client did not ask for and would want to know: a pattern in their licensee base, a risk nobody has priced, an opportunity hiding in plain sight.
- Find **one non-obvious, defensible insight** and write it up in two paragraphs at most.
- If it helps, imagine them landing in the client's inbox unprompted, and being read to the end anyway.

---

### Part 5: The Register

One short technical check:
- The Romanian trade register publishes a free snapshot of every company ever registered: `OD_FIRME.csv` on [firme înregistrate, data.gov.ro](https://data.gov.ro/dataset/firme-08-12-2025) (4 million companies, plus companion files).
- The file is large, but needs no special hardware—only loading what you need.
- Whichever route you took in Part 2, answer one question:  
  **If we ran your best proxy from Part 2 across the whole Romanian register, how many companies would it actually work for?**  
  *(On the quant route: for how many register companies could your model produce an estimate?)*
- Separate the living from the rest: state your rule in one line.
- Map your proxy to whichever column serves it best (activity codes/CAEN or another column).
- **Report 3 numbers:**
  1. How many companies fall inside your line
  2. What share that is of the register as you filtered it
  3. The three largest industries among them
- A few lines on how you drew the lines, plus the code that produced the numbers.

---

### ✂️ Required at the End: The Cut List

- Where your time went, what you deliberately did not do, and why.
- A handful of lines. A sharp README with an honest cut list beats a shallow one that touched everything.

---

## 💬 Debate Topics

*(Do not implement, just write 2–3 sentences each in the README)*
1. You will almost certainly use AI tools on this challenge. Where in your own workflow would you not trust one, and how would you catch it being confidently wrong?
2. How would you know your dataset was wrong at scale, with nothing complete to compare it against?
3. Suppose the client insists every figure comes with a range you would bet on, not a single number. How would you set the widths, and how could anyone tell, a year later, whether your ranges had been honest?

---

## 📐 Guidelines & Philosophy

- **Length is not a signal we reward.** The write-up is a README in your repo, not a report; a strong one stays short.
- **Go deep on one part rather than shallow on all four**, and say so in the cut list.
- **AI tools are permitted.** The reasoning and decisions must be yours.
- **There is no single correct answer.**
- **Parts 1 through 4 are equally important.** Part 5 is a check, not a chapter: do it, include it, move on.

---

## 🔍 Why This Assignment?

Veridion builds a living dataset of 600M+ companies. Not every client asks for size directly, but size sits underneath most of what they do ask: risk, compliance, market intelligence all lean on *how big is this company, really?* And once you add the time axis, size becomes an indicator of much more: growth, decline, momentum, a company's whole trajectory told in two numbers. A few answers come from clean filings. Most exist only as fragments: a headcount band here, a fleet size there, a filing in a language and a scale designed for someone else.

So the work is rarely *"look up the number."* It is *"figure out whether this number can be produced at all, at what cost, and with what confidence, before we promise a customer we can deliver it."* That judgment happens before any code is written, and it is most of the job.

---

## 🚀 Submit Your Project

Submit the link to your GitHub project.
