"""
=======================
Baseball Reference WAR
=======================
"""

from pybaseballdatana.data import BaseballReferenceData
bbref_data = BaseballReferenceData()

print(bbref_data.war_bat)

print(bbref_data.war_bat.sort_values("WAR", ascending=False).head(6))
print(bbref_data.war_pitch.query("year_ID >= 1911").sort_values("WAR", ascending=False).head(6))