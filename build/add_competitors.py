"""Insert competitor map + analysis into Competition Fit (pages 3-4); renumber figures +2 and pages >=4 by +1."""
import re, shutil
shutil.copy("proposal.html", "proposal_before_competitors.html")
s = open("proposal.html", encoding="utf-8").read()

# 1. figures +2
s = re.sub(r'\bFigure (\d+)\b', lambda m: f"Figure {int(m.group(1)) + 2}", s)
old_read = re.search(r'Figures 1–3 and 8 use published sector data\..*?after the pilot\.', s, re.S).group(0)
s = s.replace(old_read, "Figures 3–5 and 10 use published sector data. Figure 6 contains credited reference photographs. "
              "Figures 7, 8 and 14 show the software and CAD deliverables. Figures 1–2, 9, 11–13 and 15 show team "
              "assessments, sample inputs, financial assumptions or plans. Field results will be added after the pilot.")

# 2. page refs >= 4 shift by one
def shift(m):
    pre, a, sep, b = m.group(1), int(m.group(2)), m.group(3), m.group(4)
    f = lambda n: n + 1 if n >= 4 else n
    return f"{pre}{f(a)}" + (f"{sep}{f(int(b))}" if sep else "")
s = re.sub(r'\b(pp?\.)(\d+)(?:(–|-)(\d+))?', shift, s)
s = re.sub(r'<em>(\d+)</em>', lambda m: f"<em>{int(m.group(1)) + 1 if int(m.group(1)) >= 4 else m.group(1)}</em>", s)

# 3. overview entry for Competition Fit
s = s.replace('<b>Competition Fit and Proposal Guide</b><i></i><em>3</em></div><ul><li>Questions for the jury and where each is answered</li></ul>',
              '<b>Competition Fit and Proposal Guide</b><i></i><em>3–4</em></div><ul><li>Questions for the jury and where each is answered</li>'
              '<li>Market competitor map</li><li>Competitor analysis</li><li>What the analysis shows</li></ul>', 1)

# 4. new content at the end of the Competition Fit section
new = '''<p class="figt">Figure 1. Market competitor map</p>
<figure><img src="img/fig_comp_map.png" alt="Market competitor positioning map"><figcaption>Team positioning of the options a Malaysian cocoa grower can use today, based on the capability comparison on p.10. Positions are qualitative. [5, 6, 23, 24]</figcaption></figure>
<div style="break-before:page"></div>
<h2>Competitor Analysis</h2>
<p>Each option was scored on the eight capabilities in the comparison table on p.10 (Yes = 2, Partly = 1, No = 0), grouped into three jobs a grower needs done after heavy rain: deciding when and where to scout, capturing and identifying what is found, and verifying and reporting the result.</p>
<p class="figt">Figure 2. Competitor analysis by capability group</p>
<figure><img src="img/fig_comp_scores.png" alt="Competitor capability scores"><figcaption>Team assessment from public product descriptions and the cited studies. KokoShield is scored on planned pilot features, which are not yet field-validated. Scores will be checked with growers during discovery interviews. [5, 6, 23, 24]</figcaption></figure>
<h2>What the Analysis Shows</h2>
<table class="plain">
<tr><th style="width:26%">Finding</th><th>Implication for KokoShield</th></tr>
<tr><td><b>The top-right quadrant is empty</b></td><td>Forecast models provide the weather trigger, and field tools support the action, but no current option links the two into a block-level, time-limited route. This is the gap KokoShield targets.</td></tr>
<tr><td><b>Competitors score 2–3 out of 16</b></td><td>Each existing option does one job well. None covers planning, capture and verification together, which is where scouting time is lost after rain.</td></tr>
<tr><td><b>Diagnosis is not KokoShield’s strength</b></td><td>KokoShield scores 3 out of 4 on capture and diagnosis. It links to Plantix and PlantwisePlus rather than competing with them, so they can be partners rather than rivals.</td></tr>
<tr><td><b>The lead is on paper until tested</b></td><td>The 15 out of 16 score reflects planned features. The paired field comparison (pp.14–15) must show that the ranked route finds more confirmed pods per hour.</td></tr>
</table>
'''
anchor = 'user feedback and a regional prototype demonstration. [1, 22]</p>'
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + "\n" + new, 1)
open("proposal.html", "w", encoding="utf-8").write(s)
print(re.findall(r'pp?\.\d+(?:–\d+)?', s))
