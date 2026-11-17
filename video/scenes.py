"""Scene list for the KokoShield two-minute pitch. Shared by the frame renderer, the narration
builder and the storyboard. Images are relative to C:/Users/User/Documents/GSC/build/img."""

SCENES = [
    dict(id=1, title="Hook", kicker="KokoShield · GSC 2026–27 · Food Resilience",
         head="After heavy rain, a cocoa grower has 30 minutes.<br>Which blocks should they check first?",
         img="photoB.jpeg", layout="hero",
         narration="After a heavy rain, a cocoa grower has about thirty minutes to scout. "
                   "Which blocks should they check first? Guess wrong, and black pod spreads to healthy pods."),
    dict(id=2, title="The climate risk", kicker="The problem",
         head="Rain drives black pod, and heavy rain already cuts cocoa yields",
         stats=[("20–30%", "of global cocoa production lost to black pod each year [Guest 2007]"),
                ("3 countries", "Ghana, Ecuador and Indonesia: heavy rain linked to lower cocoa yield [PNAS 2026]"),
                ("86%", "of Malaysian cocoa area is smallholdings [MCB 2025]")],
         layout="stats",
         narration="Black pod is spread by rain splash, and it is estimated to cost twenty to thirty percent of global cocoa production. "
                   "Heavy rain is already linked to lower yields in Ghana, Ecuador and Indonesia. "
                   "In Malaysia, eighty-six percent of cocoa land is smallholdings, where advisers cannot visit every farm after every storm."),
    dict(id=3, title="The market gap", kicker="What is missing",
         head="Tools diagnose, forecast or record.<br>None turns rain into a scouting route.",
         img="fig_comp_map.png", layout="figure",
         narration="Growers already have photo apps, forecasts and paper logs. "
                   "But none of them turns it rained heavily into walk these blocks first, in the time you have. "
                   "That empty corner is where KokoShield sits."),
    dict(id=4, title="The solution", kicker="KokoShield Field Desk",
         head="Rain reading in. Ranked 30-minute route out.",
         imgs=["g_mobile_plan.jpg", "g_print.jpg"], layout="two",
         bullets=["30 mm trigger starts a round", "Wet blocks and past cases rank first",
                  "Reason shown beside every stop", "Works on a phone or on paper"],
         narration="KokoShield Field Desk takes the rain reading, the farm's block map and past cases, "
                   "and produces a ranked route sized to thirty minutes. Every stop shows why it is there, "
                   "and the route works on a phone or as a printed checklist."),
    dict(id=5, title="Record and confirm", kicker="Scout log",
         head="Scouts record. An adviser confirms.",
         img="g_scoutlog.jpg", layout="figure",
         narration="Scouts log each suspected pod with a note and a photo. "
                   "The grower or an adviser then confirms or rules out every case, so only verified disease counts."),
    dict(id=6, title="The pilot", kicker="How we will prove it",
         head="One farm. Two scouts. Same 30 minutes.",
         img="g_compare.jpg", layout="split",
         bullets=["Tanjung Sepat, Selangor · target 4 post-rain rounds",
                  "Ranked route vs the grower’s usual round",
                  "Primary measure: confirmed pods per scouting hour",
                  "Go on if better in at least 3 of 4 rounds",
                  "Pilot budget: RM1,200"],
         narration="Our pilot is one cocoa farm in Tanjung Sepat. Two scouts walk for the same thirty minutes, "
                   "one on the ranked route and one on the usual round, then a follow-up check counts what each missed. "
                   "We move on only if the ranked route finds more confirmed pods per hour in at least three of four rounds. "
                   "The pilot costs twelve hundred ringgit."),
    dict(id=7, title="Impact and market", kicker="Sustainable impact · Route to market",
         head="Less crop lost. Targeted treatment.<br>Free for growers, paid by sponsors.",
         stats=[("SDG 2 + 13", "Targets 2.3, 2.4 and 13.1: smallholder income, resilient farming and climate adaptation"),
                ("RM75", "per active farm per season, paid by a cooperative or buyer. Free for growers"),
                ("20 → 60", "active farms: first paid cluster in Sabah or Sarawak in 2027, three clusters in 2028")],
         layout="stats",
         narration="Finding disease sooner means fewer pods lost and treatment only where it is needed. "
                   "Growers use KokoShield for free. A cooperative or buyer pays seventy-five ringgit per farm per season, "
                   "starting with a twenty-farm cluster in Sabah or Sarawak in 2027."),
    dict(id=8, title="Close", kicker="Universiti Malaya",
         head="Find disease sooner after the rain.",
         sub="Leow Shen En · Chong Pohyi · Choong Zhuo Lin · Lee Jia Shern · Teoh Xi Xian",
         img="photoA.jpeg", layout="hero",
         narration="We are a team of five from Universiti Malaya. KokoShield helps cocoa growers find disease sooner after the rain, "
                   "starting with one farm and built to travel to every cocoa region facing wetter seasons."),
]

# Narration v3: lightly trimmed so the natural voice fits each scene's fixed slot in the 3D timeline.
NARRATION_V3 = {
    1: "After heavy rain, a cocoa grower has about thirty minutes to scout. Which blocks should they check first? Guess wrong, and black pod spreads to healthy pods.",
    2: "Black pod spreads by rain splash and costs an estimated twenty to thirty percent of global cocoa production. Heavy rain is already linked to lower yields in Ghana, Ecuador and Indonesia. In Malaysia, eighty-six percent of cocoa land is smallholdings, and advisers can't visit every farm after every storm.",
    3: "Growers already have photo apps, forecasts and paper logs. But none of them turns \"it rained heavily\" into \"walk these blocks first, in the time you have\". That empty corner is where KokoShield sits.",
    4: "KokoShield Field Desk combines the rain reading, the block map and past cases into a ranked route that fits thirty minutes. Every stop shows why it's there, on a phone or a printed checklist.",
    5: "Scouts log each suspected pod with a note and a photo. An adviser then confirms or rules out every case, so only verified disease counts.",
    6: "Our pilot runs on one cocoa farm in Tanjung Sepat. Two scouts walk the same thirty minutes: one on the ranked route, one on the usual round. A follow-up check counts what each missed. We go ahead only if the ranked route finds more confirmed pods per hour in three of four rounds. The pilot budget is twelve hundred ringgit.",
    7: "Finding disease sooner means fewer pods lost, and treatment only where it's needed. Growers use KokoShield for free. A cooperative or buyer pays seventy-five ringgit per farm per season, starting with a twenty-farm cluster in Sabah or Sarawak in 2027.",
    8: "We're a team of five from Universiti Malaya. KokoShield helps cocoa growers find disease sooner after the rain: one farm first, then every cocoa region facing wetter seasons.",
}
for _s in SCENES:
    _s["narration"] = NARRATION_V3[_s["id"]]
