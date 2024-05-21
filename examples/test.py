from api.aaq import pyAAQ

faqmatches = pyAAQ.faqmatches.get_faqmatches()

inbounds = pyAAQ.inbounds.get_inbounds(
    start_datetime="2023-01-01 00:00:00",
    end_datetime="2023-12-31 00:00:00"
    )

faqranks = pyAAQ.inbounds.get_faqranks(
    start_datetime="2023-01-01 00:00:00",
    end_datetime="2023-12-31 00:00:00"
    )

inbounds_ud = pyAAQ.inbounds_ud.get_inbounds_ud(
    start_datetime="2023-01-01 00:00:00",
    end_datetime="2023-12-31 00:00:00"
    )

urgency_rules = pyAAQ.urgency_rules.get_urgency_rules()

print(
    "FAQMatches :", faqmatches.head(5),
    "Inbounds :", inbounds.head(5),
    "Faqranks :", faqranks.head(5),
    "InboundsUD :", inbounds_ud.head(5),
    "UrgencyRules :", urgency_rules.head(5)
    )
