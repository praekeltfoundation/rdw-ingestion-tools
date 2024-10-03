from api.survey import pySurvey

start = "2023-01-01T00:00:00"

survey = pySurvey.mqr.get_baseline(ts=start)

print(survey.head(5))
