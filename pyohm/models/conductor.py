import math
from datetime import datetime

import pyohm.units as units
from pyohm.models.base import Base

# Polynomial coefficients for solar heat intensity as a function of
# solar altitude corresponding to clear atmosphere
PolynomialCoefficientsOfClearAtmosphere: dict[str, float] = {
    "A": -42.2391,
    "B": 63.8044,
    "C": -1.9220,
    "D": 3.46921e-2,
    "E": -3.61118e-4,
    "F": 1.94318e-6,
    "G": -4.07608e-9,
}

# Polynomial coefficients for solar heat intensity as a function of
# solar altitude corresponding to industrial atmosphere
PolynomialCoefficientsOfIndustrialAtmosphere: dict[str, float] = {
    "A": 53.1821,
    "B": 14.2110,
    "C": 6.6138e-1,
    "D": -3.1658e-2,
    "E": 5.4654e-4,
    "F": -4.3446e-6,
    "G": 1.3236e-8,
}


class DrakeConductorSpec(Base):
    # Ref: https://assets.southwire.com/ImConvServlet/imconv/\
    #   6e40b948ad8bbb2c69490138659678cbf373c912/origin?hybrisId=otmmHybrisPRD&assetDescr=ACSR-Dec-2020
    name: str = "Drake"

    kcmil: float = 795

    # feet to meter
    diameter: float = 1.107 * 0.0254

    low_temperature: float = 25

    high_temperature: float = 75

    ac_resistance_low: float = 0.0214 / 1000 / 0.3048 * 1.02

    ac_resistance_high: float = 0.0263 / 1000 / 0.3048

    unit_mapping = {
        "kcmil": units.Kciml,
        "diameter": units.Meter,
        "low_temperature": units.DegreeC,
        "high_temperature": units.DegreeC,
        "ac_resistance_low": units.OhmPerMeter,
        "ac_resistance_high": units.OhmPerMeter,
    }


class Weather(Base):
    name: str = "Weather"

    emissivity: float = 0.8

    solar_absorptivity: float = 0.8


