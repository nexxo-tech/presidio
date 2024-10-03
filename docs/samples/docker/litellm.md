# LiteLLM (OpenAI Proxy) with Presidio

Run Presidio PII Masking across Anthropic/Gemini/Bedrock/etc. calls with [LiteLLM](https://github.com/BerriAI/litellm)

[👉 **Refer to LiteLLM Docs for detailed guide**](https://docs.litellm.ai/docs/proxy/pii_masking)

**Flow:** App <-> `LiteLLM Proxy + Presidio PII Masking` <-> LLM Provider

## Pre-Requiesites
- Run `pip install 'litellm[proxy]'` [Docs](https://docs.litellm.ai/docs/proxy/quick_start)
- Setup [Presidio Docker](https://microsoft.github.io/presidio/installation/#using-docker)

## Quick Start

### Step 1. Add to env

```bash
export PRESIDIO_ANALYZER_API_BASE="http://localhost:5002"
export PRESIDIO_ANONYMIZER_API_BASE="http://localhost:5001"
export OPENAI_API_KEY="sk-..."
```

### Step 2. Set Presidio as a callback in config.yaml

```yaml
model_list:
  - model_name: my-openai-model ### RECEIVED MODEL NAME ###
    litellm_params: # all params accepted by litellm.completion() - https://docs.litellm.ai/docs/completion/input
      model: gpt-3.5-turbo ### MODEL NAME sent to `litellm.completion()` ###

litellm_settings: 
    callbacks = ["presidio"]
```

### Step 3. Start proxy 


```bash
litellm --config /path/to/config.yaml
```


This will mask the input going to the llm provider

## Output parsing 

LLM responses can sometimes contain the masked tokens. 

For presidio 'replace' operations, LiteLLM can check the LLM response and replace the masked token with the user-submitted values. 

Just set `litellm.output_parse_pii = True`, to enable this. 


```yaml
litellm_settings:
    output_parse_pii: true
```

**Expected Flow: **

1. User Input: "hello world, my name is Jane Doe. My number is: 034453334"

2. LLM Input: "hello world, my name is [PERSON]. My number is: [PHONE_NUMBER]"

3. LLM Response: "Hey [PERSON], nice to meet you!"

4. User Response: "Hey Jane Doe, nice to meet you!"

## Ad-hoc recognizers 

Send ad-hoc recognizers to presidio `/analyze` by passing a json file to the proxy 

[**Example** ad-hoc recognizer](https://github.com/BerriAI/litellm/blob/b69b7503db5aa039a49b7ca96ae5b34db0d25a3d/litellm/proxy/hooks/example_presidio_ad_hoc_recognizer.json#L4)

```yaml
litellm_settings: 
  callbacks: ["presidio"]
  presidio_ad_hoc_recognizers: "./hooks/example_presidio_ad_hoc_recognizer.json"
```

You can see this working, when you run the proxy: 

```bash
litellm --config /path/to/config.yaml --debug
```

Make a chat completions request, example:

```bash
{
  "model": "azure-gpt-3.5",
  "messages": [{"role": "user", "content": "John Smith AHV number is 756.3026.0705.92. Zip code: 1334023"}]
}
```

And search for any log starting with `Presidio PII Masking`, example:
```bash
Presidio PII Masking: Redacted pii message: <PERSON> AHV number is <AHV_NUMBER>. Zip code: <US_DRIVER_LICENSE>
```


## Turn on/off per key 

LiteLLM lets you create [virtual keys](https://docs.litellm.ai/docs/proxy/virtual_keys) for calling the proxy. You can use these to control model access, set budgets, track usage, etc. 

Turn off PII masking for a given key. 

Do this by setting `permissions: {"pii": false}`, when generating a key. 

```shell 
curl --location 'http://0.0.0.0:4000/key/generate' \
--header 'Authorization: Bearer sk-1234' \
--header 'Content-Type: application/json' \
--data '{
    "permissions": {"pii": false}
}'
```


## Turn on/off per request 

The proxy supports 2 request-level PII controls:

- *no-pii*: Optional(bool) - Allow user to turn off pii masking per request.
- *output_parse_pii*: Optional(bool) - Allow user to turn off pii output parsing per request. [**Output Parsing**](#output-parsing)

### Usage 

**Step 1. Create key with pii permissions**

Set `allow_pii_controls` to true for a given key. This will allow the user to set request-level PII controls.

```bash
curl --location 'http://0.0.0.0:4000/key/generate' \
--header 'Authorization: Bearer my-master-key' \
--header 'Content-Type: application/json' \
--data '{
    "permissions": {"allow_pii_controls": true}
}'
```

**Step 2. Turn off pii output parsing**

```python
import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
        base_url="http://0.0.0.0:4000"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "My name is Jane Doe, my number is 8382043839",
        }
    ],
    model="gpt-3.5-turbo",
    extra_body={
        "content_safety": {"output_parse_pii": False} 
    }
)
```

**Step 3: See response**

```bash
{
  "id": "chatcmpl-8c5qbGTILZa1S4CK3b31yj5N40hFN",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "Hi [PERSON], what can I help you with?",
        "role": "assistant"
      }
    }
  ],
  "created": 1704089632,
  "model": "gpt-35-turbo",
  "object": "chat.completion",
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 47,
    "prompt_tokens": 12,
    "total_tokens": 59
  },
  "_response_ms": 1753.426
}
```


## Turn on for logging only

Only apply PII Masking before logging to Langfuse, etc.

Not on the actual llm api request / response.

This is currently only applied for 
- `/chat/completion` requests
- on 'success' logging

1. Setup config.yaml
```yaml
litellm_settings:
  presidio_logging_only: true 

model_list:
  - model_name: gpt-3.5-turbo
    litellm_params:
      model: gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY
```

2. Start proxy

```bash
litellm --config /path/to/config.yaml
```

3. Test it! 

```bash
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer sk-1234' \
-D '{
  "model": "gpt-3.5-turbo",
  "messages": [
    {
      "role": "user",
      "content": "Hi, my name is Jane!"
    }
  ]
  }'
```


**Expected Logged Response**

```
Hi, my name is <PERSON>!
```