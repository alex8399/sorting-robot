class CommandUnit:

    def __init__(self):
        self.dispenser_is_running = True
        self.conveyor_is_running = True
        self.pushing_one_disk = False
        self.pushing_disks_infinitely = False

    def get_pushing_one_disk(self) -> bool:
        return self.pushing_one_disk

    def set_pushing_one_disk(self, value: bool):
        self.pushing_one_disk = value

    def get_pushing_disks_infinitely(self) -> bool:
        return self.pushing_disks_infinitely

    def set_pushing_disks_infinitely(self, value: bool):
        self.pushing_disks_infinitely = value

    def get_conveyor_is_running(self) -> bool:
        return self.conveyor_is_running

    def set_conveyor_is_running(self, value: bool) -> bool:
        self.conveyor_is_running = value

    def get_dispenser_is_running(self) -> bool:
        return self.dispenser_is_running

    def set_dispenser_is_running(self, value: bool) -> bool:
        self.conveyor_is_running = value
