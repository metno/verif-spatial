
class DataReader:
    """Data reader base class"""
    def __init__(
        self,
        path,
    ) -> None:
        self.path = path

    def _interpolate_(
        self,
        interp_res,
    ) -> None:
        pass

    def _interpolate_if_1d(
        self,
        interp_res,
    ) -> None:

        if len(self.data.shape) < 4:
            self._interpolate_()
