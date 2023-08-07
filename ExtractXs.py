import h5py
import numpy as np
import csv

# Author: Angshuman Saharia Aug 2023
# Pull min Elev values from each X-section

def inspect_stations(file_path, xs_path, elevations_path, output_file):
    with h5py.File(file_path, "r") as f:
        xs_dataset = f[xs_path]
        elevation_dataset = f[elevations_path]

        num_stations = len(xs_dataset)
        num_elevations = elevation_dataset.shape[0]

        elevations_per_station = num_elevations // num_stations

        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['Station', 'Minimum Elevation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for i in range(num_stations):
                station = xs_dataset[i]
                station_elevations = elevation_dataset[i * elevations_per_station: (i + 1) * elevations_per_station, 1]

                neg_elevations = station_elevations[station_elevations < 0]

                if len(neg_elevations) > 0:
                    min_elevation = np.min(neg_elevations)
                else:
                    min_elevation = np.min(station_elevations)

                writer.writerow({'Station': station, 'Minimum Elevation': min_elevation})


file_path = "Z:\Greenbelt\Contraband_Bayou_RAS1D\BayouContraband.g07.hdf"
xs_path = "Geometry/Cross Sections/Attributes"
elevations_path = "Geometry/Cross Sections/Station Elevation Values"
output_file = "Z:\Greenbelt\Contraband_Bayou_RAS1D\output.csv"

inspect_stations(file_path, xs_path, elevations_path, output_file)
