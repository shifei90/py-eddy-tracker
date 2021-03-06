from matplotlib import pyplot as plt
from py_eddy_tracker.dataset.grid import RegularGridDataset
grid_name, lon_name, lat_name = 'nrt_global_allsat_phy_l4_20190223_20190226.nc', 'longitude', 'latitude'
if False:

    h = RegularGridDataset(grid_name, lon_name, lat_name)
    
    fig = plt.figure(figsize=(14, 12))
    ax = fig.add_axes([.02, .51, .9, .45])
    ax.set_title('ADT (m)')
    ax.set_ylim(-75, 75)
    ax.set_aspect('equal')
    m = h.display(ax, name='adt', vmin=-1, vmax=1)
    ax.grid(True)
    plt.colorbar(m, cax=fig.add_axes([.94, .51, .01, .45]))
    h = RegularGridDataset(grid_name, lon_name, lat_name)
    h.bessel_high_filter('adt', 500, order=3)
    ax = fig.add_axes([.02, .02, .9, .45])
    ax.set_title('ADT Filtered (m)')
    ax.set_aspect('equal')
    ax.set_ylim(-75, 75)
    m = h.display(ax, name='adt', vmin=-.1, vmax=.1)
    ax.grid(True)
    plt.colorbar(m, cax=fig.add_axes([.94, .02, .01, .45]))
    fig.savefig('png/filter.png')

if True:
    import logging
    logging.getLogger().setLevel('DEBUG') # Values: ERROR, WARNING, INFO, DEBUG
    from datetime import datetime
    h = RegularGridDataset(grid_name, lon_name, lat_name)
    h.bessel_high_filter('adt', 500, order=3)
    # h.bessel_high_filter('adt', 300, order=1)
    date = datetime(2019, 2, 23)
    a, c = h.eddy_identification(
        'adt', 'ugos', 'vgos', # Variable to use for identification
        date, # Date of identification
        0.002, # step between two isolines of detection (m)
        # 0.02, # step between two isolines of detection (m)
        pixel_limit=(5, 2000), # Min and max of pixel can be include in contour
        shape_error=55, # Error maximal of circle fitting over contour to be accepted
        bbox_surface_min_degree=.125 ** 2, # degrees surface minimal to take in account contour
        )
    fig = plt.figure(figsize=(15,7))
    ax = fig.add_axes([.03,.03,.94,.94])
    ax.set_title('Eddies detected -- Cyclonic(red) and Anticyclonic(blue)')
    ax.set_ylim(-75,75)
    ax.set_xlim(0,360)
    ax.set_aspect('equal')
    a.display(ax, color='b', linewidth=.5)
    c.display(ax, color='r', linewidth=.5)
    ax.grid()
    fig.savefig('png/eddies.png')
