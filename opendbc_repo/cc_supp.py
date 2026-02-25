def create_suppress_lfa(packer, CAN, lfa_block_msg, lka_steering_alt):
  suppress_msg = "CAM_0x362" if lka_steering_alt else "CAM_0x2a4"
  msg_bytes = 32 if lka_steering_alt else 24

  values = {f"BYTE{i}": lfa_block_msg[f"BYTE{i}"] for i in range(3, msg_bytes) if i != 7}
  values["COUNTER"] = lfa_block_msg["COUNTER"]
  values["SET_ME_0"] = 0
  values["SET_ME_0_2"] = 0
  values["LEFT_LANE_LINE"] = 0
  values["RIGHT_LANE_LINE"] = 0
  return packer.make_can_msg(suppress_msg, CAN.ACAN, values)


def create_buttons(packer, CP, CAN, cnt, btn):
  canfd_msg = "CRUISE_BUTTONS_ALT" if CP.flags & HyundaiFlags.CANFD_ALT_BUTTONS else \
              "CRUISE_BUTTONS"
  # If we discover cars use different values for this in the future, echoing back
  # what's read from the car would also work.
  SET_ME_2 = 6
  values = {
    "COUNTER": cnt,
    "CRUISE_BUTTONS": btn,
    "SET_ME_1": 1,
  } | {"SET_ME_2": SET_ME_2} if CP.flags & HyundaiFlags.CANFD_ALT_BUTTONS else {}
