class TimeHandler:
    """Factory for creating a time handler instance based on the specified library."""

    @staticmethod
    def create_handler(epoch_str, library="astropy"):
        """
        Create a time handler instance based on the specified library.

        Args:
            epoch_str (str): The epoch time string in ISO 8601 format.
            library (str): The library to use for time conversion.

        Returns:
            TimeHandlerBase: An instance of the appropriate time handler.
        """
        if library == "my":
            from handlers.my_time_handler import MyTimeHandler
            return MyTimeHandler(epoch_str)
        elif library == "astropy":
            from handlers.astropy_time_handler import AstropyTimeHandler
            return AstropyTimeHandler(epoch_str)
        elif library == "spice":
            from handlers.spice_time_handler import SpiceTimeHandler
            return SpiceTimeHandler(epoch_str)
        elif library == "skyfield":
            from handlers.skyfield_time_handler import SkyfieldTimeHandler
            return SkyfieldTimeHandler(epoch_str)
        elif library == "spacepy":
            from handlers.spacepy_time_handler import SpacepyTimeHandler
            return SpacepyTimeHandler(epoch_str)
        else:
            raise ValueError(f"Unsupported library specified: {library}")
