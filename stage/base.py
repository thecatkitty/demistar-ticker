from ticker.matrix import MatrixDisplay
from ticker.ring import Ring


class Stage:
    def show(self) -> None:
        pass

    def update(self) -> None:
        pass

    def to_dict(self) -> dict:
        return dict()


class Board:
    top: MatrixDisplay
    bottom: MatrixDisplay
    inner: Ring
    outer: Ring

    def __init__(self, top_display: MatrixDisplay, bottom_display: MatrixDisplay, inner_ring: Ring, outer_ring: Ring) -> None:
        self.top = top_display
        self.bottom = bottom_display
        self.inner = inner_ring
        self.outer = outer_ring
