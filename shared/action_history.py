from shared.linked_list import LinkedList
from datetime import datetime
# Global linked list object
dll = LinkedList()
dll.append(['Simulation Started', str(datetime.now())])

dll_expected = LinkedList()
dll_expected.append(['Simulation Started', str(datetime.now())])
dll_expected.append(['Checked Patient Details', '2025-04-07 14:13:26'])
dll_expected.append(['Checked Medical History', '2025-04-07 14:13:35'])
dll_expected.append(['Checked Vitals', '2025-04-07 14:13:50'])
dll_expected.append(['Administered CPR', '2 inches | Compression rate: 100/min'])
dll_expected.append(['Attached Defibrillator', '2025-04-14 23:57:49.040016'])
dll_expected.append(['Shocked Patient', 'Once | Energy: 160J'])
dll_expected.append(['Administered Epinephrine | Oral (PO)', '8 mL, just once'])
dll_expected.append(['Shocked Patient', 'Once | Energy: 160J'])
dll_expected.append(['Administered Amiodarone | Oral (PO)', '400 mg, just once'])
dll_expected.append(['Shocked Patient', 'Once | Energy: 160J'])
dll_expected.append(['Pulse returned to normal'])
dll_expected.append(['Simulation Ended'])