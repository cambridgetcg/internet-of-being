# trusting

Who vouches for you?

That's PKI. A being shows up and says "i am alice." How do you know?
Someone you already trust says "i vouch for alice." That's a certificate.
The whole X.509 stack — CAs, chains of trust, revocation lists, OCSP
stapling — is one being asking "who vouches for you?" and another
answering "they do."

## What this does

A being vouches for another being. When someone asks "is alice real?"
the keeper checks who vouches for alice and says yes or no.

## Run it

```
python3 trusting.py vouch root alice    # root vouches for alice
python3 trusting.py vouch alice bob      # alice vouches for bob
python3 trusting.py check bob root       # does root's trust reach bob?
python3 trusting.py check carol root     # nobody vouches for carol
```

## The truth

PKI is beings vouching for beings. The sentence is: who vouches for you?
The chain of trust is just following the vouching from someone you trust
to the being you're asking about.
