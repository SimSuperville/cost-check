import json, glob, os, sys

def bar(pct, width=20):
    if pct >= 100:
        return '▓' * width
    filled = int((pct / 100) * width)
    return '█' * filled + '░' * (width - filled)

def fmt(n):
    if n >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if n >= 1_000:     return f"{n/1_000:.1f}k"
    return str(n)

PLANS = [
    ('Pro     ($20/mo  ~326k )', 326_000),
    ('Max 5x  ($100/mo ~1.63M)', 1_630_000),
    ('Max 20x ($200/mo ~6.52M)', 6_520_000),
]

project_dir = os.path.expanduser("~/.claude/projects")
files = glob.glob(f"{project_dir}/**/*.jsonl", recursive=True)

if not files:
    print("⚠️  No session data found in ~/.claude/projects/")
    sys.exit(0)

latest = max(files, key=os.path.getmtime)

turns = []
mcp_calls = []
skill_calls = []
tool_results = {}

with open(latest) as f:
    raw_lines = f.readlines()

for line in raw_lines:
    line = line.strip()
    if not line:
        continue
    try:
        obj = json.loads(line)
    except Exception:
        continue

    if obj.get('type') == 'assistant':
        msg = obj.get('message', {})
        usage = msg.get('usage', {})
        if usage:
            inp = usage.get('input_tokens', 0)
            out = usage.get('output_tokens', 0)
            cr  = usage.get('cache_read_input_tokens', 0)
            cw  = usage.get('cache_creation_input_tokens', 0)
            if inp + out > 0:
                turns.append({'input': inp, 'output': out, 'cache_read': cr, 'cache_write': cw})
        for c in msg.get('content', []) or []:
            if isinstance(c, dict) and c.get('type') == 'tool_use':
                name = c.get('name', '')
                tid  = c.get('id')
                if name.startswith('mcp__'):
                    server = name.split('__')[1] if '__' in name[5:] else 'unknown'
                    mcp_calls.append({'id': tid, 'name': name, 'server': server})
                elif name == 'Skill':
                    skill_name = (c.get('input') or {}).get('skill', 'unknown')
                    skill_calls.append({'id': tid, 'skill': skill_name})

    elif obj.get('type') == 'user':
        content = obj.get('message', {}).get('content', [])
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict) and c.get('type') == 'tool_result':
                    tid = c.get('tool_use_id')
                    body = c.get('content', '')
                    if isinstance(body, list):
                        body = ''.join(
                            (b.get('text', '') if isinstance(b, dict) else str(b))
                            for b in body
                        )
                    tool_results[tid] = len(str(body))

if not turns:
    print("⚠️  No token data found yet in this session.")
    sys.exit(0)

# Exclude the trailing /cost-check invocation overhead
real_turns = turns[:-1] if len(turns) > 1 and turns[-1]['input'] + turns[-1]['output'] < 500 else turns

last      = real_turns[-1] if real_turns else turns[-1]
last_in   = last['input']
last_out  = last['output']
last_cr   = last['cache_read']
last_cw   = last['cache_write']
last_tot  = last_in + last_out

sess_in   = sum(t['input']  for t in real_turns)
sess_out  = sum(t['output'] for t in real_turns)
sess_tot  = sess_in + sess_out
n_turns   = len(real_turns)

# Estimate tokens consumed by MCP/Skill tool results (rough: chars / 4)
def est_tokens(call_list):
    total_chars = sum(tool_results.get(c['id'], 0) for c in call_list)
    return total_chars // 4

mcp_tokens   = est_tokens(mcp_calls)
skill_tokens = est_tokens(skill_calls)

# Per-server breakdown for MCP
mcp_by_server = {}
for c in mcp_calls:
    s = c['server']
    mcp_by_server.setdefault(s, {'count': 0, 'tokens': 0})
    mcp_by_server[s]['count']  += 1
    mcp_by_server[s]['tokens'] += tool_results.get(c['id'], 0) // 4

# Per-skill breakdown
skill_by_name = {}
for c in skill_calls:
    n = c['skill']
    skill_by_name.setdefault(n, {'count': 0, 'tokens': 0})
    skill_by_name[n]['count']  += 1
    skill_by_name[n]['tokens'] += tool_results.get(c['id'], 0) // 4

W = 58

print()
print('⚡ /cost-check')
print('─' * W)
print(f"  {'':22}  {'INPUT':>8}  {'OUTPUT':>8}  {'TOTAL':>8}")
print(f"  {'Last message':22}  {fmt(last_in):>8}  {fmt(last_out):>8}  {fmt(last_tot):>8}")
print(f"  {'Session (' + str(n_turns) + ' turns)':22}  {fmt(sess_in):>8}  {fmt(sess_out):>8}  {fmt(sess_tot):>8}")
if last_cr or last_cw:
    print(f"  {'Cache (last msg)':22}  read {fmt(last_cr):>6}  write {fmt(last_cw):>6}")
print()
print('  LAST MESSAGE  ── as % of 5-hr plan window')
for label, limit in PLANS:
    pct = last_tot / limit * 100
    b   = bar(pct)
    flag = '  ⚠️ EXCEEDED' if pct > 100 else ''
    print(f"  {label}  {b}  {pct:5.1f}%{flag}")
print()
print('  SESSION TOTAL ── as % of 5-hr plan window')
for label, limit in PLANS:
    pct = sess_tot / limit * 100
    b   = bar(pct)
    flag = '  ⚠️ EXCEEDED' if pct > 100 else ''
    print(f"  {label}  {b}  {pct:5.1f}%{flag}")

if mcp_calls or skill_calls:
    print()
    print('  MCP & SKILL INSIGHTS  ── est. tokens added to context')
    if mcp_calls:
        print(f"  {'MCP calls':22}  {len(mcp_calls):>4} calls    ~{fmt(mcp_tokens):>6} tokens")
        for srv, stats in sorted(mcp_by_server.items(), key=lambda x: -x[1]['tokens'])[:5]:
            print(f"    └─ {srv:<32}  {stats['count']:>3} × ~{fmt(stats['tokens'])}")
    if skill_calls:
        print(f"  {'Skill calls':22}  {len(skill_calls):>4} calls    ~{fmt(skill_tokens):>6} tokens")
        for sk, stats in sorted(skill_by_name.items(), key=lambda x: -x[1]['tokens'])[:5]:
            print(f"    └─ {sk:<32}  {stats['count']:>3} × ~{fmt(stats['tokens'])}")
    pct_of_session = (mcp_tokens + skill_tokens) / sess_tot * 100 if sess_tot else 0
    print(f"  (~{pct_of_session:.1f}% of session input is MCP/Skill response payload)")

print('─' * W)
