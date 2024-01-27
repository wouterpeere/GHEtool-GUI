"""
script to start the GUI
"""
import logging

import sys
import matplotlib.pyplot as plt
from pathlib import Path
from platform import system
from sys import argv
from ScenarioGUI import load_config
load_config(Path(__file__).parent.joinpath("gui_config.ini"))

os_system = system()
is_frozen = getattr(sys, 'frozen', False) and os_system == 'Windows'  # pragma: no cover


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

def run(path_list=None):  # pragma: no cover
    if is_frozen:
        import pyi_splash
        pyi_splash.update_text('Loading .')
    if os_system == 'Windows':
        from ctypes import windll as ctypes_windll
    from sys import exit as sys_exit

    if is_frozen:
        pyi_splash.update_text('Loading ..')

    from PySide6.QtWidgets import QApplication as QtWidgets_QApplication
    from PySide6.QtWidgets import QMainWindow as QtWidgets_QMainWindow
    from GHEtool import Borefield
    from GHEtoolGUI.data_2_borefield_func import data_2_borefield
    from GHEtoolGUI.gui_classes.translation_class import Translations
    from GHEtoolGUI.gui_structure import GUI
    from GHEtoolGUI.gui_classes.gui_combine_window import MainWindow
    import ScenarioGUI.global_settings as globs

    # adapt borefield class
    Borefield._plot_temperature_profile = _plot_temperature_profile
    Borefield._plot_load_duration = _plot_load_duration

    if is_frozen:
        pyi_splash.update_text('Loading ...')

    # init application
    app = QtWidgets_QApplication()
    if os_system == 'Windows':
        # set version and id
        myAppID = f'{globs.GUI_NAME} v{globs.VERSION}'  # arbitrary string
        ctypes_windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppID)

    # init window
    window = QtWidgets_QMainWindow()
    # init gui window
    main_window = MainWindow(window, app, GUI, Translations, result_creating_class=Borefield, data_2_results_function=data_2_borefield)
    if is_frozen:
        pyi_splash.update_text('Loading ...')
    # load file if it is in path list
    if path_list is not None:
        main_window.filename = ([path for path in path_list if path.endswith(f'.{globs.FILE_EXTENSION}')][0], 0)
        main_window.fun_load_known_filename()

    ghe_logger = logging.getLogger()
    ghe_logger.setLevel(logging.INFO)
    # show window
    if is_frozen:
        pyi_splash.close()

    ghe_logger.info(f'{globs.GUI_NAME} loaded!')
    window.showMaximized()
    # close app
    sys_exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    # pass system args like a file to read
    run(argv if len(argv) > 1 else None)