class Conductor(Base):

    wind_speed: float

    wind_direction: float

    emissivity: float

    solar_absorption: float

    ambient_temperature: float

    conductor_surface_temperature: float

    aluminum_strand_layers_average_temperature: float

    max_allowable_conductor_temperature: float

    conductor_outside_diameter: float

    conductor_low_temperature: float

    conductor_high_temperature: float

    conductor_ac_resistance_low: float

    conductor_ac_resistance_high: float

    azimuth_of_conductor: float

    latitude: float

    clear_atmosphere: bool

    date: datetime

    elevation: float

    def __init__(self) -> None: ...

    def use_default(self) -> None:
        """
        Use default values from Drake ASCR for conductor attributes.
        """
        drake = DrakeConductorSpec()
        self.conductor_outside_diameter = drake.diameter

        self.conductor_low_temperature = drake.low_temperature
        self.conductor_high_temperature = drake.high_temperature
        self.conductor_ac_resistance_low = drake.ac_resistance_low
        self.conductor_ac_resistance_high = drake.ac_resistance_high

        self.max_allowable_conductor_temperature = 100.0

        self.aluminum_strand_layers_average_temperature = self.max_allowable_conductor_temperature

        self.conductor_surface_temperature = 45.0

        self.latitude = 30.0

        self.elevation = 0.0

        self.clear_atmosphere = True

        self.ambient_temperature = 40.0

        self.wind_speed = 0.61

        self.wind_direction = 90.0

        self.date = datetime(year=2023, month=6, day=10, hour=11)

        self.azimuth_of_conductor = 90.0

    @property
    def number_of_day(self) -> int:
        start_date = datetime(year=self.date.year, month=1, day=1)
        delta = start_date - self.date.replace(hour=0, minute=0, second=0, microsecond=0)
        return delta.days

    @property
    def t_film(self) -> float:
        """
        T_film, Average temperature of the boundary layer
        """
        return (self.max_allowable_conductor_temperature + self.ambient_temperature) / 2

    @property
    def air_density(self) -> float:
        """
        ρf, Density of air
        :return:
        """
        return (1.293 - 1.525e-4 * self.elevation + 6.379e-9 * self.elevation**2) / (1 + 0.00367 * self.t_film)

    @property
    def air_viscosity(self) -> float:
        """
        µf, Absolute (dynamic) viscosity of air
        """
        return float((1.458e-6 * (self.t_film + 273) ** 1.5) / (self.t_film + 383.4))

    @property
    def air_thermal_conductivity(self) -> float:
        """
        kf, Thermal conductivity of air
        """
        return 2.424e-2 + 7.477e-5 * self.t_film - 4.407e-9 * (self.t_film**2)

    @property
    def wind_direction_factor(self) -> float:
        """
        K_angle, Wind direction factor.
        """
        return (
            1.194
            - math.cos(self.wind_direction)
            + 0.194 * math.cos(2 * self.wind_direction)
            + 0.68 * math.sin(2 * self.wind_direction)
        )

    @property
    def radiated_heat_loss(self) -> float:
        """
        q_r, Radiated heat loss
        """
        return (
            17.8
            * self.conductor_outside_diameter
            * self.emissivity
            * (((self.conductor_surface_temperature + 273) / 100) ** 4 - ((self.ambient_temperature + 273) / 100) ** 4)
        )

    @property
    def solar_declination(self) -> float:
        """
        δ, The solar declination (the angular distance of the sun from the Earth’s equator), δ, in degrees
        :return:
        """
        return 23.45 * math.sin(((284 + self.number_of_day) / 365) * 360)

    @property
    def hour_angle(self) -> float:
        """
        "ω, Hour angle"
        """
        return (self.date.hour - 12) * 15

    @property
    def solar_azimuth(self) -> float:
        """
        Z_c, Solar azimuth
        """
        X = math.sin(self.hour_angle) / (
            math.sin(self.latitude) * math.cos(self.hour_angle)
            - math.cos(self.latitude) * math.tan(self.solar_declination)
        )
        if X >= 0 and -180 <= self.hour_angle < 0:
            C = 0
        elif X >= 0 and 0 <= self.hour_angle < 180:
            C = 180
        elif X < 0 and -180 <= self.hour_angle < 0:
            C = 180
        elif X < 0 and 0 <= self.hour_angle < 180:
            C = 360
        else:
            raise ValueError

        Z_c = C + math.atan(X)

        return Z_c

    @property
    def solar_altitude(self) -> float:
        """
        Hc, Solar altitude
        """
        return math.asin(
            math.cos(self.latitude) * math.cos(self.solar_declination) * math.cos(self.hour_angle)
            + math.sin(self.latitude) * math.sin(self.solar_declination)
        )

    @property
    def total_solar_and_sky_radiated_heat_intensity_at_sea_level(self) -> float:
        """
        Qs, Total solar and sky radiated heat intensity at sea level
        """
        coefficient_table = (
            PolynomialCoefficientsOfClearAtmosphere
            if self.clear_atmosphere
            else PolynomialCoefficientsOfIndustrialAtmosphere
        )

        Qs = (
            coefficient_table["A"]
            + coefficient_table["B"] * self.solar_altitude
            + coefficient_table["C"] * self.solar_altitude**2
            + coefficient_table["D"] * self.solar_altitude**3
            + coefficient_table["E"] * self.solar_altitude**4
            + coefficient_table["F"] * self.solar_altitude**5
            + coefficient_table["G"] * self.solar_altitude**6
        )

        return Qs

    @property
    def total_solar_and_sky_radiated_heat_intensity_factor(self) -> float:
        """
        K_solar,
        """
        return 1 + 1.148e-4 * self.elevation + (-1.108e8 * self.elevation**2)

    @property
    def total_solar_and_sky_radiated_heat_intensity(self) -> float:
        """
        Q_se, Total solar and sky radiated heat intensity corrected for elevation
        """
        return (
            self.total_solar_and_sky_radiated_heat_intensity_factor
            * self.total_solar_and_sky_radiated_heat_intensity_at_sea_level
        )

    @property
    def solar_heat_gain(self) -> float:
        """
        q_s, Solar heat gain
        """
        return 0
        # theta = math.acos(math.cos() *  (self.solar_altitude -))
        # return self.solar_absorption * self.total_solar_and_sky_radiated_heat_intensity * math.sin()
