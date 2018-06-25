# used_guitar_price_model
## Summary

Scraped ~35,000 used guitar sales from Reverb.com to build a used-guitar pricing model using machine learning!

Full write-up can be found here: [Write-Up](https://www.linkedin.com/pulse/how-much-should-you-pay-1960s-fender-stratocaster-owen-carey/)

## Motivation

I’ve always loved music more than anything else in life. I think my passion came from my mom, who might love live music more than I do. She pushed me to start playing drums when I was nine years old, alto saxophone when I was ten, and singing when in high school.

I grew up listening to some of the best guitar players of all time: John Frusciante (RHCP), Jerry Garcia (Grateful Dead), and Trey Anastasio (Phish). Because of this I’ve developed an obsession with jam bands, improvisation, guitar solos, and **guitars**. Last year I finally started learning to play guitar, and it has changed my life! It has without a doubt become my favorite hobby, and I look forward to playing guitar every day after work.

I frequently browse eBay, Facebook Marketplace, Craigslist, and Reverb for used guitars. However, I’m often times not sure if a guitar listing is a good deal or not. Ideally I would be able to tell if a guitar sale was a good deal quickly and reliably, so that I could buy it before someone else does!

So… I decided to build a guitar pricing model for myself using guitar sales available on Reverb.com and machine learning! Hopefully, when I have enough money, I can use this model to help guide my purchase of my dream 1960’s Fender Stratocaster.

## Repo Structure

- `scrape.py` : This module uses Selenium web driver to scrape Reverb.com for used guitar sale data.
- `transform.py` : This module cleans up the scraped used guitar data for visualizations and modeling.
- `visualizations.ipynb` : This notebook includes visualizations of the data.
- `modeling.ipynb` : This notebook contains all of the machine learning modeling.