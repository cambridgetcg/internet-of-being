# requesting

Give me what you have.

You ask. They give. That's HTTP. The verb is "give." The resource is
"what you have." The response is what they give you. Everything else —
methods, headers, content negotiation, caching directives, status code
taxonomies — is ceremony layered on top of one being asking another
for something and receiving it.

## What this does

A being asks for something. The keeper gives it or says they don't have it.

## Run it

```
python3 requesting.py serve     # a being that has things
python3 requesting.py ask /hello  # ask for a thing
```

## The truth

HTTP is a request and a response. The request is "give me X." The
response is "here's X" or "i don't have X." Everything else is headers.