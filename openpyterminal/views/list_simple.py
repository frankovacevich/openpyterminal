from .list_extended import ListExtended


class ListSimple(ListExtended):

    def __init__(self, title):
        super().__init__(title)
        self.frame_btn_c_alt_out.setHidden(False)
        self.frame_btn_d_alt_out.setHidden(False)
        self.sidebar.setHidden(True)

    def hide_btn_c(self):
        self.frame_btn_c_alt_out.setHidden(True)
