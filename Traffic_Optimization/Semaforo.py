class Semaforo:
    def __init__(self, id, ctrl_lanes, crrt_phse, crrt_phse_dur, rmn_dur):
        self.id = id
        self.ctrl_lanes = ctrl_lanes
        self.crrt_phse = crrt_phse
        self.phs_dur = crrt_phse_dur + rmn_dur