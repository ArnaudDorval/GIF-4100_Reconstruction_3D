
class camera_calib_var:
    def __init__(self, ret, cameraMatrix, dist, rvecs, tvecs):
        self.ret = ret
        self.cameraMatrix = cameraMatrix
        self.dist = dist
        self.rvecs = rvecs
        self.tvecs = tvecs
