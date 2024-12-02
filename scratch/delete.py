# df.style.set_properties(subset=['Name'], **{'text-align': 'center'})

# df.loc[df["decade"] == 2010,:].dropna()[["movie_title", "lift", "gross", "budget"]]




# df = df.loc[df["decade"] < 2020]
# sns.regplot(df, y="gross_log", x = "budget_log")

# # df = df.loc[df["decade"] > 1970]

# # Create a FacetGrid
# g = sns.FacetGrid(df, col="decade", height=5)

# # Map the regplot to each facet
# g.map(sns.regplot, "budget_log", "gross_log", scatter_kws={'s': 100, 'color': 'blue'}, line_kws={'color': 'red'})

# # Adjust the plot
# g.set_axis_labels("Gross (log)", "Budget (log)")
# g.set_titles("{col_name}")
# g.add_legend()

# # Show the plot
# plt.show()



# grp["growth_since_1990"] = (grp[('mean', 'lift', 2010)] - grp[('mean', 'lift', 1990)]) /grp[('mean', 'lift', 2010)] * 100

# grp.sort_values("growth_since_1990", ascending=False)
# grp["growth_since_1980"] = (grp[('mean', 'lift', 2010)] - grp[('mean', 'lift', 1980)]) /grp[('mean', 'lift', 2010)] * 100

# grp.sort_values("growth_since_1980", ascending=False)
# grp["growth_since_1970"] = (grp[('mean', 'lift', 2010)] - grp[('mean', 'lift', 1970)]) /grp[('mean', 'lift', 2010)] * 100

# grp.sort_values("growth_since_1970", ascending=False)
# (grp[('mean', 'lift', 1990)] + grp[('mean', 'lift', 2010)]) / grp[('mean', 'lift', 2010)] 

# grp.sort_values("growth_since_1990", ascending=False)

# (grp[('mean', 'lift', 1990)] + grp[('mean', 'lift', 2010)]) / grp[('mean', 'lift', 2010)] 
# list(grp)
# grp.sum(axis=1)
# g = sns.FacetGrid(df_explode, col = 'genre_clean', hue='genre_clean', col_wrap=4)
# g.map(sns.lineplot, 'gross_log', 'budget_log')
# g.set_titles('{col_name}')
# g.set_axis_labels('Gross', 'Budget') 
# g.fig.subplots_adjust(top=.9)
# g.fig.suptitle('test', fontsize=16)