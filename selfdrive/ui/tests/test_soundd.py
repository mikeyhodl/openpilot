from cereal import car
from cereal import messaging
from cereal.messaging import SubMaster, PubMaster
from openpilot.selfdrive.ui.soundd import CONTROLS_TIMEOUT, check_controls_timeout_alert

import time

AudibleAlert = car.CarControl.HUDControl.AudibleAlert


class TestSoundd:
  def test_check_controls_timeout_alert(self):
    sm = SubMaster(['selfdriveState'])
    pm = PubMaster(['selfdriveState'])

    for _ in range(100):
      cs = messaging.new_message('selfdriveState')
      cs.selfdriveState.enabled = True

      pm.send("selfdriveState", cs)

      time.sleep(0.01)

      sm.update(0)

      assert not check_controls_timeout_alert(sm)

    for _ in range(CONTROLS_TIMEOUT * 110):
      sm.update(0)
      time.sleep(0.01)

    assert check_controls_timeout_alert(sm)

  # TODO: add test with micd for checking that soundd actually outputs sounds

