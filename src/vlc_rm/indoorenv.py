import numpy as np


import torch

from vlc_rm.constants import Constants as Kt

from vlc_rm.transmitter import Transmitter

from vlc_rm.photodetector import Photodetector



class Indoorenv:
    """
    This class defines the indoor environment features, and computes
    the points grid and the cosine and distance pair-waise.

    """

    def __init__(
        self,
        name: str,
        size: np.ndarray,
        resolution: float,
        no_reflections: int = 3
    ) -> None:

        self._name = name
        self._size = np.array(size)
        self._resolution = resolution
        self._no_reflections = no_reflections

    @property
    def name(self):
        """The name property"""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def size(self) -> np.ndarray:
        """The size property"""
        return self._size

    @size.setter
    def size(self, value):
        print("Set size")
        self._size = value

    @property
    def no_reflections(self) -> int:
        """The number of reflections property"""
        return self._no_reflections

    @no_reflections.setter
    def no_reflections(self, value):
        self._no_reflections = value

    @property
    def resolution(self) -> float:
        """The resolution property"""
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        self._resolution = value

    def __str__(self) -> str:
        return (
            f'\n List of parameters for indoor envirionment: \n'
            f'Size [x y z] -> [m]: {self._size} \n'
            f'Order reflection: {self._no_reflections} \n'
            f'Resolution points [cm]: {self._resolution}'
        )

    def set_reflectance(self, wall_name, reflectance_wall):
        self._wall_name = wall_name
        self._reflectance_wall = np.array(reflectance_wall)

        if self._wall_name == 'ceiling':
            self._ceiling = self._reflectance_wall
        elif self._wall_name == 'west':
            self._west = self._reflectance_wall
        elif self._wall_name == 'north':
            self._north = self._reflectance_wall
        elif self._wall_name == 'east':
            self._east = self._reflectance_wall
        elif self._wall_name == 'south':
            self._south = self._reflectance_wall
        elif self._wall_name == 'floor':
            self._floor = self._reflectance_wall
        else:
            print('Invalid wall name.')

    def create_envirorment(
        self,
        tx_position: Transmitter,
        rx_position: Photodetector,
        tx_normal: Photodetector,
        rx_normal: Photodetector,
        fov: Photodetector
    ) -> None:

        self.create_grid(tx_position, rx_position, tx_normal, rx_normal)
        self.compute_parameters(fov)

    def create_grid(
        self,
        tx_position: np.ndarray,
        rx_position: np.ndarray,
        tx_normal: np.ndarray,
        rx_normal: np.ndarray
    ) -> None:

        no_xtick = int(self._size[0]/self._resolution)
        no_ytick = int(self._size[1]/self._resolution)
        no_ztick = int(self._size[2]/self._resolution)

        ceiling_points = np.zeros((no_xtick*no_ytick, 3), dtype=np.float16)
        west_points = np.zeros((no_ztick*no_xtick, 3), dtype=np.float16)
        north_points = np.zeros((no_ztick*no_ytick, 3), dtype=np.float16)
        east_points = np.zeros((no_ztick*no_xtick, 3), dtype=np.float16)
        south_points = np.zeros((no_ztick*no_ytick, 3), dtype=np.float16)
        floor_points = np.zeros((no_xtick*no_ytick, 3), dtype=np.float16)

        ceiling_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[0]], no_xtick*no_ytick, axis=0)
        east_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[1]], no_ztick*no_xtick, axis=0)
        south_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[2]], no_ztick*no_ytick, axis=0)
        west_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[3]], no_ztick*no_xtick, axis=0)
        north_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[4]], no_ztick*no_ytick, axis=0)
        floor_normal = np.repeat(
            [Kt.NORMAL_VECTOR_WALL[5]], no_xtick*no_ytick, axis=0)

        # Creates reflectance vector for each point
        ceiling_reflectance = np.repeat(
            [self._ceiling], no_xtick*no_ytick, axis=0)
        west_reflectance = np.repeat(
            [self._west], no_ztick*no_xtick, axis=0)
        north_reflectance = np.repeat(
            [self._north], no_ztick*no_ytick, axis=0)
        east_reflectance = np.repeat(
            [self._east], no_ztick*no_xtick, axis=0)
        south_reflectance = np.repeat(
            [self._south], no_ztick*no_ytick, axis=0)
        floor_reflectance = np.repeat(
            [self._floor], no_xtick*no_ytick, axis=0)

        x_ticks = np.linspace(
            self._resolution/2, self._size[0]-self._resolution/2, no_xtick)
        y_ticks = np.linspace(
            self._resolution/2, self._size[1]-self._resolution/2, no_ytick)
        z_ticks = np.linspace(
            self._resolution/2, self._size[2]-self._resolution/2, no_ztick)

        self.no_points = (
            2*no_xtick*no_ytick +
            2*no_ztick*no_xtick +
            2*no_ztick*no_ytick + 2)

        # Generates the x,y,z of grids in each points
        x_ygrid, y_xgrid = np.meshgrid(x_ticks, y_ticks)
        x_zgrid, z_xgrid = np.meshgrid(x_ticks, z_ticks)
        y_zgrid, z_ygrid = np.meshgrid(y_ticks, z_ticks)

        # Save x,y,z coordinates of points in each wall
        ceiling_points[:, 0] = floor_points[:, 0] = x_ygrid.flatten()
        ceiling_points[:, 1] = floor_points[:, 1] = y_xgrid.flatten()
        ceiling_points[:, 2], floor_points[:, 2] = self._size[2], 0

        west_points[:, 0] = east_points[:, 0] = x_zgrid.flatten()
        west_points[:, 2] = east_points[:, 2] = z_xgrid.flatten()
        east_points[:, 1], west_points[:, 1] = 0, self._size[1]

        north_points[:, 1] = south_points[:, 1] = y_zgrid.flatten()
        north_points[:, 2] = south_points[:, 2] = z_ygrid.flatten()
        south_points[:, 0], north_points[:, 0] = 0, self._size[0]

        # Creates tensors for gridpoints,
        # normal vectors and reflectance vectors.
        self.gridpoints = torch.from_numpy(np.concatenate((
            ceiling_points,
            east_points,
            south_points,
            west_points,
            north_points,
            floor_points,
            [tx_position],
            [rx_position]),
            axis=0
        ))

        self.normal_vectors = torch.from_numpy(np.concatenate((
            ceiling_normal,
            east_normal,
            south_normal,
            west_normal,
            north_normal,
            floor_normal,
            tx_normal,
            rx_normal),
            axis=0, dtype=np.float16)).reshape(self.no_points, 1, 3)

        self.reflectance_vectors = np.concatenate((
            ceiling_reflectance,
            east_reflectance,
            south_reflectance,
            west_reflectance,
            north_reflectance,
            floor_reflectance,
            [[0, 0, 0, 0]],
            [[0, 0, 0, 0]]), axis=0, dtype=np.float16)

        self.deltaA = (
            2*self._size[0]*self._size[1] +
            2*self._size[0]*self._size[2] +
            2*self._size[1]*self._size[2]
        )/(self.no_points-2)

    def compute_parameters(self, fov: float) -> None:
        """This function creates an 3d-array with cross-parametes between
            points.

        This parameters are the distance between points and the cosine of the
        angles respect to the normal vector. Using this array is commputed the
        channel immpulse response.

        Parameters:
            gridpoints: 2d tensor array with [x,y,z] coordinates for each point
            normal_vector: 2d tensor array with [x,y,z] coordinates of normal
                vector in each point

        Returns: Returns a 3d-array with distance and cos(tetha) parameters.
            The shape of this array is [2,no_points,no_points].


            _____________________
           /                    /|
          /                    / |
         /                    /  |
        /____________________/  /|
        |     Distance       | / |
        |____________________|/ /
        |     Cos(tetha)     | /
        |____________________|/


        """

        self.wall_parameters = np.zeros(
            (2, self.no_points, self.no_points), dtype=np.float16)

        # Computes pairwise-element distance using tensor
        # TODO: consider using Numpy only if possible
        dist = torch.cdist(self.gridpoints, self.gridpoints)

        # Computes the pairwise-difference (vector) using tensor
        diff = -self.gridpoints.unsqueeze(1) + self.gridpoints

        # Computes the unit vector from pairwise-difference usiing tensor
        unit_vector = torch.nan_to_num(torch.div(
            diff, dist.reshape(self.no_points, self.no_points, 1)), nan=0.0)

        # Computes the cosine of angle between unit vector and
        # normal vector using tensor.
        cos_phi = torch.sum(unit_vector*self.normal_vectors, dim=2)

        array_rx = np.asarray(cos_phi[-1, :])
        low_values_flags = array_rx < np.cos(fov*np.pi/180)
        array_rx[low_values_flags] = 0

        array_tx = np.asarray(cos_phi[-2, :])
        low_values_flags = array_tx < np.cos(90*np.pi/180)
        array_tx[low_values_flags] = 0

        # Save in numpy array the results of tensor calculations
        self.wall_parameters[0, :, :] = dist.numpy()
        self.wall_parameters[1, :, :] = cos_phi.numpy()
