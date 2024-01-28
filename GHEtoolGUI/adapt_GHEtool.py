import matplotlib.pyplot as plt


def _plot_temperature_profile(self, legend: bool = True, plot_hourly: bool = False):
    """
    This function plots the temperature profile.
    If the Borefield object exists as part of the GUI, than the figure is returned,
    otherwise it is shown.

    Parameters
    ----------
    legend : bool
        True if the legend should be printed
    plot_hourly : bool
        True if the temperature profile printed should be based on the hourly load profile.

    Returns
    -------
    fig, ax
        If the borefield object is part of the GUI, it returns the figure object
    """

    # make a time array
    if plot_hourly:
        time_array = self.load.time_L4 / 12 / 3600 / 730
    else:
        time_array = self.load.time_L3 / 12 / 730. / 3600.

    # plt.rc('figure')
    # create new figure and axes if it not already exits otherwise clear it.
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # set axes labelsv
    ax.set_xlabel(r'Time (year)')
    ax.set_ylabel(r'Temperature ($^\circ C$)')
    ax.yaxis.label.set_color(plt.rcParams["axes.labelcolor"])
    ax.xaxis.label.set_color(plt.rcParams["axes.labelcolor"])

    # plot Temperatures
    ax.step(time_array, self.results.Tb, 'k-', where="post", lw=1.5, label="Tb")

    if plot_hourly:
        ax.step(time_array, self.results.peak_cooling, 'b-', where="post", lw=1, label='Tf')
    else:
        ax.step(time_array, self.results.peak_cooling, 'b-', where="post", lw=1.5, label='Tf peak cooling')
        ax.step(time_array, self.results.peak_heating, 'r-', where="post", lw=1.5, label='Tf peak heating')

        ax.step(time_array, self.results.monthly_cooling, color='b', linestyle="dashed", where="post", lw=1.5,
                label='Tf base cooling')
        ax.step(time_array, self.results.monthly_heating, color='r', linestyle="dashed", where="post", lw=1.5,
                label='Tf base heating')

    # define temperature bounds
    ax.hlines(self.Tf_min, 0, self.simulation_period, colors='r', linestyles='dashed', label='', lw=1)
    ax.hlines(self.Tf_max, 0, self.simulation_period, colors='b', linestyles='dashed', label='', lw=1)
    ax.set_xticks(range(0, self.simulation_period + 1, 2))

    # Plot legend
    if legend:
        ax.legend()
    ax.set_xlim(left=0, right=self.simulation_period)
    # show figure if not in gui mode
    return fig, ax

def _plot_load_duration(self, legend: bool = False):
    """
    This function makes a load-duration curve from the hourly values.

    Parameters
    ----------
    legend : bool
        True if the figure should have a legend

    Returns
    ----------
    Tuple
        plt.Figure, plt.Axes
    """
    # sort heating and cooling load
    heating = self._secundary_borefield_load.hourly_heating_load.copy()
    heating[::-1].sort()

    cooling = self._secundary_borefield_load.hourly_cooling_load.copy()
    cooling.sort()
    cooling = cooling * (-1)
    # create new figure and axes if it not already exits otherwise clear it.
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # add sorted loads to plot
    ax.step(range(0, 8760, 1), heating, 'r-', label="Heating")
    ax.step(range(0, 8760, 1), cooling, 'b-', label="Cooling")
    # create 0 line
    ax.hlines(0, 0, 8759, color="black")
    # add labels
    ax.set_xlabel("Time [hours]")
    ax.set_ylabel("Power [kW]")
    # set x limits to 8760
    ax.set_xlim(0, 8760)
    # plot legend if wanted
    if legend:
        ax.legend()  # pragma: no cover
    return fig, ax