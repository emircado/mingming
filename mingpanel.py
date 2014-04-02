import random

class mingswitch:

	def __init__(self, sid):
		self.sid = sid

_switches = [
	mingswitch(0),
	mingswitch(1),
	mingswitch(2),
	mingswitch(3),
	mingswitch(4),
	mingswitch(5),
	mingswitch(6),
	mingswitch(7),
	mingswitch(8),
	mingswitch(9),
	mingswitch(10),
	mingswitch(11),
	mingswitch(12),
	mingswitch(13),
	mingswitch(14),
	mingswitch(15),
	mingswitch(16),
	mingswitch(17),
	mingswitch(18),
	mingswitch(19),
	mingswitch(20),
	mingswitch(21),
	mingswitch(22),
	mingswitch(23),
	mingswitch(24),
	mingswitch(25),
	mingswitch(26),
	mingswitch(27),
	mingswitch(28),
	mingswitch(29),
	mingswitch(30),
	mingswitch(31),
	mingswitch(32),
	mingswitch(33),
	mingswitch(34),
	mingswitch(35),
	mingswitch(36),
	mingswitch(37),
	mingswitch(38),
	mingswitch(39),
	mingswitch(40),
	mingswitch(41),
	mingswitch(42),
	mingswitch(43),
	mingswitch(44),
	mingswitch(45),
	mingswitch(46),
	mingswitch(47),
	mingswitch(48),
	mingswitch(49)
]
	
def generate_panels():
	panels = [i for i in range(len(_switches))]
	random.shuffle(panels)
	return [panels[0:6], panels[6:12], panels[12:18], panels[18:24]]