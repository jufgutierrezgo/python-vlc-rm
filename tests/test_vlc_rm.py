import sys
sys.path.insert(1, '/home/juanpc/python_phd/cruft_sample/python-vlc-rm/src/')

# Import Constants Transmitter
from vlc_rm.transmitter import Transmitter
# Import Constants Photodetector
from vlc_rm.photodetector import Photodetector
# Import Constants Photodetecto
from vlc_rm.indoorenv import Indoorenv
# Import Constants Photodetector
from vlc_rm.recursivemodel import Recursivemodel

# from vlc_rm.cli import main

def test_main():
    # main([])

    led1 = Transmitter(
        "Led1",
        position=[2.5, 2.5, 3],
        normal=[0, 0, -1],
        mlambert=1,
        power=1,
        wavelengths=[650, 530, 430, 580],
        fwhm=[20, 12, 20, 20]
                    )
    led1.led_pattern()
    print(led1)

    pd1 = Photodetector(
        "PD1",
        position=[0.5, 1.0, 0],
        normal=[0, 0, 1],
        area=1e-4,
        fov=85,
        sensor='S10917-35GT'
                )
    pd1.plot_responsivity()
    print(pd1)

    room = Indoorenv(
        "Room", size=[5, 5, 3], no_reflections=3, resolution=1/4
                )

    room.set_reflectance('ceiling', [0.8, 0.8, 0.8, 0.8])
    room.set_reflectance('west', [0.8, 0.8, 0.8, 0.8])
    room.set_reflectance('north', [0.8, 0.8, 0.8, 0.8])
    room.set_reflectance('east', [0.8, 0.8, 0.8, 0.8])
    room.set_reflectance('south', [0.8, 0.8, 0.8, 0.8])
    room.set_reflectance('floor', [0.3, 0.3, 0.3, 0.3])
    room.create_envirorment(led1, pd1)
    print(room)

    channel_model = Recursivemodel("ChannelModelA", led1, pd1, room)
    channel_model.simulate_channel()
    print(channel_model)
    channel_model.print_Hk()

    assert (
        channel_model.rgby_dcgain[0] > 2.44e-06 and channel_model.rgby_dcgain[0] < 2.46e-06
        # channel_model.rgby_dcgain[0] == 2.5e-06
        )