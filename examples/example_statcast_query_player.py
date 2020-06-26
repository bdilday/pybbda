"""
=============================
Statcast Data - Player Query
=============================


"""

from matplotlib import pyplot as plt
import seaborn as sns
from pybbda.data import StatcastData

statcast_data = StatcastData()
ana_df = statcast_data.get_statcast_daily("batter", "2019-05-01", "2019-05-15", player_id=547989)


sns.distplot(ana_df.launch_speed)
plt.title("Jose Abreu - 2019-05-01 to 2019-05-15")
plt.show()

