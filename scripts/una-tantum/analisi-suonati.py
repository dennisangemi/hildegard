# ------------------- start storico suonati ------------------- #

# filter storico_suonati per id_liturgia
storico_suonati = storico_suonati[storico_suonati['id_liturgia'] == id_liturgia]

# print storico_suonati
print("")
print("🔍 Storico dei canti suonati per la liturgia", id_liturgia)
print(storico_suonati)
print("")

# rimuovi la colonna titolo da mean_suonati (non serve perchè è già in storico_suonati e poi ci sarà merging)
mean_suonati = mean_suonati.drop(columns=['titolo'])

# add to storico_suonati the mean of the played songs from mean_suonati
print("🔍 Storico dei canti suonati con la media:")
storico_suonati = pd.merge(storico_suonati, mean_suonati, on='id_canti')
print(storico_suonati)
print("")

# keep only canti with cnt > mean
print("🔍 Storico dei canti suonati con la media e solo quelli con cnt > mean:")
storico_suonati = storico_suonati[storico_suonati['cnt'] > storico_suonati['mean']]

# add column max-cnt
storico_suonati['max-cnt'] = storico_suonati['max'] - storico_suonati['cnt']

# add column cnt/max
storico_suonati['cnt/max'] = (storico_suonati['cnt'] / storico_suonati['max']).round(2)

# add column deviation from mean
storico_suonati['dev'] = storico_suonati['cnt'] - storico_suonati['mean']

# add column normalized deviation from mean
storico_suonati['norm_dev'] = (storico_suonati['dev'] / storico_suonati['cnt']).round(2)

# add product of cnt/max and norm_dev
storico_suonati['prod'] = (storico_suonati['cnt/max'] * storico_suonati['norm_dev']).round(2)

# add cnt/max(cnt)
storico_suonati['cnt/max(cnt)'] = (storico_suonati['cnt'] / storico_suonati['cnt'].max()).round(2)

# compute the final score for suonati 
storico_suonati['score_suonati'] = ((0.3*storico_suonati['cnt/max'] + 0.3*storico_suonati['norm_dev'] + 0.4*storico_suonati['cnt/max(cnt)'])).round(2)

# normlalize score_suonati
storico_suonati['score_suonati'] = ((storico_suonati['score_suonati'] / storico_suonati['score_suonati'].max())).round(2)

# order by mean_metrics
storico_suonati = storico_suonati.sort_values(by='score_suonati', ascending=False)
print(storico_suonati)

# select only id_canti e score_suonati
storico_suonati = storico_suonati[['id_canti', 'score_suonati']]

# plot histogram of score_suonati with plt
plt.hist(storico_suonati['score_suonati'])
plt.show()

# a me interessano quelli con max-cnt basso e cnt-mean alto
# magari do più peso a cnt/max
# devo capire quale metrica è più rilevante

print(storico_suonati)
print("")

# pause user key
input("Premi invio per continuare...")

# ------------------- end storico suonati ------------------- #