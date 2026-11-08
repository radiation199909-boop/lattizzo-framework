"""Step 1. Extract named dress terms from each record with a large language model.

Every call is appended to a JSONL file with the full raw reply, the parsed JSON, the model name returned by the API,
the SHA-256 of the prompt and the call time. The raw reply is kept unchanged so later steps can be checked against it.

Settings used in the paper: temperature 0 (left out when the API does not accept it), no reasoning mode,
one call per record, prompt prompts/extraction_prompt_v3.txt. Keys are read from a local .env file that is never committed:
    ANTHROPIC_API_KEY=...   OPENAI_API_KEY=...   DEEPSEEK_API_KEY=...

Example
    python src/extract.py --records demo/records.csv --provider openai --model <model> --out out/model_output.jsonl --limit 2
The demo does not need this step: demo/model_output.jsonl holds the cached replies of the main model for the demo records.
"""
import argparse, datetime, hashlib, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, load_records, parse_model_json

def load_env(path):
    if os.path.exists(path):
        for line in open(path, encoding='utf-8'):
            if '=' in line and not line.lstrip().startswith('#'):
                k, v = line.strip().split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"\''))


def make_client(provider):
    if provider == 'openai':
        import openai
        return openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    import anthropic
    if provider == 'deepseek':  # DeepSeek offers an Anthropic-compatible endpoint
        return anthropic.Anthropic(base_url='https://api.deepseek.com/anthropic', api_key=os.environ['DEEPSEEK_API_KEY'])
    return anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])


def call(client, provider, model, message, max_tokens, state):
    """Returns (reply text, model name reported by the API, token usage)."""
    if provider == 'openai':
        import openai
        kw = dict(model=model, max_completion_tokens=max_tokens, reasoning_effort='none',
                  messages=[{'role': 'user', 'content': message}])
        if state['temperature']:
            kw['temperature'] = 0
        try:
            r = client.chat.completions.create(**kw)
        except openai.BadRequestError as e:
            if state['temperature'] and 'temperature' in str(e):
                state['temperature'] = False
                kw.pop('temperature')
                r = client.chat.completions.create(**kw)
            else:
                raise
        return r.choices[0].message.content or '', r.model, dict(input=r.usage.prompt_tokens, output=r.usage.completion_tokens)
    import anthropic
    kw = dict(model=model, max_tokens=max_tokens, messages=[{'role': 'user', 'content': message}])
    # no reasoning: Claude 5.5 models take 'between_tools' (no tools are used here, so no reasoning is produced); DeepSeek takes 'disabled'
    kw['thinking'] = {'type': 'between_tools'} if provider == 'anthropic' else {'type': 'disabled'}
    if state['temperature']:
        kw['temperature'] = 0
    try:
        r = client.messages.create(**kw)
    except anthropic.BadRequestError as e:
        if state['temperature'] and 'temperature' in str(e):
            state['temperature'] = False
            kw.pop('temperature')
            r = client.messages.create(**kw)
        else:
            raise
    text = ''.join(b.text for b in r.content if getattr(b, 'type', '') == 'text')
    return text, r.model, dict(input=r.usage.input_tokens, output=r.usage.output_tokens)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--records', required=True)
    ap.add_argument('--provider', choices=['anthropic', 'openai', 'deepseek'], required=True)
    ap.add_argument('--model', required=True)
    ap.add_argument('--prompt', default=os.path.join(ROOT, 'prompts', 'extraction_prompt_v3.txt'))
    ap.add_argument('--out', required=True)
    ap.add_argument('--run', default='all', help='label stored with each call, e.g. gold, gold2, all')
    ap.add_argument('--ids', default='', help='comma-separated record ids; default all records')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--max-tokens', type=int, default=12000)
    ap.add_argument('--dry-run', action='store_true', help='print the first filled prompt and stop')
    a = ap.parse_args()

    load_env(os.path.join(ROOT, '.env'))
    template = open(a.prompt, encoding='utf-8').read()
    sha = hashlib.sha256(template.encode('utf-8')).hexdigest()
    records = load_records(a.records)
    ids = [x.strip() for x in a.ids.split(',') if x.strip()] or list(records)
    if a.limit:
        ids = ids[:a.limit]
    fill = lambda r: template.replace('{record_id}', r['record_id']).replace('{language}', r['language']).replace('{text}', r['text'])
    if a.dry_run:
        print(fill(records[ids[0]]))
        return
    client, state = make_client(a.provider), {'temperature': True}
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, 'a', encoding='utf-8') as f:
        for i, rid in enumerate(ids, 1):
            for attempt in range(5):  # retry transient errors only
                try:
                    raw, model, usage = call(client, a.provider, a.model, fill(records[rid]), a.max_tokens, state)
                    break
                except Exception as e:
                    if attempt == 4 or type(e).__name__ in ('BadRequestError', 'AuthenticationError', 'PermissionDeniedError', 'NotFoundError'):
                        raise
                    time.sleep(5 * (attempt + 1))
            parsed, _ = parse_model_json(raw)
            f.write(json.dumps(dict(record_id=rid, run=a.run, provider=a.provider, model_requested=a.model, model=model,
                                    temperature=0 if state['temperature'] else 'default',
                                    reasoning='none', prompt_sha256=sha, time=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
                                    usage=usage, raw=raw, parsed=parsed), ensure_ascii=False) + '\n')
            f.flush()
            print(f'{i}/{len(ids)} {rid} terms={len(parsed["terms"]) if parsed else "PARSE ERROR"}')


if __name__ == '__main__':
    main()
