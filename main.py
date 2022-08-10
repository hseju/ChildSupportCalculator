from app import db, Respondents
import pandas as pd

result = Respondents.query.get(3)

print(result)
