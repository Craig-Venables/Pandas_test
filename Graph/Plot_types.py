import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

""" All graph types"""
def plot_iv(voltage, current, fontsize=8):
    # Plot voltage against current
    plt.plot(voltage, current, color='blue')
    plt.ylabel('Current', fontsize=fontsize)
    plt.xlabel('Voltage', fontsize=fontsize)

def plot_logiv(voltage, abs_current, fontsize=8):
    # Plot voltage against absolute current on a logarithmic scale
    plt.plot(voltage, abs_current, color='blue')
    plt.yscale("log")
    plt.ylabel('Abs Current', fontsize=fontsize)
    plt.xlabel('Voltage', fontsize=fontsize)

def plot_current_count(current, fontsize=8):
    # Plot current against its index
    plt.plot(range(len(current)), current, 'r-')
    plt.ylabel('Current', fontsize=fontsize)
    plt.xlabel('Index', fontsize=fontsize)

def plot_iv_avg(voltage, current, num_points=10, fontsize=8):
    # Plot averaged IV curve with arrows indicating direction
    step_size = len(voltage) // num_points
    print(step_size)
    # of broken check below:
    if step_size <= 1:
        step_size = 1
    avg_voltage = [np.mean(voltage[i:i + step_size]) for i in range(0, len(voltage), step_size)]
    avg_current = [np.mean(current[i:i + step_size]) for i in range(0, len(current), step_size)]

    plt.scatter(avg_voltage, avg_current, c='b', marker='o', label='Averaged Data', s=10)
    for i in range(1, len(avg_voltage)):
        plt.annotate('', xy=(avg_voltage[i], avg_current[i]), xytext=(avg_voltage[i - 1], avg_current[i - 1]),
                     arrowprops=dict(arrowstyle='->', color='red'))
    #plt.title(f'Averaged Data Showing {num_points} Data points with Arrows indicating direction')
    plt.grid(True)

def polar_subplot(x, y):
    fig, (ax1, ax2) = plt.subplots(1, 2, subplot_kw=dict(projection='polar'))
    ax1.plot(x, y)
    ax2.plot(x, y ** 2)
#

def sclc_ps(voltage, current_density, fontsize=8):
    # create scatter
    plt.plot(voltage, current_density, color='black')
    # Add labels and a title
    plt.yscale("log")
    plt.xscale("log")

    # plt.tick_params(axis='both', which='major', labelsize=fontsize)
    # plt.ylabel('current density positive (A/cm^2) ', fontsize= fontsize)
    # plt.xlabel('Voltage (V)', fontsize= fontsize)
    # plt.title('SCLC')


def sclc_ng(voltage, abs_current_density, fontsize=8):
    # create scatter
    #print(abs_current_density, voltage)
    plt.plot(voltage, abs_current_density, color='black')
    plt.yscale("log")
    plt.xscale("log")

    # Add labels and a title
    # plt.ylabel('Current density negative (A/cm^2)', fontsize= fontsize)
    # plt.xlabel('abs(Voltage) (V)', fontsize= fontsize)
    # plt.title('SCLC')


def schottky_emission_ps(voltage_half, current, fontsize=8):
    # create scatter
    plt.plot(voltage_half, current, color='black')
    # Add labels and a title
    plt.yscale("log")
    # plt.ylabel('Current (A) ', fontsize= fontsize)
    # plt.xlabel('Voltage (V^1/2)', fontsize= fontsize)
    # plt.title('Schottky Emission (positive)')


def schottky_emission_ng(voltage_half, abs_current, fontsize=8):
    # create scatter
    plt.plot(voltage_half, abs_current, color='black')
    # Add labels and a title
    plt.yscale("log")
    # plt.ylabel('abs(Current) (A) ', fontsize= fontsize)
    # plt.xlabel('Voltage (V^1/2)', fontsize= fontsize)
    # plt.title('Schottky Emission (Negative)')


def poole_frenkel_ps(current_voltage, voltage_half, fontsize=8):
    # create scatter
    plt.plot(current_voltage, voltage_half, color='black')
    # Add labels and a title
    plt.yscale("log")
    # plt.ylabel('Current/Voltage (A/V) ', fontsize= fontsize)
    # plt.xlabel('Voltage (V^1/2)', fontsize= fontsize)
    # plt.title('Poole-Frenkel (Positive')


def poole_frenkel_ng(abs_current_voltage, voltage_half, fontsize=8):
    # create scatter
    plt.plot(abs_current_voltage, voltage_half, color='black')
    # Add labels and a title
    plt.yscale("log")

    # plt.ylabel('abs(Current/Voltage) (A/V) ', fontsize= fontsize)
    # plt.xlabel('Voltage (V^1/2)', fontsize= fontsize)
    # plt.title('Poole-Frenkel (negative')


def resistance_time(resistance):
    plt.plot(range(len(resistance)), resistance, color='black')
