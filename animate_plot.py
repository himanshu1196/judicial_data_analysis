import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def update_plot(i, data, scat):
	# scat.set_facecolor([data[i], data[i], data[i]])
	scat = scat.set_offset(data[i])
	return scat,

def animate_plot_for(tenure_pendency_by_year_dist):
# year_and_dist_wise_tenures = pd.read_csv('generated/karnataka_year_dist_wise_judge_tenures.csv')
# year_and_dist_wise_pendency_data = pd.read_csv('generated/karnataka_dist_wise_pendency_data_by_year.csv')
# tenure_pendency_by_year_dist = year_and_dist_wise_pendency_data.merge(year_and_dist_wise_tenures, how = 'inner', on = ['year', 'state_code', 'dist_code'])
	f, axs = plt.subplots(3,3)
	f.set_figwidth(15)
	f.set_figheight(10)
	categories = np.unique(tenure_pendency_by_year_dist['year'])
	colors = np.linspace(0, 1, len(categories))
	colordict = dict(zip(categories, colors))  

	tenure_pendency_by_year_dist["Color"] = tenure_pendency_by_year_dist['year'].apply(lambda x: colordict[x])
	
	num_points = 30
	for j in range(3):
		for k in range(3):
			i = 3 * j + k
			axs[j,k].set_ylim([0,1.25])
			axs[j,k].scatter(tenure_pendency_by_year_dist['avg_judge_count'][i*num_points:(i+1)*num_points], tenure_pendency_by_year_dist['new_clearance_rate'][i*num_points:(i+1)*num_points], c = tenure_pendency_by_year_dist['year'][i*num_points:(i+1)*num_points])
			axs[j,k].set_title(tenure_pendency_by_year_dist['year'][i*num_points])

	for ax in axs.flat:
		ax.set(xlabel='avg_judge_count', ylabel='new_clearance_rate')

	# Hide x labels and tick labels for top plots and y ticks for right plots.
	for ax in axs.flat:
		ax.label_outer()
	# sctr_plt = ax.scatter(tenure_pendency_by_year_dist['num_appointments'][:31], tenure_pendency_by_year_dist['new_clearance_rate'][:31], c = tenure_pendency_by_year_dist['year'][:31])
	# # sctr_plt = ax.scatter(tenure_pendency_by_year_dist['num_appointments'][:31], tenure_pendency_by_year_dist['new_clearance_rate'][:31], c = tenure_pendency_by_year_dist['year'][:31])
	# # produce a legend with the unique colors from the scatter
	# legend1 = ax.legend(*sctr_plt.legend_elements(),
	# 					loc="lower right", title="Years")
	# # print(legend1)
	# ax.add_artist(legend1)

	# numframes = len(tenure_pendency_by_year_dist)
	# numpoints = 30
	# ani = animation.FuncAnimation(f, update_plot, frames=range(numframes), fargs=((tenure_pendency_by_year_dist['year']), sctr_plt), blit = True)
	plt.show()
	# ax.scatter(tenure_pendency_by_year_dist['num_appointments'][:30], tenure_pendency_by_year_dist['new_clearance_rate'][:30], c = tenure_pendency_by_year_dist['year'][:30])
	# plt.draw()
	# plt.pause(0.5)
	# plt.clf()
	# ax.scatter(tenure_pendency_by_year_dist['num_appointments'][30:60], tenure_pendency_by_year_dist['new_clearance_rate'][30:60], c = tenure_pendency_by_year_dist['year'][30:60])
	# plt.draw()
	# plt.pause(0.5)
	# plt.clf()

	# plt.xlabel('Number of appointments')
	# plt.ylabel('New clearance rate')
	# plt.title('Karnataka districts')
	# plt.savefig('generated/karnataka_dist_year_wise_clearance_and_appointments.png')

def plot_for(tenure_pendency_by_year_dist):
	f, axs = plt.subplots()
	f.set_figwidth(15)
	f.set_figheight(10)
	categories = np.unique(tenure_pendency_by_year_dist['year'])
	colors = np.linspace(0, 1, len(categories))
	colordict = dict(zip(categories, colors))  

	tenure_pendency_by_year_dist["Color"] = tenure_pendency_by_year_dist['year'].apply(lambda x: colordict[x])
	
	num_points = 30
	# for j in range(3):
	# 	for k in range(3):
	# 		i = 3 * j + k
	# axs[j,k].set_ylim([0,1.25])
	# axs[j,k].scatter(tenure_pendency_by_year_dist['median_appointment_duration'], tenure_pendency_by_year_dist['new_clearance_rate'], c = tenure_pendency_by_year_dist['year'])
	# axs[j,k].set_title(tenure_pendency_by_year_dist['year'][i*num_points])

	# for ax in axs.flat:
	# 	ax.set(xlabel='median_appointment_duration', ylabel='new_clearance_rate')

	# # Hide x labels and tick labels for top plots and y ticks for right plots.
	# for ax in axs.flat:
		# ax.label_outer()
	sctr_plt = axs.scatter(tenure_pendency_by_year_dist['avg_judge_count'], tenure_pendency_by_year_dist['new_clearance_rate'], c = tenure_pendency_by_year_dist['year'])
	# sctr_plt = ax.scatter(tenure_pendency_by_year_dist['num_appointments'][:31], tenure_pendency_by_year_dist['new_clearance_rate'][:31], c = tenure_pendency_by_year_dist['year'][:31])
	# produce a legend with the unique colors from the scatter
	legend1 = axs.legend(*sctr_plt.legend_elements(),
						loc="lower right", title="Years")
	# print(legend1)
	axs.add_artist(legend1)

	# numframes = len(tenure_pendency_by_year_dist)
	# numpoints = 30
	# ani = animation.FuncAnimation(f, update_plot, frames=range(numframes), fargs=((tenure_pendency_by_year_dist['year']), sctr_plt), blit = True)
	# plt.show()
	# ax.scatter(tenure_pendency_by_year_dist['num_appointments'][:30], tenure_pendency_by_year_dist['new_clearance_rate'][:30], c = tenure_pendency_by_year_dist['year'][:30])
	# plt.draw()
	# plt.pause(0.5)
	# plt.clf()
	# ax.scatter(tenure_pendency_by_year_dist['num_appointments'][30:60], tenure_pendency_by_year_dist['new_clearance_rate'][30:60], c = tenure_pendency_by_year_dist['year'][30:60])
	# plt.draw()
	# plt.pause(0.5)
	# plt.clf()

	plt.xlabel('Avg daily judge strength')
	plt.ylabel('New clearance rate')
	plt.title('Karnataka districts')
	plt.savefig('generated/karnataka_strength_pendency_by_year_dist.png')

if __name__ == '__main__':
	# year_and_dist_wise_tenures = pd.read_csv('generated/karnataka_year_dist_wise_judge_tenures.csv')
	# year_and_dist_wise_pendency_data = pd.read_csv('generated/karnataka_dist_wise_pendency_data_by_year.csv')
	# tenure_pendency_by_year_dist = year_and_dist_wise_pendency_data.merge(year_and_dist_wise_tenures, how = 'inner', on = ['year', 'state_code', 'dist_code'])
	tenure_pendency_by_year_dist = pd.read_csv('generated/strength_pendency_by_year_dist.csv')
	animate_plot_for(tenure_pendency_by_year_dist)